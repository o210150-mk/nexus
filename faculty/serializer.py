from rest_framework import serializers
from faculty.models import *

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'
    
class CLasseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassDetails
        fields = '__all__'

class ExcelUploadSerializer(serializers.Serializer):
    excel_file = serializers.FileField()