from django.contrib.auth.forms  import UserCreationForm
from django.views.generic.edit  import CreateView
from django.urls                import reverse_lazy
from django.shortcuts           import render, redirect, get_object_or_404
from .models                    import Task
from .forms                     import TaskForm, TaskFilterForm, HistoryTaskFilterForm
from rest_framework             import viewsets
from rest_framework.decorators  import action
from rest_framework.response    import Response
from .serializers               import TaskSerializer
from django.contrib.auth.views  import LoginView
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated

class TaskViewSet(viewsets.ModelViewSet):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer
  
  @action(detail=False, methods=['get'])
  def task_list(self, request):
    if not request.user.is_authenticated:
      return render(request, 'task_list.html')
    original_tasks = Task.objects.all()
    tasks = original_tasks

    filter_form = TaskFilterForm(request.GET)
    if filter_form.is_valid():
      status = filter_form.cleaned_data.get('status')
      nazwa = filter_form.cleaned_data.get('nazwa')
      przypisany_uzytkownik = filter_form.cleaned_data.get('przypisany_uzytkownik')
      sort_by = filter_form.cleaned_data.get('sort_by')

      if status:
        tasks = tasks.filter(status=status)
      if nazwa:
        tasks = tasks.filter(nazwa__icontains=nazwa)
      if przypisany_uzytkownik:
        tasks = tasks.filter(przypisany_uzytkownik__username__icontains=przypisany_uzytkownik)

      if sort_by:
        tasks = tasks.order_by(sort_by)

    return render(request, 'task_list.html', {'tasks': tasks, 'filter_form': filter_form, 'original_tasks': original_tasks})
  @action(detail=False, methods=['get', 'post'])
  def task_add(self, request):
    if not request.user.is_authenticated:
      return redirect('task_list')
    if request.method == 'POST':
      form = TaskForm(request.POST)
      if form.is_valid():
        form.save()
        return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'task_add.html', {'form': form})
  
  @action(detail=True, methods=['get'])
  def task_history(self, request, pk=None):
    if not request.user.is_authenticated:
      return redirect('task_list')
    filter_form = HistoryTaskFilterForm(request.GET)
    if filter_form.is_valid():
      date = filter_form.cleaned_data.get('date')
      if date:
        if pk:
          task = get_object_or_404(Task, pk=pk)
          history = task.history.all().filter(history_date__date=date)
          return render(request, 'task_history.html', {'tasks': history, 'id': pk,'filter_form':filter_form})
        return render(request, 'task_history.html', {'tasks': Task.history.all().filter(history_date__date=date),'filter_form':filter_form})
      if pk:
        task = get_object_or_404(Task, pk=pk)
        history = task.history.all()
        
        return render(request, 'task_history.html', {'tasks': history, 'id': pk,'filter_form':filter_form})
      return render(request, 'task_history.html', {'tasks': Task.history.all(),'filter_form':filter_form})
  
  @action(detail=True, methods=['get', 'post', 'delete'])
  def task_delete(self, request, pk=None):
    task = get_object_or_404(Task, pk=pk)
    if request.method in ['POST', 'DELETE']:
      task.delete()
      return redirect('task_list')

    return render(request, 'task_delete.html', {'task': task})



  @action(detail=True, methods=['get'])
  def task_detail(self, request, pk=None):
    task = self.get_object()
    return render(request, 'task_detail.html', {'task': task, 'form': TaskForm(instance=task)})

  @action(detail=True, methods=['get', 'post'])
  def task_edit(self, request, pk=None):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
      form = TaskForm(request.POST, instance=task)
      if form.is_valid():
        form.save()
        return redirect('task_detail', pk=pk)
    else:
      form = TaskForm(instance=task)

    return render(request, 'task_edit.html', {'task': task, 'form': form})

class CustomUser:
  class CustomRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'user_register.html'
    success_url = reverse_lazy('user_login')
    
  class CustomLoginView(LoginView):
    template_name = 'user_login.html'
    def get_success_url(self):
      return reverse_lazy('task_list')