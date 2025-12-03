# myapp/admin.py
from django.contrib import admin
from .models import Student, CustomUser
from faculty.views import Faculty

admin.site.register(Student)
admin.site.register(CustomUser)
