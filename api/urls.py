from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, UserRegistrationView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
  path('tasks/',            TaskViewSet.as_view({'get': 'task_list', 'post':'task_add'}), name='api_task_list'),
  path('tasks/<int:pk>/',   TaskViewSet.as_view({'get': 'task_detail', 'put':'task_update','delete': 'task_delete'}), name='api_task_list'),
  path('history/',          TaskViewSet.as_view({'get': 'task_history'}), name='api_task_history'),
  path('history/<int:pk>/', TaskViewSet.as_view({'get': 'task_history'}), name='api_task_history'),
  path('register/',         UserRegistrationView.as_view(), name='user-registration'),
]

