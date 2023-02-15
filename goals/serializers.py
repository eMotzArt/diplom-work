from django.db import transaction
from rest_framework import serializers

from core.models import User
from core.serializers import ProfileRetrieveUpdateSerializer
from goals.models import Category, Goal, Comment, Board, BoardParticipant


# categories
class CategoryListSerializer(serializers.ModelSerializer):
    user = ProfileRetrieveUpdateSerializer(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('title', 'user', 'is_deleter', 'board', 'id', 'created', 'updated')


class CategoryUpdateSerializer(serializers.ModelSerializer):
    user = ProfileRetrieveUpdateSerializer(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created', 'updated', 'is_deleted', 'board')


class CategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ("id", "created", "updated", "user")


# goals
class GoalListSerializer(serializers.ModelSerializer):
    user = ProfileRetrieveUpdateSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', 'category', 'title', 'description', 'status', 'priority', 'due_date')


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.PrimaryKeyRelatedField(
        default=CategoryListSerializer,
        queryset=Category.objects.all(),
    )

    def validate_category(self, category: Category) -> Category:
        if category.is_deleted:
            raise serializers.ValidationError("You cannot create goal with deleted category")

        # проверка не нужна, т.к. owner и writer пропускаются в permissions, другие сюда не попадают

        # if not category.board.participants.filter(
        #         user=self.context["request"].user,
        #         role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]).exists():
        #     raise serializers.ValidationError("You cannot create in this category")

        return category

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ("id", "created", "updated", "user")


class GoalUpdateSerializer(serializers.ModelSerializer):
    user = ProfileRetrieveUpdateSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        default=CategoryListSerializer,
        queryset=Category.objects.all(),
    )

    def update(self, instance: Goal, validated_data: dict) -> Goal:
        validated_data.pop('user')
        return super().update(instance, validated_data)

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ("id", "created", "updated", "user")


# comments
class CommentListSerializer(serializers.ModelSerializer):
    user = ProfileRetrieveUpdateSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    goal = serializers.PrimaryKeyRelatedField(
        default=GoalListSerializer,
        queryset=Goal.objects.all(),
    )

    # проверка перенесена в permissions
    # def validate_goal(self, value):
    #     if value.user != self.context["request"].user:
    #         raise serializers.ValidationError("not owner of goal")

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ("id", "created", "updated", "user")


class CommmentUpdateSerializer(serializers.ModelSerializer):
    user = ProfileRetrieveUpdateSerializer(read_only=True)
    goal = serializers.PrimaryKeyRelatedField(
        default=GoalListSerializer,
        queryset=Goal.objects.all(),
    )

    class Meta:
        model = Comment
        fields = '__all__'


# boards
class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(required=True, choices=BoardParticipant.Role.choices)
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'title', 'is_deleted')


class BoardRetrieveSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ('id', 'created', 'updated', 'title', 'is_deleted')


class BoardUpdateSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board", "is_deleted")

    def update(self, instance: Board, validated_data: dict) -> Board:
        board_owner = BoardParticipant.objects.filter(board=instance, role=BoardParticipant.Role.owner).first().user

        caller = validated_data.pop('user')
        title = validated_data.pop('title')

        new_participants = validated_data.pop('participants')
        new_participants_ids = {participant['user'].id: participant
                                for participant in new_participants
                                if participant['user'].id != caller.id and participant['user'].id != board_owner.id} #вызывающий человек не может редактировать себя (понижать до читателя), и редактировать владельца, их исключаем

        # защита от хитреца - никто не может выдать права владельца
        for new_participant in new_participants_ids.values():
            if new_participant['role'] == BoardParticipant.Role.owner:
                new_participant['role'] = BoardParticipant.Role.writer

        old_participants = instance.participants.exclude(user__in=[caller, board_owner])
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user.id not in new_participants_ids:
                    old_participant.delete()
                    continue

                if old_participant.role != new_participants_ids[old_participant.user.id]['role']:
                    old_participant.role = new_participants_ids[old_participant.user.id]['role']
                    old_participant.save()

                new_participants_ids.pop(old_participant.user.id)

            for new_participant in new_participants_ids.values():
                BoardParticipant.objects.create(board=instance,
                                                user=new_participant["user"],
                                                role=new_participant["role"]
                )

            if instance.title != title: instance.title = title

            instance.save()

        return instance


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ("id", "created", "updated")

    def create(self, validated_data: dict) -> Board:
        user = validated_data.pop("user")
        with transaction.atomic():
            board = Board.objects.create(**validated_data)
            BoardParticipant.objects.create(user=user, board=board, role=BoardParticipant.Role.owner)
        return board
