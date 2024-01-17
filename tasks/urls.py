from django.urls                import path, include
from django.contrib.auth.views  import LogoutView
from rest_framework.routers     import DefaultRouter
from .views                     import TaskViewSet, CustomUser

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
  path('history/<int:pk>/', TaskViewSet.as_view({'get': 'task_history'}),                           name='task_history'),
  path('history/',          TaskViewSet.as_view({'get': 'task_history'}),                           name='task_history'),
  path('add/',              TaskViewSet.as_view({'get': 'task_add', 'post': 'task_add'}),           name='task_add'),
  path('tasks/',            TaskViewSet.as_view({'get': 'task_list'}),                              name='task_list'),
  path('detail/<int:pk>/',  TaskViewSet.as_view({'get': 'task_detail'}),                            name='task_detail'),
  path('edit/<int:pk>/',    TaskViewSet.as_view({'get': 'task_edit', 'post': 'task_edit'}),         name='task_edit'),
  path('delete/<int:pk>/',  TaskViewSet.as_view({'get': 'task_delete','post': 'task_delete'}),      name='task_delete'),
  path('login/',            CustomUser.CustomLoginView.as_view(),                                   name='user_login'),
  path('register/',         CustomUser.CustomRegisterView.as_view(),                                name='user_register'),
  path('logout/',           LogoutView.as_view(next_page='task_list'),                              name='user_logout'),
  path('', include(router.urls)),
]
