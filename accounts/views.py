from functools import partial
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import generics, serializers
from .models import CustomUser
from .serializers import CustomUserSerializer, ChangePasswordSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.hashers import make_password, check_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, get_user_model

CustomUser = get_user_model()
# Create your views here.
@swagger_auto_schema(methods=['POST'],request_body=LoginSerializer())
@api_view(['POST'])
def login_page(request):
    if request.method == 'POST':
        login_data = LoginSerializer(data=request.data)
        if login_data.is_valid():
            user = authenticate(request, username= login_data.validated_data['username'], password=login_data.validated_data['password'])
            if user:
                if user.is_active:
                    user_serializer =CustomUserSerializer(user)
                    data = {
                        'message': 'Login successful',
                        'data': user_serializer.data
                    }
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    error = {
                        'message':'Please activate your account',
                    }
            
                    return Response(error, status=status.HTTP_401_UNAUTHORIZED) 
            else:
                error = {
                    "error": user_serializer.errors
                }
                return Response(error, status=status.HTTP_401_UNAUTHORIZED)
 





@swagger_auto_schema(methods=['POST'],request_body=CustomUserSerializer())
@api_view(['GET', 'POST'])
def user(request):
    if request.method== 'GET':
        all_users = CustomUser.objects.filter(is_active = True) #get the data
        serializer = CustomUserSerializer(all_users, many=True)

        data = {
            "message": "success",
            "data" : serializer.data
        }
        return Response(data, status = status.HTTP_200_OK)

    elif request.method =='POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            #check if data is valid
            serializer.validated_data['password'] = make_password(serializer.validated_data['password']) #Hash the password

            user = CustomUser.objects.create(**serializer.validated_data)
            user_serializer = CustomUserSerializer(user)

            data = {
                "message" : "success",
                "data" : user_serializer.data
            }
            return Response(data, status = status.HTTP_201_CREATED)
        else:
            error = {
                "message": "failed",
                "error" : serializer.errors
            }
            return Response(error, status = status.HTTP_400_BAD_REQUEST)

# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer



@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=CustomUserSerializer)
@api_view(['GET', 'PUT', 'DELETE'])
def UserDetail(request, user_id):

    try:
        user = CustomUser.objects.get(id=user_id) #get the data from the model
    except CustomUser.DoesNotExist:
        error = {
                "message": "failed",
                "errors" : f"Student with id {user_id} does not exist"
        }
        return Response(error, status = status.HTTP_404_NOT_FOUND)

    if request.method== 'GET':
        serializer =  CustomUserSerializer(user)

        data = {
            "message": "success",
            "data" : serializer.data
        }
        return Response(data, status = status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = CustomUserSerializer(user, data=request.data, partial= True)

        if serializer.is_valid():
            if 'password' in serializer.validated_data.keys():
                raise ValidationError("Unable to change password")

            serializer.save()
            data = {
                "message" : "success",
                "data" : serializer.data
            }
            return Response(data, status = status.HTTP_202_ACCEPTED)
        else:
            error = {
                "message": "failed",
                "error" : serializer.errors
            }
            return Response(error, status = status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response({"message":"success"}, status= status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(methods=['POST'], request_body=ChangePasswordSerializer())
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    # print(user.password)
    if request.method == "POST":
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            if check_password(old_password, user.password):
                
                user.set_password(serializer.validated_data['new_password'])
                
                user.save()
                
                # print(user.password)
                
                return Response({"message":"success"}, status=status.HTTP_200_OK)
            
            else:
                error = {
                'message':'failed',
                "errors":"Old password not correct"
            }
    
            return Response(error, status=status.HTTP_400_BAD_REQUEST) 
            
        else:
            error = {
                'message':'failed',
                "errors":serializer.errors
            }
    
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


