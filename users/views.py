from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib import auth

from .serializers import UserSerializer, RegisterSerializer

# Create your views here.


class LoginAPIView(APIView):
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=200)


class LogoutAPIView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        key = request.headers['Authorization'].split(' ')[1]

        Token.objects.filter(key=key).delete()
        
        return Response({'logout': True}, status=200)


class RegisterAPIView(APIView):
    
    def post(self, request):
        
        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        user = auth.authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        print(user)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token':token.key}, status=201)