from django.shortcuts import render
import random
from django.shortcuts import render
import pandas as pd
from rest_framework.views import APIView
from . models import *
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework.authentication import SessionAuthentication
from . serializer import *
from rest_framework import status
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.

class uploadFaculty(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # serializer_class = ExcelUploadSerializer
        # serializer = serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)

        # excel_file = serializer.validated_data['excel_file']

        serializer = ExcelUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        excel_file = serializer.validated_data['excel_file']


            # 1. Read the Excel file into a pandas DataFrame
            # The uploaded file is in memory, so we pass it directly.
            # Assuming the first sheet has the data and the first row is the header.
        df = pd.read_excel(excel_file, sheet_name=0) 

            # 2. Prepare data for bulk creation
        faculty_to_create = []
            
            # Iterate over the DataFrame rows
        for index, row in df.iterrows():
                # **IMPORTANT:** Match column names exactly from your Excel file
            item = Faculty(
                    name=row['NAME'], 
                    gender = row['GENDER'],
                    mail_id = row['GMAIL'],
                    qualification = row['QUALIFICATION'],
                    designation = row['DESIGNATION'],
                    experience = row['EXPERIENCE']
                )
            faculty_to_create.append(item)

            # 3. Store data in the database using bulk_create (efficient)
        Faculty.objects.bulk_create(
                faculty_to_create, 
                ignore_conflicts=True # Skips rows that violate unique constraints (e.g., duplicate SKU)
            )
        data = Faculty.objects.filter(verified = False)
        data = FacultySerializer(data, many=True)
        return Response(
                {"message": f"Successfully uploaded {len(faculty_to_create)} records.", 'data':data.data},
                status=status.HTTP_201_CREATED
            )

class SaveFaculty(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = Faculty.objects.filter(verified = False)
        User = get_user_model() 
        for item in data:
            gmail = item.mail_id
            passsword = 'faculty123'
            user = User.objects.create_user(
                email = gmail,
                role = 'FACULTY',
                password= passsword 
            )
            user.save()
            item.verified = True
            item.save()
        return Response(
            {'message':'Successfully Stored in database...'},
            status=status.HTTP_201_CREATED
        )
    
class facultyAllotment(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # serializer_class = ExcelUploadSerializer
        # serializer = serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)

        # excel_file = serializer.validated_data['excel_file']

        serializer = ExcelUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        excel_file = serializer.validated_data['excel_file']


            # 1. Read the Excel file into a pandas DataFrame
            # The uploaded file is in memory, so we pass it directly.
            # Assuming the first sheet has the data and the first row is the header.
        df = pd.read_excel(excel_file, sheet_name=0) 

            # 2. Prepare data for bulk creation
        class_details = []
            # Iterate over the DataFrame rows
        for index, row in df.iterrows():
                # **IMPORTANT:** Match column names exactly from your Excel file
            faculty = row['FACULTY']
            faculty_instance = Faculty.objects.get(mail_id = faculty)
            item = ClassDetails(
                    year =row['YEAR'], 
                    sem = row['SEM'],
                    class_name = row['CLASS'],
                    faculty = faculty_instance
                )
            
            class_details.append(item)

            # 3. Store data in the database using bulk_create (efficient)
        ClassDetails.objects.bulk_create(
                class_details, 
                ignore_conflicts=True # Skips rows that violate unique constraints (e.g., duplicate SKU)
            )
        data = ClassDetails.objects.all()
        data = CLasseDetailsSerializer(data, many=True)
        return Response(
                {"message": f"Successfully Saved {len(class_details)} records.", 'data':data.data},
                status=status.HTTP_201_CREATED
            )

