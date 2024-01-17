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
    
    def update(self, instance, validated_data):
      instance.przypisany_uzytkownik = validated_data.get('przypisany_uzytkownik', instance.przypisany_uzytkownik)
      instance.nazwa = validated_data.get('nazwa', instance.nazwa)
      instance.status = validated_data.get('status', instance.status)
      instance.opis = validated_data.get('opis', instance.opis)
      instance.save()
      return instance

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
    user = User.objects.create_user(
      username=validated_data['username'],
      password=validated_data['password']
    )
    return user