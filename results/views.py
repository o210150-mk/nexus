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
from student.permissions import IsAdmin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated, AllowAny

class UploadSubjectInfo(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
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
            print(row['CREDITS'])
            item = SubjectInfo(
                    subject_code = row['SUBJECT CODE'], 
                    name = row['NAME'],
                    credits = row['CREDITS'],
                    year = row['YEAR']
                )
            print(item.credits)
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
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = ResultUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        excel_file = serializer.validated_data['excel_file']
        year_sem = serializer.validated_data['year_sem']

        # 1. Map Model
        model_mapping = {
            'E1_S1': ResultE1S1, 'E1_S2': ResultE1S2,
            'E2_S1': ResultE2S1, 'E2_S2': ResultE2S2,
            'E3_S1': ResultE3S1, 'E3_S2': ResultE3S2,
            'E4_S1': ResultE4S1, 'E4_S2': ResultE4S2,
            'PUC1_S1': ResultP1S1, 'PUC1_S2': ResultP1S2,
            'PUC2_S1': ResultP2S1, 'PUC2_S2': ResultP2S2,
        }
        model_class = model_mapping.get(year_sem)
        if not model_class:
            return Response({'message': 'Invalid Year/Sem selection'}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Read Excel
        try:
            df = pd.read_excel(excel_file, sheet_name=0, dtype={'IDNO': str})
            df.columns = df.columns.str.strip() # Remove spaces from headers
        except Exception as e:
            return Response({'message': f'Error reading excel: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        updated_count = 0
        created_count = 0
        errors = []

        # 3. Iterate
        for index, row in df.iterrows():
            try:
                # Clean Keys
                row_id = str(row['IDNO']).strip()
                row_subject = str(row['SUBJECT CODE']).strip()

                student = Student.objects.get(idNo=row_id)
                subject = SubjectInfo.objects.get(subject_code=row_subject)
                excel_yop = row['YOP']

                # --- NEW HELPER FUNCTION ---
                # Converts Pandas "NaN" to Python "None" (Null)
                def clean_val(val):
                    if pd.isna(val) or val == "":
                        return None 
                    return val

                # Prepare Clean Data
                defaults_data = {
                    'mid1': clean_val(row.get('MID1')),
                    'mid2': clean_val(row.get('MID2')),
                    'mid3': clean_val(row.get('MID3')),
                    'WAT': clean_val(row.get('WAT')),
                    'grade': clean_val(row.get('GRADE')),
                }

                # Create or Fetch
                obj, created = model_class.objects.get_or_create(
                    student=student,
                    subject=subject,
                    year_of_pass=excel_yop,
                    defaults=defaults_data
                )

                if created:
                    created_count += 1
                else:
                    # Update Logic
                    has_changes = False
                    fields_to_check = [
                        ('MID1', 'mid1'),
                        ('MID2', 'mid2'),
                        ('MID3', 'mid3'),
                        ('WAT', 'WAT'),
                        ('GRADE', 'grade')
                    ]

                    for excel_col, model_field in fields_to_check:
                        raw_val = row.get(excel_col)
                        
                        # Only update if the new value is NOT NaN/Empty
                        if pd.notna(raw_val) and raw_val != "":
                            current_val = getattr(obj, model_field)
                            # Convert raw_val to correct type if necessary, or rely on Django
                            if current_val != raw_val:
                                setattr(obj, model_field, raw_val)
                                has_changes = True
                    
                    if has_changes:
                        obj.save()
                        updated_count += 1

            except Student.DoesNotExist:
                errors.append(f"Row {index}: Student ID '{row_id}' not found.")
                continue
            except SubjectInfo.DoesNotExist:
                errors.append(f"Row {index}: Subject '{row_subject}' not found.")
                continue
            except Exception as e:
                errors.append(f"Row {index}: Error - {str(e)}")
                continue

        # Return Response
        response_data = {
            "message": f"Process Complete. Created: {created_count}, Updated: {updated_count}",
            "total_processed": len(df)
        }
        if errors:
            response_data["errors"] = errors[:5]

        return Response(response_data, status=status.HTTP_200_OK)