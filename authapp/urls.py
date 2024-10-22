from django.urls import path
from .views import RegisterView, VerifyOtpView, LoginView, LogoutView, DashboardView, IndexView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # User registration
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),  # OTP verification
    path('login/', LoginView.as_view(), name='login'),  # User login
    path('logout/', LogoutView.as_view(), name='logout'),  # User logout
    path('dashboard/', DashboardView.as_view(), name='dashboard'),  # Dashboard view
    path('', IndexView.as_view(), name='index'),  # Homepage view
]
