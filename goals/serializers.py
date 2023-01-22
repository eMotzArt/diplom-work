from rest_framework import serializers

from core.serializers import ProfileRetrieveUpdateSerializer
from goals.models import Category, Goal, Comment


class CategoryListSerializer(serializers.ModelSerializer):
    user = ProfileRetrieveUpdateSerializer(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class CategoryUpdateSerializer(serializers.ModelSerializer):
    user = ProfileRetrieveUpdateSerializer(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

class CategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ("id", "created", "updated", "user")


class GoalListSerializer(serializers.ModelSerializer):
    user = ProfileRetrieveUpdateSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = '__all__'


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.PrimaryKeyRelatedField(
        default=CategoryListSerializer,
        queryset=Category.objects.all(),
    )

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")

        return value

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

    class Meta:
        model = Goal
        fields = '__all__'


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

    def validate_goal(self, value):
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of goal")

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
