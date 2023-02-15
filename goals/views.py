# 3rd-party import
from django.db import transaction
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters
from rest_framework import viewsets

# app import
from goals.filters import GoalDateFilter, CommentGoalFilter, BoardCategoryFilter
from goals.models import Goal, Category, Comment, Board
from goals.permissions import IsBoardParticipant, IsGoalWriterOrOwner, IsCategoryWriterOrOwner, IsCommentWriterOrOwner
from goals.serializers import (
    CategoryListSerializer, CategoryCreateSerializer, CategoryUpdateSerializer,
    GoalListSerializer, GoalCreateSerializer, GoalUpdateSerializer,
    CommentListSerializer, CommentCreateSerializer, CommmentUpdateSerializer,
    BoardListSerializer, BoardCreateSerializer, BoardRetrieveSerializer, BoardUpdateSerializer)


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
    permission_classes = [permissions.IsAuthenticated, IsCategoryWriterOrOwner]

    # filtering
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = BoardCategoryFilter


    # overrides
    def get_queryset(self):
        return self.queryset.filter(board__participants__user=self.request.user, is_deleted=False)

    def get_serializer_class(self):
        return self.serializers.get(self.action)

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.goals.all().update(status=4)
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
    permission_classes = [permissions.IsAuthenticated, IsGoalWriterOrOwner]

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
    def get_queryset(self) -> QuerySet:
        accessed_categories = Category.objects.filter(board__participants__user=self.request.user, is_deleted=False)
        return Goal.objects.filter(category__in=accessed_categories, status__in=[1, 2, 3])

    def get_serializer_class(self):
        return self.serializers.get(self.action)

    def perform_create(self, serializer) -> None:
        serializer.save(category=Category.objects.get(id=self.request.data['category']))

    def perform_update(self, serializer) -> None:
        serializer.save(user=self.request.user, category=Category.objects.get(id=self.request.data['category']))

    def perform_destroy(self, instance: Goal) -> None:
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
    permission_classes = [permissions.IsAuthenticated, IsCommentWriterOrOwner]

    # filtering
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = ['created', 'updated', ]
    filterset_class = CommentGoalFilter
    ordering = ['-created', ]

    # overrides
    def get_queryset(self) -> QuerySet:
        accessed_categories = Category.objects.filter(board__participants__user=self.request.user, is_deleted=False)
        return self.queryset.filter(goal__category__in=accessed_categories, goal__status__in=[1, 2, 3])

    def get_serializer_class(self):
        return self.serializers.get(self.action)

    def perform_create(self, serializer) -> None:
        serializer.save(goal=Goal.objects.get(pk=self.request.data['goal']))

    def perform_update(self, serializer) -> None:
        serializer.save(user=self.request.user)

class BoardsViews(viewsets.ModelViewSet):
    # service
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = Board.objects.all()
    serializers = {
        'list': BoardListSerializer,
        'retrieve': BoardRetrieveSerializer,
        'create': BoardCreateSerializer,
        'update': BoardUpdateSerializer,
    }
    permission_classes = [permissions.IsAuthenticated, IsBoardParticipant]

    # filtering
    filter_backends = [
        filters.OrderingFilter,
    ]
    ordering = ['title', ]

    # overrides
    def get_queryset(self) -> QuerySet:
        return self.queryset.select_related().filter(participants__user=self.request.user, is_deleted=False)

    def get_serializer_class(self):
        return self.serializers.get(self.action)

    def perform_destroy(self, instance: Board) -> None:
        with transaction.atomic():
            instance.is_deleted = True
            [category.goals.update(status=4) for category in instance.categories.all()]
            instance.categories.update(is_deleted=True)
            instance.save()

