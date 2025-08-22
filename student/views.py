from django.shortcuts import render
from rest_framework.views import APIView
from . models import *
from rest_framework.response import Response
from . serializer import *

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

class StudentView(APIView):
    def get(self, request):
        serializer_class = StudentSerializer
        data = Student.objects.all()
        data = serializer_class(data, many=True)
        return Response(data.data)

class LogView(APIView):
    serializer_class = LogSerializer

    def get(self, request):
        return Response({'data':'enter data'})
    
    def post(self, request):
        serializer = LogSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.data['email'])
        return Response({'data':'logged'})