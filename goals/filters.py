from django.db import models
from django_filters import rest_framework, IsoDateTimeFilter

from goals.models import Goal, Comment, Category


class GoalDateFilter(rest_framework.FilterSet):
    class Meta:
        model = Goal
        fields = {
            "due_date": ("lte", "gte"),
            "category": ("exact", "in"),
            "status": ("exact", "in"),
            "priority": ("exact", "in"),
        }

    filter_overrides = {
        models.DateTimeField: {"filter_class": IsoDateTimeFilter},
    }


class CommentGoalFilter(rest_framework.FilterSet):
    class Meta:
        model = Comment
        fields = {
            "goal": ("exact",)
        }


class BoardCategoryFilter(rest_framework.FilterSet):
    class Meta:
        model = Category
        fields = {
            "board": ("exact", ),
        }
