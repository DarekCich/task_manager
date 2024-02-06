# serializers.py
from rest_framework import serializers
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from tasks.models import Task

class TaskSerializer(serializers.ModelSerializer):
  przypisany_uzytkownik = serializers.SlugRelatedField(
    slug_field='username',
    queryset=User.objects.all(),
    allow_null=False,
    required=True
  )

  class Meta:
    model = Task
    fields = '__all__'
    extra_kwargs = {
      'nazwa': {'required': True},
      'status': {'choices': [choice[0] for choice in Task.STATUS_CHOICES]},
    }

class TaskHistoryListSerializer(serializers.ModelSerializer):
  history = TaskSerializer(many=True, read_only=True)

  class Meta:
    model = Task
    fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, required=True)
  class Meta:
    model = User
    fields = ['username',  'password']
  
  def create(self, validated_data):
    user = User(username=validated_data['username'])
    user.set_password(validated_data['password'])
    user.save()
    return user