from django.contrib import admin

from goals.models import Category, Goal, Comment


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user__username")


class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "due_date", "status", "priority", "created", "updated")
    search_fields = ("title", "user__username", "description")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "user", "goal", "created", "updated")
    search_fields = ("text", "user__username")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Comment, CommentAdmin)

