from django.shortcuts import get_object_or_404, render
from .serializers import *
from rest_framework import viewsets      
from .models import *                 
from django.http import HttpResponse
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, filters, generics, permissions

from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission, IsAdminUser, DjangoModelPermissions
from rest_framework import viewsets
from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from rest_framework import viewsets, filters, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser


# <-----------------------------------------------------------------university_Models-------------------------------------------------------------------------->



# # Lesson All List
# class LessonsListView(viewsets.ModelViewSet):  
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = ListSerializer   
#     queryset = Lessons_Models.objects.all() 




# university All List
class university_ModelsView(viewsets.ModelViewSet):  
    serializer_class = university_ModelsSerializer   
    queryset = university_Models.objects.all() 
    
    
# university Arry Description All List
class universityDescriptionView(viewsets.ModelViewSet):  
    serializer_class = universityDescriptionSerializer   
    queryset = universityDescription_Models.objects.all() 
    
    
# university Arry photo All List
class universityPhotoArryView(viewsets.ModelViewSet):  
    serializer_class = universityPhotoArrySerializer   
    queryset = universityPhotoArry_Models.objects.all() 
    
    
    
# university  Arry video All List
class universityVideoArryView(viewsets.ModelViewSet):  
    serializer_class = universityVideoArrySerializer   
    queryset = universityVideoArry_Models.objects.all() 








# <-----------------------------------------------------------------sections_Models-------------------------------------------------------------------------->

# sections All List
class sections_ModelsView(viewsets.ModelViewSet):  
    serializer_class = sectionsSerializer   
    queryset = sections_Models.objects.all() 
    
    
# sections Arry photo All List
class sectionsPhotoArryView(viewsets.ModelViewSet):  
    serializer_class = sectionsPhotoArrySerializer   
    queryset = sectionsPhotoArry_Models.objects.all() 
    
    
    
# sections  Arry video All List
class sectionsVideoArryView(viewsets.ModelViewSet):  
    serializer_class = sectionsVideoArrySerializer   
    queryset = sectionsVideoArry_Models.objects.all() 
    
    
    
# <-----------------------------------------------------------------sections_Models-------------------------------------------------------------------------->

# FormAplctionUserSerializer
class FormAplctionUserView(viewsets.ModelViewSet):  
    serializer_class = FormAplctionUserSerializer   
    queryset = FormAplctionUser_Models.objects.all() 
    
    
    
# <-----------------------------------------------------------------PackageModels-------------------------------------------------------------------------->

# PackageSerializer
class PackageView(viewsets.ModelViewSet):  
    serializer_class = PackageSerializer   
    queryset = Package_Models.objects.all() 
    
    
# <-----------------------------------------------------------------TasksModels-------------------------------------------------------------------------->

# TasksSerializer
class TasksView(viewsets.ModelViewSet):  
    serializer_class = TasksSerializer   
    queryset = Tasks_Models.objects.all() 
    
    
    
# PhoneTrnsView
class PhoneTrnsView(viewsets.ModelViewSet):  
    serializer_class = PhoneTrnsSerializer   
    queryset = PhoneTrns_Models.objects.all() 
    
    
# PaymentConfirmationView
class PaymentConfirmationView(viewsets.ModelViewSet):  
    serializer_class = PaymentConfirmationSerializer   
    queryset = PaymentConfirmation_Models.objects.all() 