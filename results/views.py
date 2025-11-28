from django.shortcuts import render
import random
from django.shortcuts import render
import pandas as pd
from rest_framework.views import APIView
from . models import *
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework.authentication import SessionAuthentication
from student.serializer import *
from results.serializer import *
from rest_framework import status
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated, AllowAny

class UploadSubjectInfo(APIView):
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
        subjects_to_add = []
            
            # Iterate over the DataFrame rows
        for index, row in df.iterrows():
                # **IMPORTANT:** Match column names exactly from your Excel file
            item = SubjectInfo(
                    subject_code = row['SUBJECT CODE'], 
                    name = row['NAME'],
                    credits = row['CREDITS'],
                    year = row['YEAR']
                )
            subjects_to_add.append(item)

            # 3. Store data in the database using bulk_create (efficient)
        SubjectInfo.objects.bulk_create(
                subjects_to_add, 
                ignore_conflicts=True # Skips rows that violate unique constraints (e.g., duplicate SKU)
            )

        return Response(
                {"message": f"Successfully uploaded {len(subjects_to_add)} records."},
                status=status.HTTP_201_CREATED
            )


class UploadResult(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # serializer_class = ExcelUploadSerializer
        # serializer = serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)

        # excel_file = serializer.validated_data['excel_file']

        serializer = ResultUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        excel_file = serializer.validated_data['excel_file']
        year_sem = serializer.validated_data['year_sem']
        file_name = excel_file.name


            # 1. Read the Excel file into a pandas DataFrame
            # The uploaded file is in memory, so we pass it directly.
            # Assuming the first sheet has the data and the first row is the header.
        df = pd.read_excel(excel_file, sheet_name=0) 

            # 2. Prepare data for bulk creation
            # Iterate over the DataFrame rows

        if year_sem == 'E1_S1':
            results_uploaded = []
            for index, row in df.iterrows():
                                # **IMPORTANT:** Match column names exactly from your Excel file
                student = Student.objects.get(idNo = row['IDNO'])
                subject = SubjectInfo.objects.get(subject_code = row['SUBJECT CODE'])
                item = ResultE1S1(
                    student = student, 
                    subject = subject,
                    mid1 = row['MID1'],
                    mid2 = row['MID2'],
                    mid3 = row['MID3'],
                    WAT = row['WAT'],
                    grade = row['GRADE'],
                    year_of_pass = row['YOP']
                )
                results_uploaded.append(item)
            # Store data in the database using bulk_create (efficient)
            ResultE1S1.objects.bulk_create(
            results_uploaded,
            ignore_conflicts=True # Skips rows that violate unique constraints (e.g., duplicate SKU)
        )
        elif year_sem == 'E1_S2':
            results_uploaded = []
            for index, row in df.iterrows():
                                # **IMPORTANT:** Match column names exactly from your Excel file
                student = Student.objects.get(idNo = row['IDNO'])
                subject = SubjectInfo.objects.get(subject_code = row['SUBJECT CODE'])
                item = ResultE1S2(
                    student = student, 
                    subject = subject,
                    mid1 = row['MID1'],
                    mid2 = row['MID2'],
                    mid3 = row['MID3'],
                    WAT = row['WAT'],
                    grade = row['GRADE'],
                    year_of_pass = row['YOP']
                )
                results_uploaded.append(item)
            # Store data in the database using bulk_create (efficient)
            ResultE1S2.objects.bulk_create(
            results_uploaded,
            ignore_conflicts=True # Skips rows that violate unique constraints (e.g., duplicate SKU)
        )
        
        elif year_sem == 'E2_S1':
            results_uploaded = []
            for index, row in df.iterrows():
                                # **IMPORTANT:** Match column names exactly from your Excel file
                student = Student.objects.get(idNo = row['IDNO'])
                subject = SubjectInfo.objects.get(subject_code = row['SUBJECT CODE'])
                item = ResultE2S1(
                    student = student, 
                    subject = subject,
                    mid1 = row['MID1'],
                    mid2 = row['MID2'],
                    mid3 = row['MID3'],
                    WAT = row['WAT'],
                    grade = row['GRADE'],
                    year_of_pass = row['YOP']
                )
                results_uploaded.append(item)
            # Store data in the database using bulk_create (efficient)
            ResultE2S1.objects.bulk_create(
            results_uploaded,
            ignore_conflicts=True # Skips rows that violate unique constraints (e.g., duplicate SKU)
        )
        elif year_sem == 'E2_S2':
            results_uploaded = []
            for index, row in df.iterrows():
                                # **IMPORTANT:** Match column names exactly from your Excel file
                student = Student.objects.get(idNo = row['IDNO'])
                subject = SubjectInfo.objects.get(subject_code = row['SUBJECT CODE'])
                item = ResultE2S2(
                    student = student, 
                    subject = subject,
                    mid1 = row['MID1'],
                    mid2 = row['MID2'],
                    mid3 = row['MID3'],
                    WAT = row['WAT'],
                    grade = row['GRADE'],
                    year_of_pass = row['YOP']
                )
                results_uploaded.append(item)
            # Store data in the database using bulk_create (efficient)
            ResultE2S2.objects.bulk_create(
            results_uploaded,
            ignore_conflicts=True # Skips rows that violate unique constraints (e.g., duplicate SKU)
        )
        elif year_sem == 'E3_S1':
            results_uploaded = []
            for index, row in df.iterrows():
                                # **IMPORTANT:** Match column names exactly from your Excel file
                student = Student.objects.get(idNo = row['IDNO'])
                subject = SubjectInfo.objects.get(subject_code = row['SUBJECT CODE'])
                item = ResultE3S1(
                    student = student, 
                    subject = subject,
                    mid1 = row['MID1'],
                    mid2 = row['MID2'],
                    mid3 = row['MID3'],
                    WAT = row['WAT'],
                    grade = row['GRADE'],
                    year_of_pass = row['YOP']
                )
                results_uploaded.append(item)
            # Store data in the database using bulk_create (efficient)
            ResultE3S1.objects.bulk_create(
            results_uploaded,
            ignore_conflicts=True # Skips rows that violate unique constraints (e.g., duplicate SKU)
        )
        elif year_sem == 'E3_S2':
            results_uploaded = []
            for index, row in df.iterrows():
                                # **IMPORTANT:** Match column names exactly from your Excel file
                student = Student.objects.get(idNo = row['IDNO'])
                subject = SubjectInfo.objects.get(subject_code = row['SUBJECT CODE'])
                item = ResultE3S2(
                    student = student, 
                    subject = subject,
                    mid1 = row['MID1'],
                    mid2 = row['MID2'],
                    mid3 = row['MID3'],
                    WAT = row['WAT'],
                    grade = row['GRADE'],
                    year_of_pass = row['YOP']
                )
                results_uploaded.append(item)
            # Store data in the database using bulk_create (efficient)
            ResultE3S2.objects.bulk_create(
            results_uploaded,
            ignore_conflicts=True # Skips rows that violate unique constraints (e.g., duplicate SKU)
        )
        elif year_sem == 'E4_S1':
            results_uploaded = []
            for index, row in df.iterrows():
                                # **IMPORTANT:** Match column names exactly from your Excel file
                student = Student.objects.get(idNo = row['IDNO'])
                subject = SubjectInfo.objects.get(subject_code = row['SUBJECT CODE'])
                item = ResultE4S1(
                    student = student, 
                    subject = subject,
                    mid1 = row['MID1'],
                    mid2 = row['MID2'],
                    mid3 = row['MID3'],
                    WAT = row['WAT'],
                    grade = row['GRADE'],
                    year_of_pass = row['YOP']
                )
                results_uploaded.append(item)
            # Store data in the database using bulk_create (efficient)
            ResultE4S1.objects.bulk_create(
            results_uploaded,
            ignore_conflicts=True # Skips rows that violate unique constraints (e.g., duplicate SKU)
        )
        elif year_sem == 'E4_S2':
            results_uploaded = []
            for index, row in df.iterrows():
                                # **IMPORTANT:** Match column names exactly from your Excel file
                student = Student.objects.get(idNo = row['IDNO'])
                subject = SubjectInfo.objects.get(subject_code = row['SUBJECT CODE'])
                item = ResultE4S2(
                    student = student, 
                    subject = subject,
                    mid1 = row['MID1'],
                    mid2 = row['MID2'],
                    mid3 = row['MID3'],
                    WAT = row['WAT'],
                    grade = row['GRADE'],
                    year_of_pass = row['YOP']
                )
                results_uploaded.append(item)
            # Store data in the database using bulk_create (efficient)
            ResultE4S2.objects.bulk_create(
            results_uploaded,
            ignore_conflicts=True # Skips rows that violate unique constraints (e.g., duplicate SKU)
        )
        elif year_sem == 'PUC1_S1':
            results_uploaded = []
            for index, row in df.iterrows():
                                # **IMPORTANT:** Match column names exactly from your Excel file
                student = Student.objects.get(idNo = row['IDNO'])
                subject = SubjectInfo.objects.get(subject_code = row['SUBJECT CODE'])
                item = ResultP1S1(
                    student = student, 
                    subject = subject,
                    mid1 = row['MID1'],
                    mid2 = row['MID2'],
                    mid3 = row['MID3'],
                    WAT = row['WAT'],
                    grade = row['GRADE'],
                    year_of_pass = row['YOP']
                )
                results_uploaded.append(item)
            # Store data in the database using bulk_create (efficient)
            ResultP1S1.objects.bulk_create(
            results_uploaded,
            ignore_conflicts=True # Skips rows that violate unique constraints (e.g., duplicate SKU)
        )
        elif year_sem == 'PUC1_S2':
            results_uploaded = []
            for index, row in df.iterrows():
                                # **IMPORTANT:** Match column names exactly from your Excel file
                student = Student.objects.get(idNo = row['IDNO'])
                subject = SubjectInfo.objects.get(subject_code = row['SUBJECT CODE'])
                item = ResultP1S2(
                    student = student, 
                    subject = subject,
                    mid1 = row['MID1'],
                    mid2 = row['MID2'],
                    mid3 = row['MID3'],
                    WAT = row['WAT'],
                    grade = row['GRADE'],
                    year_of_pass = row['YOP']
                )
                results_uploaded.append(item)
            # Store data in the database using bulk_create (efficient)
            ResultP1S2.objects.bulk_create(
            results_uploaded,
            ignore_conflicts=True # Skips rows that violate unique constraints (e.g., duplicate SKU)
        )
        elif year_sem == 'PUC2_S1':
            results_uploaded = []
            for index, row in df.iterrows():
                                # **IMPORTANT:** Match column names exactly from your Excel file
                student = Student.objects.get(idNo = row['IDNO'])
                subject = SubjectInfo.objects.get(subject_code = row['SUBJECT CODE'])
                item = ResultP2S1(
                    student = student, 
                    subject = subject,
                    mid1 = row['MID1'],
                    mid2 = row['MID2'],
                    mid3 = row['MID3'],
                    WAT = row['WAT'],
                    grade = row['GRADE'],
                    year_of_pass = row['YOP']
                )
                results_uploaded.append(item)
            # Store data in the database using bulk_create (efficient)
            ResultP2S1.objects.bulk_create(
            results_uploaded,
            ignore_conflicts=True # Skips rows that violate unique constraints (e.g., duplicate SKU)
        )
        elif year_sem == 'PUC2_S2':
            results_uploaded = []
            for index, row in df.iterrows():
                                # **IMPORTANT:** Match column names exactly from your Excel file
                student = Student.objects.get(idNo = row['IDNO'])
                subject = SubjectInfo.objects.get(subject_code = row['SUBJECT CODE'])
                item = ResultP2S2(
                    student = student, 
                    subject = subject,
                    mid1 = row['MID1'],
                    mid2 = row['MID2'],
                    mid3 = row['MID3'],
                    WAT = row['WAT'],
                    grade = row['GRADE'],
                    year_of_pass = row['YOP']
                )
                results_uploaded.append(item)
            # Store data in the database using bulk_create (efficient)
            ResultP2S2.objects.bulk_create(
            results_uploaded,
            ignore_conflicts=True # Skips rows that violate unique constraints (e.g., duplicate SKU)
        )
        else:
            return Response({'message':'error'}, status= status.HTTP_204_NO_CONTENT)
        
        return Response(
                {"message": f"Successfully uploaded {len(results_uploaded)} records."},
                status=status.HTTP_201_CREATED
            )
