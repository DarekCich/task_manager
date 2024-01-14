from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Task(models.Model):
  STATUS_CHOICES = [
    ('Nowy', 'Nowy'),
    ('W toku', 'W toku'),
    ('Rozwiązany', 'Rozwiązany'),
  ]

  id = models.AutoField(primary_key=True)
  nazwa = models.CharField(max_length=255)
  opis = models.TextField(blank=True, null=True)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Nowy')
  przypisany_uzytkownik = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
  history = HistoricalRecords()
  def __str__(self):
    return f"{self.id} - {self.nazwa}"
