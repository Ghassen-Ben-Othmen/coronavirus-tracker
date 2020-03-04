from rest_framework import serializers, exceptions
from django.contrib import auth
from django.contrib.auth.models import User

class UserSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data['username']
        password = data['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                data['user'] = user
            else:
                raise exceptions.ValidationError('invalid username or password')
        else:
            raise exceptions.ValidationError('invalid username or password')

        return data


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        
        

