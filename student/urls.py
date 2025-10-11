from django.contrib import admin
from django.urls import path
from student.views import StudentView, uploadView, CreateUsers


urlpatterns = [
    path('profile/', StudentView.as_view(), name='std_profile'),
    path('add-users/', uploadView.as_view(), name='add-users'),
    path('save-users/', CreateUsers.as_view(), name = 'save-users')
]
