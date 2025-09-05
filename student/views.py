from django.shortcuts import render
from rest_framework.views import APIView
from . models import *
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import SessionAuthentication
from . serializer import *
from rest_framework import status
from django.contrib.auth.decorators import login_required, user_passes_test
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