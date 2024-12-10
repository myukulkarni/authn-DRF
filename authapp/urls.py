from django.urls import path
from .views import RegisterView, VerifyOtpView, LoginView, LogoutView,UserProfileView, UpdateUserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/<int:user_id>/', VerifyOtpView.as_view(), name='verify-otp'),  # Updated URL
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),  # Fetch user profile
    path('profile/update/', UpdateUserProfileView.as_view(), name='update_user_profile'),  # Update user profile
]