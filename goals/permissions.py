from rest_framework import permissions
from rest_framework.request import Request

from goals.models import BoardParticipant, Category, Goal, Board, Comment


class IsBoardParticipant(permissions.BasePermission):
    def has_object_permission(self, request: Request, view, obj: Board) -> bool:
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user,
                                                   board=obj).exists()

        if request.method == 'PUT':
            return BoardParticipant.objects.filter(
                user=request.user,
                board=obj,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]).exists()

        return BoardParticipant.objects.filter(user=request.user,
                                               board=obj,
                                               role=BoardParticipant.Role.owner).exists()


class IsGoalWriterOrOwner(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        if not request.user.is_authenticated:
            return False

        if request.method == 'POST':
            category_num = request.data.get('category', None)
            if not category_num: return False

            category = Category.objects.get(id=category_num)
            board = category.board

            return BoardParticipant.objects.filter(
                user=request.user,
                board=board,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]).exists()

        return True

    def has_object_permission(self, request: Request, view, obj: Goal) -> bool:
        if not request.user.is_authenticated:
            return False

        obj_board = obj.category.board

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user,
                                                   board=obj_board).exists()

        if request.method == 'PUT':
            return BoardParticipant.objects.filter(
                user=request.user,
                board=obj_board,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]).exists()

        return BoardParticipant.objects.filter(user=request.user,
                                               board=obj_board,
                                               role=BoardParticipant.Role.owner).exists()


class IsCategoryWriterOrOwner(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        if not request.user.is_authenticated:
            return False

        if request.method == 'POST':
            board_num = request.data.get('board', None)
            if not board_num: return False
            return BoardParticipant.objects.filter(
                user=request.user,
                board_id=board_num,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]).exists()

        return True

    def has_object_permission(self, request: Request, view, obj: Category) -> bool:
        if not request.user.is_authenticated:
            return False

        obj_board = obj.board

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user,
                                                   board=obj_board).exists()

        if request.method == 'PUT':
            return BoardParticipant.objects.filter(
                user=request.user,
                board=obj_board,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]).exists()

        return BoardParticipant.objects.filter(user=request.user,
                                               board=obj_board,
                                               role=BoardParticipant.Role.owner).exists()


class IsCommentWriterOrOwner(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        if not request.user.is_authenticated:
            return False

        if request.method == 'POST':
            goal_num = request.data.get('goal', None)
            if not goal_num: return False
            goal = Goal.objects.get(id=goal_num)
            board = goal.category.board
            return BoardParticipant.objects.filter(
                user=request.user,
                board=board,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]).exists()

        return True

    def has_object_permission(self, request: Request, view, obj: Comment):
        if not request.user.is_authenticated:
            return False

        obj_board = obj.goal.category.board

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user,
                                                   board=obj_board).exists()

        if request.method in ['PUT', 'DELETE']:
            return obj.user == request.user

        return BoardParticipant.objects.filter(user=request.user,
                                               board=obj_board,
                                               role=BoardParticipant.Role.owner).exists()
