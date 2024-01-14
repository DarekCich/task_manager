from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from tasks.models import Task
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import TaskSerializer
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils import timezone

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=False, methods=['get'])
    def task_list(self, request):
        original_tasks = Task.objects.all()
        tasks = original_tasks

        task_status = request.query_params.get('status')  # Zmieniłem nazwę zmiennej
        nazwa = request.query_params.get('nazwa')
        przypisany_uzytkownik = request.query_params.get('przypisany_uzytkownik')
        sort_by = request.query_params.get('sort_by')

        if task_status:
            tasks = tasks.filter(status=task_status)
        if nazwa:
            tasks = tasks.filter(nazwa__icontains=nazwa)
        if przypisany_uzytkownik:
            tasks = tasks.filter(przypisany_uzytkownik__username__icontains=przypisany_uzytkownik)

        if sort_by:
            tasks = tasks.order_by(sort_by)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  # Używam zmiennej status z modułu rest_framework
