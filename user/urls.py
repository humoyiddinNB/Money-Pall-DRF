from django.urls import path
from .views import UserDetailView, UserListView, RegisterView, LoginView, OTPVerifyAPIView, LogOut, ProfileUpdateAPIView, \
    DeleteAccountAPIView

urlpatterns = [
    path('list/', UserListView.as_view(), name='user_list'),
    path('user_detail/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='api-login'),
    path('otp_verify', OTPVerifyAPIView.as_view(), name='otp_verify'),
    path('logout', LogOut.as_view(), name='logout'),
    path('update', ProfileUpdateAPIView.as_view(), name='update'),
    path('delete', DeleteAccountAPIView.as_view(), name='delete'),

]