import django_filters
from tasks.models import Task

class TaskFilter(django_filters.FilterSet):
  nazwa = django_filters.CharFilter(lookup_expr='icontains')
  opis  = django_filters.CharFilter(lookup_expr='icontains')
  przypisany_uzytkownik = django_filters.CharFilter(field_name='przypisany_uzytkownik__username')
  status = django_filters.CharFilter()

  class Meta:
    model = Task
    fields = ['nazwa','opis','przypisany_uzytkownik','status']