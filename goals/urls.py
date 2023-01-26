from django.urls import path
from goals import views


urlpatterns = [
    #goal_category
    path('goal_category/list', views.CategoriesViews.as_view({'get': 'list'})),
    path('goal_category/create', views.CategoriesViews.as_view({'post': 'create'})),
    path('goal_category/<pk>', views.CategoriesViews.as_view({'get': 'retrieve',
                                                              'put': 'update',
                                                              'delete': 'destroy'})),

    #goals
    path('goal/list', views.GoalsViews.as_view({'get': 'list'})),
    path('goal/create', views.GoalsViews.as_view({'post': 'create'})),
    path('goal/<pk>', views.GoalsViews.as_view({'get': 'retrieve',
                                                'put': 'update',
                                                'delete': 'destroy'})),

    #comments
    path('goal_comment/list', views.CommentsViews.as_view({'get': 'list'})),
    path('goal_comment/create', views.CommentsViews.as_view({'post': 'create'})),
    path('goal_comment/<pk>', views.CommentsViews.as_view({'get': 'retrieve',
                                                           'put': 'update',
                                                           'delete': 'destroy'})),

    #board
    path('board/list', views.BoardsViews.as_view({'get': 'list'})),
    path('board/create', views.BoardsViews.as_view({'post': 'create'})),
    path('board/<pk>', views.BoardsViews.as_view({'get': 'retrieve',
                                                         'put': 'update',
                                                         'delete': 'destroy'})),
]
