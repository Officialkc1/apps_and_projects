from django.shortcuts import render
from rest_framework import generics
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes


# Create your views here.
# @swagger_auto_schema(methods=['POST'],request_body=TodoSerializer())
# @api_view(['GET', 'POST'])
class ListTodo(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    


class UpdateTodo(generics.UpdateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

class DetailTodo(generics.DestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer