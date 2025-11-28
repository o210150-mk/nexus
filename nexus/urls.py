from django.contrib import admin
from django.urls import path, include
from student.views import *
from faculty.views import *
from results.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView, # ADD THIS IMPORT
    TokenRefreshView,    # ADD THIS IMPORT
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/', include('student.urls')),
    path('faculty/', include('faculty.urls')),
    path('logout/', outView.as_view(), name='logout'),
    path('results/', include('results.urls')),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]