from django.contrib import admin
from django.urls import path
from faculty.views import uploadFaculty, SaveFaculty, facultyAllotment
urlpatterns = [
    path('add-faculty/', uploadFaculty.as_view(), name='add-faculty'),
    path('save-faculty/', SaveFaculty.as_view(), name='save-faculty'),
    path('allot-faculty/', facultyAllotment.as_view(), name='allot-faculty')
]
