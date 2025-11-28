from rest_framework import serializers
from . models import *
from results.models import ResultE1S1

class LogSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        
class ExcelUploadSerializer(serializers.Serializer):
    excel_file = serializers.FileField()

class SampleSerializer(serializers.Serializer):
    text = serializers.CharField(max_length = 120)

class StudentTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
    

class GetMailSerializer(serializers.Serializer):
    gmail = serializers.EmailField()

class VerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length = 6)

class getPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 15)
    gmail = serializers.EmailField()

class LogSerializer(serializers.Serializer):
    year_sem = serializers.CharField(max_length = 10)

class ResultE3S1Serializer(serializers.ModelSerializer):
    class Meta:
        model = ResultE1S1
        fields = '__all__'