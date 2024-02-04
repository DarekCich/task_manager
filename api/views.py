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
  
  def list(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())
    serializer = self.serializer_class(queryset, many=True)
    return Response(serializer.data)

  def create(self, request):
    serializer = self.serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def retrieve(self, request, pk=None):
    instance    = self.get_object()
    serializer  = self.serializer_class(instance)
    return Response(serializer.data)
  
  def update(self, request, pk=None):
    instance    = self.get_object()
    serializer  = TaskSerializer(instance, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def partial_update(self, request, pk=None):
    instance    = self.get_object()
    serializer  = TaskSerializer(instance, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def destroy(self, request, pk=None):
    instance = self.get_object()
    self.perform_destroy(instance)
    return Response({'status': 'success', 'message': f'Zadanie o id={pk} zostało usunięte.'}, status=status.HTTP_200_OK)
  
  @action(detail=False, methods=['get'])
  def task_history(self, request, pk=None):
    task = self.get_object() if pk else None
    history = task.history.all() if task else Task.history.all()

    # Użyj filtra TaskHistoryFilter
    filter_set = TaskHistoryFilter(request.GET, queryset=history)
    queryset = filter_set.qs

    serializer = TaskHistoryListSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
class UserRegistrationView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserRegistrationSerializer