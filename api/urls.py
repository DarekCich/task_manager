from django.urls  import path, include
from .views       import TaskViewSet, UserRegistrationView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = [
  path('', include(router.urls)),
  path('history/',          TaskViewSet.as_view({'get': 'task_history'}), name='api_task_history'),
  path('history/<int:pk>/', TaskViewSet.as_view({'get': 'task_history'}), name='api_task_history'),
  path('register/',         UserRegistrationView.as_view(), name='user-registration'),
]

