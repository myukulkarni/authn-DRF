from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from .utils import generate_otp, verify_otp  # Assuming you have these utility functions

# Register View
class RegisterView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        contact_no = data.get('contact_no')
        gender = data.get('gender')
        date_of_birth = data.get('date_of_birth')
        residential_address = data.get('residential_address')
        city= data.get('city')
        district = data.get('district')
        pincode= data.get('pincode')
        state=data.get('state')
        udf1=data.get('udf1')
        udf2=data.get('udf2')
        udf3=data.get('udf3')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username already exists
        if CustomUser.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the email already exists
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create and save new user
        try:
            user = CustomUser.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                contact_no=contact_no,
                gender=gender,
                date_of_birth=date_of_birth,
                residential_address=residential_address,
                city=city,
                district=district,
                pincode=pincode,
                state=state,
                udf1=udf1,
                udf2=udf2,
                udf3=udf3,
                password=password,
            )

            # Generate and save OTP
            email_otp = generate_otp()
            user.email_otp = email_otp
            user.save()

            # Send email OTP
            send_mail(
                'Email Verification OTP',
                f'Your OTP for email verification is: {email_otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return Response({'success': 'Registration successful!', 'user_id': user.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f'Error during registration: {e}'}, status=status.HTTP_400_BAD_REQUEST)


# OTP Verification View
class VerifyOtpView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract user_id from the request body
        user_id = request.data.get('user_id')
        
        # Check if user exists
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid user.'}, status=status.HTTP_400_BAD_REQUEST)

        email_otp = request.data.get('email_otp')

        # Check if OTP matches
        if email_otp == str(user.email_otp):
            user.is_email_verified = True
            user.email_otp = None  # Clear OTP after successful verification
            user.save()

            # Log the user in after successful OTP verification
            auth_login(request, user)
            return Response({'success': 'OTP verification successful, you are now logged in!'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)

# Login View
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)

            return Response({
                'message': 'Login successful!',
                'refresh': str(refresh),
                'access': access,
            }, status=status.HTTP_200_OK)
        else:
            print("Authentication failed: Invalid credentials.")
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        #     # Check if the user's email is verified
        #     if user.is_verified:
        #         auth_login(request, user)
        #         return Response({'success': 'Logged in successfully!'}, status=status.HTTP_200_OK)
        #     else:
        #         return Response({'success': 'Logged in successfully!'}, status=status.HTTP_200_OK)
        # else:
        #     return Response({'error': 'Invalid username or password.'}, status=status.HTTP_400_BAD_REQUEST)

        

# Logout View
class LogoutView(APIView):
    def post(self, request):
        auth_logout(request)
        return Response({'success': 'You have been logged out.'}, status=status.HTTP_200_OK)


# Dashboard View
class DashboardView(APIView):
    def get(self, request):
        return Response({'message': 'Welcome to the dashboard!'}, status=status.HTTP_200_OK)


# Index View (for homepage)
class IndexView(APIView):
    def get(self, request):
        return Response({'message': 'Welcome to the homepage!'}, status=status.HTTP_200_OK)

