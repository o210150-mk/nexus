# myapp/admin.py
from django.contrib import admin
from .models import Student, CustomUser, Student_temp

admin.site.register(Student)
admin.site.register(CustomUser)
admin.site.register(Student_temp)