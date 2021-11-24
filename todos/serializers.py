from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    Todo = serializers.ReadOnlyField()
    class Meta:
        model = Todo
        fields = ('id','date', 'title', 'body', 'Todo')