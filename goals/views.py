# 3rd-party import
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters
from rest_framework import viewsets

# app import
from goals.filters import GoalDateFilter, CommentGoalFilter
from goals.models import Goal, Category, Comment
from goals.serializers import CategoryCreateSerializer, CategoryListSerializer, CategoryUpdateSerializer, \
    GoalCreateSerializer, GoalListSerializer, GoalUpdateSerializer,\
    CommentListSerializer, CommentCreateSerializer, CommmentUpdateSerializer


class CategoriesViews(viewsets.ModelViewSet):
    # service
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = Category.objects.all()
    serializers = {
        'list': CategoryListSerializer,
        'retrieve': CategoryListSerializer,
        'create': CategoryCreateSerializer,
        'update': CategoryUpdateSerializer,
    }
    serializer_class = CategoryCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    # overrides
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, is_deleted=False)

    def get_serializer_class(self):
        return self.serializers.get(self.action)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.archive_related_goals()
        instance.save()


class GoalsViews(viewsets.ModelViewSet):
    # service
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = Goal.objects.all()
    serializers = {
        'list': GoalListSerializer,
        'retrieve': GoalListSerializer,
        'create': GoalCreateSerializer,
        'update': GoalUpdateSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]

    # filtering
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ['priority', 'due_date']
    ordering = ['priority', 'due_date']
    search_fields = ['title', 'description']

    # overrides
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, status__in=[1, 2, 3])

    def get_serializer_class(self):
        return self.serializers.get(self.action)

    def perform_create(self, serializer):
        serializer.save(category=Category.objects.get(id=self.request.data['category']))

    def perform_update(self, serializer):
        serializer.save(user=self.request.user, category=Category.objects.get(id=self.request.data['category']))

    def perform_destroy(self, instance):
        instance.status = 4
        instance.save()


class CommentsViews(viewsets.ModelViewSet):
    # service
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = Comment.objects.all()
    serializers = {
        'list': CommentListSerializer,
        'retrieve': CommentListSerializer,
        'create': CommentCreateSerializer,
        'update': CommmentUpdateSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]

    # filtering
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = ['created', 'updated', ]
    filterset_class = CommentGoalFilter
    ordering = ['-created', ]

    # overrides
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, goal__status__in=[1, 2, 3])

    def get_serializer_class(self):
        return self.serializers.get(self.action)

    def perform_create(self, serializer):
        serializer.save(goal=Goal.objects.get(pk=self.request.data['goal']))

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

