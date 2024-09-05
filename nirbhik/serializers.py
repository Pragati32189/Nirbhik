from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile_no', 'address']

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'mobile_no', 'address', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        refresh = RefreshToken.for_user(user)
         # Mark that the user has a token now
        user.has_token = True
        user.save()
        
        return {
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            # Check if the user already has a token
            if user.has_token:
                raise serializers.ValidationError("User already has a token.")
            
            # Generate tokens only if the user doesn't have a token
            refresh = RefreshToken.for_user(user)

            # Update the user to mark that they now have a token
            user.has_token = True
            user.save()

            return {
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        raise serializers.ValidationError("Invalid credentials")
