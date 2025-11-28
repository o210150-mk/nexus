from django.contrib import admin
from django.urls import path
from .views import UploadSubjectInfo, UploadResult

urlpatterns = [
    path('subjectInfo/', UploadSubjectInfo.as_view(), name='subjectInfo'),
    path('result/', UploadResult.as_view(), name='Result')
]