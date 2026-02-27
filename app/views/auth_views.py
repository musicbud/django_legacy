from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from app.forms.registeration import LoginForm, RegistrationForm
from django.contrib.auth.models import User
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import logging
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from app.middlewares.async_jwt_authentication import AsyncJWTAuthentication

logger = logging.getLogger('app')

@method_decorator(csrf_exempt, name='dispatch')
class AuthLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        content_type = request.content_type.lower()

        if content_type == 'application/json':
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        elif content_type == 'application/x-www-form-urlencoded':
            username = request.POST.get('username')
            password = request.POST.get('password')
        else:
            return Response({
                "success": False,
                "message": "Unsupported content type"
            }, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        if not username or not password:
            return Response({
                "success": False,
                "message": "Both username and password are required"
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "success": True,
                "message": "Login successful",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "message": "Invalid credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)

@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                if User.objects.filter(username=username).exists():
                    return render(request, 'register.html', {'form': form, 'error': 'Username already exists'})
                
                if User.objects.filter(email=email).exists():
                    return render(request, 'register.html', {'form': form, 'error': 'Email already exists'})
                
                user = User.objects.create_user(username=username, email=email, password=password)
                logger.info(f"New user registered: {username}")
                return redirect('login')
            except Exception as e:
                logger.exception(f"Error during user registration for username {username}: {e}")
                return render(request, 'register.html', {'form': form, 'error': 'An unexpected error occurred during registration. Please try again.'})
        else:
            logger.error(f"Registration form validation failed. Errors: {form.errors}")
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

@method_decorator(csrf_exempt, name='dispatch')
class Logout(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)



@method_decorator(csrf_exempt, name='dispatch')
class RefreshTokenView(APIView):
    def post(self, request):
        try:
            content_type = request.content_type.lower()

            if content_type == 'application/json':
                refresh_token = request.data.get('refresh_token') or request.data.get('refresh')
            elif content_type == 'application/x-www-form-urlencoded':
                refresh_token = request.POST.get('refresh_token') or request.POST.get('refresh')
            else:
                return Response({
                    'success': False,
                    'message': 'Unsupported content type'
                }, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

            if not refresh_token:
                return Response({
                    'success': False,
                    'message': 'Refresh token is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            return Response({
                'success': True,
                'message': 'Token refresh successful',
                'access_token': access_token
            })
        except TokenError:
            return Response({
                'success': False,
                'message': 'Invalid or expired refresh token'
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.exception(f"An unexpected error occurred during token refresh: {e}")
            return Response({
                'success': False,
                'message': 'An internal server error occurred.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_likes(request):
    service = request.data.get('service')
    if not service:
        return Response({
            'success': False,
            'message': 'Service parameter is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = request.user
        
        # Example: Update user's preferred service
        # Assuming user.profile exists and is a related object with a 'preferred_service' field
        if hasattr(user, 'profile') and user.profile:
            user.profile.preferred_service = service
            user.profile.save()
            return Response({
                'success': True,
                'message': f'Likes updated for service: {service}'
            }, status=status.HTTP_200_OK)
        else:
            logger.error(f"User {user.username} does not have a profile object.")
            return Response({
                'success': False,
                'message': 'User profile not found.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        logger.exception(f"An unexpected error occurred while updating likes for user {request.user.username}: {e}")
        return Response({
            'success': False,
            'message': 'An internal server error occurred.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
