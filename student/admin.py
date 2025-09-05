# myapp/admin.py
from django.contrib import admin
from .models import Student, CustomUser

admin.site.register(Student)
admin.site.register(CustomUser)