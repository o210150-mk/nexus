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
    
    
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string 
from django.conf import settings
from django.utils.html import strip_tags
from django.core.mail import send_mail

class GetMail(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer_class = GetMailSerializer(data = request.data)
        if serializer_class.is_valid():
            gmail = serializer_class.validated_data['gmail']
            subject = 'Your HTML Welcome'
            from_email = settings.DEFAULT_FROM_EMAIL
            to = [gmail]
#             result = send_mail(

#   'Reset Password',

#   f"This is 6 digit otp {123456} to reset the password.",

#   settings.EMAIL_HOST_USER, # Sender must be your configured Gmail address

#   [gmail], # Your actual recipient address

#   fail_silently=False, # Crucial: forces an exception if the SMTP connection fails

# )
    # Render HTML template (assuming you have one at 'email/welcome.html')
    # Or you can define the HTML directly as a string
            # html_content = render_to_string('templates/mail.html', {'username': 'User'})
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            request.session.save()
            html_content = render_to_string('mail.html', {'username': gmail, 'otp':otp})
    # # Create a plain text version for non-HTML email clients
            text_content = strip_tags(html_content) 
            print('1')
    # # 2. Create the message object
            msg = EmailMultiAlternatives('Password Reset', f"This is the 6 digit otp to rest your password", from_email, to)
            print('2')
    # # 3. Attach the HTML version
            msg.attach_alternative(html_content, "text/html")
            print('3')
    # # 4. Send the email
            msg.send(fail_silently=False)
            print('4')
            return Response({'message':'Mail sent successfully...'})
        return Response({'message':'Error...'})
    
class VerifyOtp(APIView):
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
    def post(self, request):
        serializer_class = getPasswordSerializer(data = request.data)

        if serializer_class.is_valid():
                password = serializer_class.validated_data['password']
                gmail = serializer_class.validated_data['gmail']
                user = CustomUser.objects.get(email=gmail)
                user.set_password(password)
                user.save()
                return Response({'message':'password changed successfully...'})
        else:
                print('Error')

class ResendMail(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer_class = GetMailSerializer(data = request.data)
        if serializer_class.is_valid():
            gmail = serializer_class.validated_data['gmail']
            subject = 'Your HTML Welcome'
            from_email = settings.DEFAULT_FROM_EMAIL
            to = [gmail]
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            request.session.save()
#             result = send_mail(

#   'Reset Password',

#   f"This is 6 digit otp {123456} to reset the password.",

#   settings.EMAIL_HOST_USER, # Sender must be your configured Gmail address

#   [gmail], # Your actual recipient address

#   fail_silently=False, # Crucial: forces an exception if the SMTP connection fails

# )
    # Render HTML template (assuming you have one at 'email/welcome.html')
    # Or you can define the HTML directly as a string
            # html_content = render_to_string('templates/mail.html', {'username': 'User'})
            html_content = render_to_string('mail.html', {'username': gmail, 'otp':otp})
    # # Create a plain text version for non-HTML email clients
            text_content = strip_tags(html_content) 

    # # 2. Create the message object
            msg = EmailMultiAlternatives('Password Reset', f"This is the 6 digit otp to rest your password", from_email, to)
    
    # # 3. Attach the HTML version
            msg.attach_alternative(html_content, "text/html")
    
    # # 4. Send the email
            msg.send(fail_silently=False)
            return Response({'message':'Mail sent successfully...'})
        return Response({'message':'Error...'})
