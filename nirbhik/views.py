from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SignupSerializer, SigninSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.save(), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SigninView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request):
        serializer = SigninSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetAllUserTokensView(APIView):
    permission_classes = [IsAuthenticated]  # You can restrict this to staff/admin if necessary

    def get(self, request):
        users_with_tokens = User.objects.filter(has_token=True)
        data = []
        
        for user in users_with_tokens:
            # Generate a new token for each user (you can modify this based on your logic)
            refresh = RefreshToken.for_user(user)
            user_data = {
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            data.append(user_data)

        return Response(data, status=status.HTTP_200_OK)

