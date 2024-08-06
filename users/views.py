import random

from django.contrib.auth import authenticate
from django.core.cache import cache
from django.conf import settings
from django.core.mail import send_mail

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


from .serializers import CustomUserSerializer, RegisterSerializer, UserProfileSerializer
from .models import CustomUser, UserProfile


def send_verification_code(email, code):
    subject = 'Your Verification Code'
    message = f'Your verification code is: {code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)

class RegisterView(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({'detail': 'Registered successfully!'})


class LoginView(APIView):

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        if not username or not password:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)
            
        email = user.email

        code = random.randint(10000, 99999)
        cache.set(str(username), code)

        try:
            send_verification_code(email, code)
        except Exception:
            return Response({'error': 'Something went wrong'})

        return Response({'detail': f'Code sent to {email}',
                         'code': code})
    

class TokenGeneratorView(APIView):

    def post(self, request):
        username = request.data['username']
        code = request.data['code']

        cached_code = cache.get(username)

        if cached_code is None:
            return Response({"error": "Verification code expired or invalid."}, status=status.HTTP_400_BAD_REQUEST)
        
        if cached_code != int(code):
            return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        rf = RefreshToken.for_user(user)
        access_token = str(rf.access_token)
        refresh_token = str(rf)

        cache.delete(username)

        return Response({
            'detail': 'Login successful',
            'access': access_token, 'refresh': refresh_token}, 
            status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = CustomUser.objects.get(username=username)
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, username):
        try:
            user = CustomUser.objects.get(username=username)
            serializer = CustomUserSerializer(user, request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = CustomUser.objects.get(username=username)
            profile = UserProfile.objects.get(user=user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, username):
        try:
            user = CustomUser.objects.get(username=username)
            profile = UserProfile.objects.get(user=user)

            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
