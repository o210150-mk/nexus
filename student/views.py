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
from rest_framework.permissions import IsAuthenticated

# class ReactView(APIView):
  
#     serializer_class = ReactSerializer

#     def get(self, request):
#         detail = [ {"name": detail.name,"detail": detail.detail} 
#         for detail in React.objects.all()]
#         return Response(detail)

#     def post(self, request):

#         serializer = ReactSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return  Response(serializer.data)

def is_student(user):
    return user.role == 'STUDENT'

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_student), name='dispatch')
class StudentView(APIView):
    def get(self, request):
        serializer_class = StudentSerializer
        try:
            data = Student.objects.get(gmail = request.user)
            data = serializer_class(data)
            return Response(data.data)
        except:
            return Response({'message':'Invalid role accesss...'})


# @method_decorator(login_required, name='dispatch')
# class StudentView(APIView):
#     def get(self, request):
#         serializer_class = StudentSerializer
#         print(request.user)
#         data = Student.objects.get(gmail = request.user)
#         data = serializer_class(data)
#         return Response(data.data)

class LogView(APIView):
    authentication_classes = [SessionAuthentication]
    def post(self, request):
        serializer = LogSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return Response({'message': 'Login successful','is_authenticated':True,'role':request.user.role,}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials','is_authenticated':False}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid credentials','is_authenticated':False}, status=status.HTTP_401_UNAUTHORIZED)
    def get(self, request):
        print(request.user)
        if request.user.is_authenticated:
            return Response({
                'is_authenticated':True,
                'role':request.user.role,
                'message': 'user logged successfully',
            })
        else:
            return Response({
                'is_authenticated':False,
                'role':'NULL',
                'message': 'user not logged',
            })
        

class outView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        return Response({'Message':'Logged out successfully'})


class uploadView(APIView):
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
        users_to_create = []
            
            # Iterate over the DataFrame rows
        for index, row in df.iterrows():
                # **IMPORTANT:** Match column names exactly from your Excel file
            product = Student_temp(
                    name=row['NAME'], 
                    rollNo = row['ROLL NO'],
                    idNo = row['ID NO'],
                    gender = row['GENDER'],
                    branch = row['BRANCH'],
                    fatherName = row['FATHER NAME'],
                    motherName = row['MOTHER NAME'],
                    studentMobile = row['MOBILE NO'],
                    parentMobile = row['PARENT MOBILE'],
                    address = row['ADDRESS'],
                    gmail = row['GMAIL'],
                    hallTicketNo = row['HALLTICKET NO']
                )
            users_to_create.append(product)


            # 3. Store data in the database using bulk_create (efficient)
        Student_temp.objects.bulk_create(
                users_to_create, 
                ignore_conflicts=True # Skips rows that violate unique constraints (e.g., duplicate SKU)
            )
        data = Student_temp.objects.all()
        serializer_class = StudentTempSerializer
        data = serializer_class(data, many=True)
        return Response(
                {"message": f"Successfully uploaded and stored {len(users_to_create)} records.", 'data':data.data},
                status=status.HTTP_201_CREATED
            )
    
class CreateUsers(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = list(Student_temp.objects.all())
        User = get_user_model() 
        for dat in data:
            gamil = dat.gmail
            Student(name = dat.name, rollNo =dat.rollNo, idNo = dat.idNo, gender = dat.gender, branch = dat.branch,fatherName = dat.fatherName, motherName = dat.motherName, studentMobile = dat.studentMobile, parentMobile = dat.parentMobile, address = dat.address, gmail = dat.gmail, hallTicketNo =dat.hallTicketNo).save()
            dat.delete()
            passsword = 'rgukt123'
            user = User.objects.create_user(
                email = gamil,
                role = 'STUDENT',
                password= passsword 
            )
            user.save()
        return Response({'message':f"Successfully created : User Logins"})
        

