import random
from django.shortcuts import render
import pandas as pd
from rest_framework.views import APIView
from . models import *
from results.models import *
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework.authentication import SessionAuthentication
from . serializer import *
from rest_framework import status
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsStudent, IsAdmin
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import CustomTokenObtainPairSerializer

def is_student(user):
    return user.role == 'STUDENT'


class StudentView(APIView):
    # This automatically enforces JWT validation and populates request.user
    permission_classes = [IsAuthenticated, IsStudent] 
    def get(self, request):
        # 1. ENFORCE ROLE CHECK
        if request.user.role != 'STUDENT':
            return Response(
                {'message': 'Access Denied: Only Students can view this data.'},
                status=status.HTTP_403_FORBIDDEN # Use 403 Forbidden for insufficient permissions
            )
        
        # 2. GET DATA
        serializer_class = StudentSerializer
        try:
            # request.user is available thanks to JWTAuthentication
            data = Student.objects.get(gmail=request.user.email) 
            data = serializer_class(data)
            return Response(data.data)
        except Student.DoesNotExist:
            return Response(
                {'message': 'Student record not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
             # Catching a generic exception is often bad, but for unknown issues, 
             # return a generic error or log it.
             return Response(
                {'message': 'An unexpected error occurred.'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
             )



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class outView(APIView):
    # This view automatically checks the JWT header thanks to settings.py
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        try:
            # Get the Refresh Token from the request body (client must send it)
            refresh_token = request.data["refresh"] 
            token = RefreshToken(refresh_token)
            token.blacklist() # Blacklist the token, revoking its ability to refresh

            return Response({'Message':'Logged out and token blacklisted successfully'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            # Handle cases where the token is invalid or missing
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class uploadView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    def post(self, request):

        serializer = ExcelUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        excel_file = serializer.validated_data['excel_file']
        # 1. Read Excel file into a DataFrame
        df = pd.read_excel(excel_file, sheet_name=0) 

            # 2. Prepare data for bulk creation
        users_to_create = []
            
            # Iterate over the DataFrame rows
        for index, row in df.iterrows():
                # **IMPORTANT:** Match column names exactly from your Excel file
            
            product = Student(
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
                    hallTicketNo = row['HALLTICKET NO'],
                    section = row['SECTION'],
                    guardian = row['GUARDIAN'],
                    dob = row['DATE OF BIRTH'],
                    hostelName = row['HOSTEL NAME'],
                    roomNo = row['ROOM NO'],
                    batch = str(row['ID NO'])[:3],
                    bloodGroup = row['BLOOD GROUP'],
                    verified = False
                )
            users_to_create.append(product)

            # 3. Store data in the database using bulk_create (efficient)
        Student.objects.bulk_create(
                users_to_create, 
                ignore_conflicts=True # Skips rows that violate unique constraints (e.g., duplicate SKU)
            )
        data = Student.objects.filter(verified = False)
        serializer_class = StudentSerializer
        data = serializer_class(data, many=True)
        print(data.data)
        return Response(
                {"message": f"Successfully uploaded and stored {len(users_to_create)} records.", 'data':data.data},
                status=status.HTTP_201_CREATED
            )
    
class CreateUsers(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    def post(self, request):
        data = list(Student.objects.filter(verified = False))[:10]
        User = get_user_model() 
        for dat in data:
            gamil = dat.gmail
            dat.verified = True
            dat.save()
            passsword = 'rgukt123'
            user = User.objects.create_user(
                email = gamil,
                role = 'STUDENT',
                password= passsword 
            )
            user.save()
        return Response({'message':f"Successfully created : User Logins"})
    
    
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string 
from django.conf import settings
from django.utils.html import strip_tags
from django.core.mail import send_mail
# In your views.py
# In your views.py

# Import the new function
from .task import send_otp_email_async 
# ... other imports

class GetMail(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer_class = GetMailSerializer(data = request.data)
        
        if serializer_class.is_valid():
            gmail = serializer_class.validated_data['gmail']
            
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            request.session['mail'] = gmail
            request.session.save()
            
            # CALL THE THREADED FUNCTION (Immediately returns)
            send_otp_email_async(gmail, otp) 
            
            # IMMEDIATE RESPONSE
            return Response({'message':'Mail sent successfully...'})
        
        return Response({'message':'Error...'}, status=status.HTTP_400_BAD_REQUEST)

# Apply the same change to the ResendMail view.
class ResendMail(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer_class = GetMailSerializer(data=request.data)
        
        if serializer_class.is_valid():
            gmail = request.session['mail']
            
            # --- 1. Generate New OTP ---
            otp = random.randint(100000, 999999)
            
            # --- 2. Save New OTP to Session ---
            # This replaces the old OTP in the session
            request.session['otp'] = str(otp) # Store as string for easy comparison later
            request.session.save()
            
            # --- 3. Trigger Asynchronous Email Send ---
            # This function uses threading to send the mail in the background, 
            # allowing the API call to return immediately.
            send_otp_email_async(gmail, otp)
            
            return Response({'message': 'New OTP mail sent successfully...'})
        
        # If serializer validation fails
        return Response(
            {'message': 'Error validating input.', 'errors': serializer_class.errors},
            status=status.HTTP_400_BAD_REQUEST
        )    
class VerifyOtp(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer_class = VerifySerializer(data = request.data)
        if serializer_class.is_valid():
            otp = serializer_class.validated_data['otp']
            if otp == str(request.session['otp']):
                return Response({'message':'Successfully Verified'})
            else:
                return Response(
                {"detail": "Invalid OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )

class UpdatePassword(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        serializer_class = getPasswordSerializer(data = request.data)
        if serializer_class.is_valid():
                password = serializer_class.validated_data['password']
                print(password)
                user = CustomUser.objects.get(email=request.session['mail'])
                user.set_password(password)
                user.save()
                print(request.session['otp'], " ",request.session['mail'])
                del request.session['otp']
                del request.session['mail']
                return Response({'message':'password changed successfully...'})
        else:
                print('Error')


class GetResults(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    def get(self, request):
        year_sem = request.GET.get('year_sem')
        result = []
        data = []
        student_idno = str(request.user).split('@')[0]
        student = Student.objects.get(idNo = student_idno)
        if year_sem == 'E1_S1':
                data = ResultE1S1.objects.filter(student = student)
        elif year_sem == 'E1_S2':
                data = ResultE1S2.objects.filter(student = student)
        elif year_sem == 'E2_S1':
                data = ResultE2S1.objects.filter(student = student)
        elif year_sem == 'E2_S2':
                data = ResultE2S2.objects.filter(student = student)
        elif year_sem == 'E3_S1':
                data = ResultE3S1.objects.filter(student = student)
        elif year_sem == 'E3_S2':
                data = ResultE3S2.objects.filter(student = student)
        elif year_sem == 'E4_S1':
                data = ResultE4S1.objects.filter(student = student)
        elif year_sem == 'E4_S2':
                data = ResultE4S2.objects.filter(student = student)
        elif year_sem == 'PUC1_S1':
                data = ResultP1S1.objects.filter(student = student)
        elif year_sem == 'PUC1_S2':
                data = ResultP1S2.objects.filter(student = student)
        elif year_sem == 'PUC2_S1':
                data = ResultP2S1.objects.filter(student = student)
        elif year_sem == 'PUC2_S2':
                data = ResultP2S2.objects.filter(student = student)
        serializer = ResultE3S1Serializer(data, many=True)
        for item in serializer.data:
            midterm_scores = [item['mid1'], item['mid2'], item['mid3']]
            bo2 = sum(midterm_scores) - min(midterm_scores)
            subject = SubjectInfo.objects.get(subject_code = item['subject'])
            subjectName = subject.name
            subjectCredits = subject.credits
            new_data = {'credits':subjectCredits, 'subject':subjectName, 'bo2':bo2}
            item.update(new_data)

        split_data = {}

        for item in serializer.data:
            year = item['year_of_pass']
            if year not in split_data:
                split_data[year] = []
            split_data[year].append(item)
        return Response({'message':'response', 'data':split_data})