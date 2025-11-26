from django.contrib import admin
from django.urls import path
from student.views import StudentView, uploadView, CreateUsers, GetMail, VerifyOtp, UpdatePassword, ResendMail

urlpatterns = [
    path('profile/', StudentView.as_view(), name='std_profile'),
    path('add-users/', uploadView.as_view(), name='add-users'),
    path('save-users/', CreateUsers.as_view(), name = 'save-users'),
    path('get-mail/', GetMail.as_view(), name='get-mail'),
    path('verify-otp/', VerifyOtp.as_view(), name='verify-otp'),
    path('reset-password/', UpdatePassword.as_view(), name='reset-password'),
    path('resend-otp/', ResendMail.as_view(), name='resend-otp'),
]
