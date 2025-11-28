from rest_framework import serializers
from . models import *

class ExcelUploadSerializer(serializers.Serializer):
    excel_file = serializers.FileField()

class ResultUploadSerializer(serializers.Serializer):
    year_sem = serializers.CharField(max_length=10)
    excel_file = serializers.FileField()