from django.contrib import admin
from django.urls import path
from student.views import *


urlpatterns = [
    path('profile/', StudentView.as_view(), name='std_profile')
]
