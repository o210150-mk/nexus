from django.contrib import admin
from django.urls import path, include
from student.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('log/', LogView.as_view(), name="log"),
    path('student/', include('student.urls')),
    path('logout/', outView.as_view(), name='logout')
]