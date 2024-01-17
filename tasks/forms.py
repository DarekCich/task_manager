from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
  class Meta:
    model = Task
    fields = ['nazwa', 'opis', 'przypisany_uzytkownik', 'status']

  def __init__(self, *args, **kwargs):
    super(TaskForm, self).__init__(*args, **kwargs)
    self.fields['nazwa'].required = True
    self.fields['przypisany_uzytkownik'] = forms.ModelChoiceField(
      queryset=User.objects.all(),
      widget=forms.Select(attrs={'class': 'form-control'}),
      required=True,
      initial=''
    )

class RegistrationForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'password1', 'password2']
        
class TaskFilterForm(forms.Form):
  status = forms.ChoiceField(choices=[('', 'Wybierz status')] + Task.STATUS_CHOICES, required=False, initial='')
  nazwa = forms.CharField(required=False)
  przypisany_uzytkownik = forms.CharField(required=False)

  SORT_CHOICES = (
    ('nazwa', 'Nazwa'),
    ('przypisany_uzytkownik', 'Przypisany użytkownik'),
    ('id', 'Id'),
    ('status', 'Status'),
  )
  sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False, initial='')
  
class RegistrationForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'password1', 'password2']
        
class HistoryTaskFilterForm(forms.Form):
  date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    required=False,
    label='Filtruj wg daty'
  )

