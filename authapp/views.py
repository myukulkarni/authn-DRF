from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from django.utils.crypto import get_random_string


# Utility function to generate OTP
def generate_otp():
    return get_random_string(length=6, allowed_chars="0123456789")


# Register View
class RegisterView(APIView):
    def post(self, request):
        data = request.data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        contact_no = data.get("contact_no")
        residential_address = data.get("residential_address")
        pincode = data.get("pincode")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        username = data.get("username")  # Optional username field

        # Validate passwords
        if password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if username already exists
        if username and CustomUser.objects.filter(username=username).exists():
            return Response({"error": "Username is already taken."}, status=status.HTTP_400_BAD_REQUEST)

        # Generate unique username if not provided
        if not username:
            username = email.split("@")[0] + get_random_string(length=4)

        # Generate OTP and send it to the email
        otp = generate_otp()

        # Temporarily store user data with OTP
        user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            contact_no=contact_no,
            residential_address=residential_address,
            pincode=pincode,
            email_otp=otp,
            is_verified=False,
        )
        user.set_password(password)  # Hash password

        try:
            send_mail(
                subject="Email Verification OTP",
                message=f"Your OTP is: {otp}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )
            user.save()  # Save only with OTP and unverified status
            return Response({"success": "OTP sent to your email.", "user_id": user.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Failed to send OTP: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Verify OTP View
class VerifyOtpView(APIView):
    def post(self, request, user_id):  # Accepting user_id from URL
        otp = request.data.get("otp")

        try:
            # Find the user by id and OTP
            user = CustomUser.objects.get(id=user_id, email_otp=otp)

            # Mark the user as verified and clear OTP
            user.is_verified = True
            user.email_otp = None  # Clear OTP after successful verification
            user.save()

            return Response({"success": "Email verified successfully!"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid user ID or OTP."}, status=status.HTTP_400_BAD_REQUEST)


# Login View
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser  # Adjust according to your project structure

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = CustomUser.objects.get(username=username)

            if not user.is_verified:
                return Response({"error": "Email not verified."}, status=status.HTTP_400_BAD_REQUEST)

            if authenticate(username=username, password=password):
                # Generate tokens
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token

                return Response({
                    "message": "Login successful!",
                    "refresh": str(refresh),
                    "access": str(access),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)




from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import CustomUser  # Adjust according to your project structure

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user

            # Fetch user's profile data
            profile_data = {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "contact_no": getattr(user, "contact_no", None),
                "residential_address": getattr(user, "residential_address", None),
                "pincode": getattr(user, "pincode", None),
            }

            return Response(profile_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Failed to fetch user profile"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateUserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    # Update the current user's profile
    def put(self, request):
        user = request.user
        data = request.data

        # Update user fields
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.email = data.get("email", user.email)
        user.contact_no = data.get("contact_no", user.contact_no)
        user.residential_address = data.get("residential_address", user.residential_address)
        user.pincode = data.get("pincode", user.pincode)

        # Save the updated user data
        user.save()

        return Response({"message": "Profile updated successfully!"}, status=status.HTTP_200_OK)

from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Blacklist the refresh token
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            return Response({"success": "Logged out successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
