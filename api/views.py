from tasks.models                   import Task
from django_filters.rest_framework  import DjangoFilterBackend
from rest_framework             import viewsets, status, generics, filters
from django.contrib.auth.models import User
from rest_framework.decorators  import action
from rest_framework.response    import Response
from .serializers               import TaskSerializer, TaskHistoryListSerializer, UserRegistrationSerializer
from .filters import TaskFilter, TaskHistoryFilter

class TaskViewSet(viewsets.ModelViewSet):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
  filterset_class = TaskFilter

  @action(detail=False, methods=['get'])
  def task_history(self, request, pk=None):
    task = self.get_object() if pk else None
    history = task.history.all() if task else Task.history.all()

    filter_set = TaskHistoryFilter(request.GET, queryset=history)
    queryset = filter_set.qs
    # Wolniej, ale zwraca tylko dane Task
    # serializer = TaskHistoryListSerializer(queryset, many=True)
    # return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(list(queryset.values()), status=status.HTTP_200_OK)
    

class UserRegistrationView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserRegistrationSerializer

