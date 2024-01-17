from django.shortcuts import get_object_or_404
from tasks.models     import Task
from django.db.models import Q
from rest_framework   import viewsets, status, generics
from django.contrib.auth.models import User
from rest_framework.decorators  import action
from rest_framework.response    import Response
from .serializers               import TaskSerializer, TaskHistoryListSerializer, UserRegistrationSerializer

class TaskViewSet(viewsets.ModelViewSet):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer

  @action(detail=False, methods=['get'])
  def task_list(self, request):
    tasks = Task.objects.all()

    task_status = request.query_params.get('status')
    nazwa       = request.query_params.get('nazwa')
    opis        = request.query_params.get('opis')
    opis_nazwa  = request.query_params.get('opis_nazwa')
    sort_by     = request.query_params.get('sort_by')
    przypisany_uzytkownik = request.query_params.get('przypisany_uzytkownik')

    if task_status:
      tasks = tasks.filter(status=task_status)
    if opis:
      tasks = tasks.filter(opis__icontains=opis)
    if nazwa:
      tasks = tasks.filter(nazwa__icontains=nazwa)
    if opis_nazwa:
      tasks = tasks.filter(Q(nazwa__icontains=opis_nazwa)| Q(opis__icontains=opis_nazwa))
    if przypisany_uzytkownik:
      tasks = tasks.filter(przypisany_uzytkownik__username__icontains=przypisany_uzytkownik)
    if sort_by:
      tasks = tasks.order_by(sort_by)

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @action(detail=True, methods=['post'])
  def task_add(self, request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
      username = request.data.get('przypisany_uzytkownik')
      if username:
        user_exists = User.objects.filter(username=username).exists()
        if not user_exists:
          return Response({'status': 'error', 'message': 'Użytkownik o podanym username nie istnieje'}, status=status.HTTP_400_BAD_REQUEST)
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  @action(detail=False, methods=['get'])
  def task_history(self, request, pk=None):
    if pk:
      task = get_object_or_404(Task, pk=pk)
    else:
      task = Task

    history = task.history.all()
    date = request.query_params.get('date')
    if date:
      history = history.filter(history_date__date=date)

    serializer = TaskHistoryListSerializer(history, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @action(detail=True, methods=['delete'])
  def task_delete(self, request, pk=None):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return Response({'status': 'success', 'message': f'Zadanie o id={pk} zostało usunięte.'}, status=status.HTTP_200_OK)

  @action(detail=True, method=['get'])
  def task_detail(self, request, pk=None):
    task = get_object_or_404(Task, pk=pk)
    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  @action(detail=True, methods=['put'])
  def task_update(self, request, pk=None):
    task = get_object_or_404(Task, pk=pk)
    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class UserRegistrationView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserRegistrationSerializer