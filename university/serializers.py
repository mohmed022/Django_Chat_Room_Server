from django.forms import ChoiceField
from rest_framework import serializers
from .models import *


# <-----------------------------------------------------------------university_Models-------------------------------------------------------------------------->
class university_ModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = university_Models
        fields = ( '__all__')
        
class universityDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = universityDescription_Models
        fields = ( '__all__')
        
# university Arry photo        
class universityPhotoArrySerializer(serializers.ModelSerializer):
    class Meta:
        model = universityPhotoArry_Models
        fields = ( '__all__')
        
               
# university Arry video                
class universityVideoArrySerializer(serializers.ModelSerializer):
    class Meta:
        model = universityVideoArry_Models
        fields = ( '__all__')




# <-----------------------------------------------------------------sections_Models-------------------------------------------------------------------------->

class sectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = sections_Models
        fields = ( '__all__')

# sections photo Arry
class sectionsPhotoArrySerializer(serializers.ModelSerializer):
    class Meta:
        model = sectionsPhotoArry_Models
        fields = ( '__all__')
        
# sections video Arry
class sectionsVideoArrySerializer(serializers.ModelSerializer):
    class Meta:
        model = sectionsVideoArry_Models
        fields = ( '__all__')
 
 
 # <-----------------------------------------------------------------FormAplctionUser_Models-------------------------------------------------------------------------->

 # FormAplctionUser_Models
class FormAplctionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormAplctionUser_Models
        fields = ( '__all__')
        
        
        
 # <-----------------------------------------------------------------Package_Models-------------------------------------------------------------------------->

 # Package_Models
class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package_Models
        fields = ( '__all__')
        
        
        
 # <-----------------------------------------------------------------Tasks_Models-------------------------------------------------------------------------->

 # Tasks_Models
class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks_Models
        fields = ( '__all__')
        
        
 # <-----------------------------------------------------------------PhoneTrns_Models-------------------------------------------------------------------------->

 # PhoneTrns_Models
class PhoneTrnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneTrns_Models
        fields = ( '__all__')
        
        
        
 # <-----------------------------------------------------------------PaymentConfirmation_Models-------------------------------------------------------------------------->

 # PaymentConfirmation_Models
class PaymentConfirmationSerializer(serializers.ModelSerializer):
    # created_at_py = serializers.DateTimeField(format="%B %d, %Y") 
    # created_at2 = serializers.DateTimeField(format="%H : %M") 
    class Meta:
        model = PaymentConfirmation_Models
        fields = ("created_by_PaymentConfirmation", 'id',
                  "Assistsnt",
                  "university",
                  "sections",
                  "Package",
                  "price",
                  "Apathy",
                  "created_at_py",
                  "created_at_py2",)
        












