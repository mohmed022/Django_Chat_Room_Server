import os
from pyexpat import model
from django.urls import reverse
from django.db import models
from datetime import datetime, timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings

from django.db import models
from django.template.defaultfilters import slugify
import datetime
from django.utils import timezone
from chat3.models import Room

def uplodeimgeuniversity (instance, filname):
    return '/%Y/%m/%d/'.join(['university_Models' , str(instance.photo.name), filname])

def uplodevidewuniversity (instance, filname):
    return '/%Y/%m/%d/'.join(['university_Models' , str(instance.video.name), filname])




# <-----------------------------------------------------------------university_Models-------------------------------------------------------------------------->
class university_Models(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created_by_university = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by_university')
    name       = models.CharField(max_length=150,null=True )  
    description= models.TextField(max_length=3000,blank=True)
    link       = models.TextField(max_length=3000,blank=True)
    photo      = models.ImageField(upload_to=uplodeimgeuniversity ,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class universityDescription_Models(models.Model):
    created_by_universityDescription = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by_universityDescription')
    university = models.ForeignKey(university_Models, on_delete=models.CASCADE, default=1)
    name       = models.CharField(max_length=150,null=True )  
    link       = models.CharField(max_length=3000,null=True )  
    description= models.TextField(max_length=3000,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name

class universityPhotoArry_Models(models.Model):
    created_by_universityPhotoArry = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by_universityPhotoArry')
    university = models.ForeignKey(university_Models, on_delete=models.CASCADE, default=1)
    photo      = models.ImageField(upload_to=uplodeimgeuniversity ,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.photo.name

class universityVideoArry_Models(models.Model):
    created_by_universityVideoArry = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by_universityVideoArry')
    university = models.ForeignKey(university_Models, on_delete=models.CASCADE, default=1)
    name       = models.CharField(max_length=150,null=True )  
    link       = models.CharField(max_length=3000,null=True )  
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name


# <-----------------------------------------------------------------sections_Models-------------------------------------------------------------------------->

class sections_Models(models.Model):
    created_by_sections = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by_sections')
    university = models.ForeignKey(university_Models, on_delete=models.CASCADE, default=1)
    name       = models.CharField(max_length=150,null=True )  
    link       = models.CharField(max_length=3000,null=True )  
    description= models.TextField(max_length=3000,blank=True)
    photo      = models.ImageField(upload_to=uplodeimgeuniversity ,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name



class sectionsPhotoArry_Models(models.Model):
    created_by_sectionsPhotoArry = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by_sectionsPhotoArry')
    university = models.ForeignKey(university_Models, on_delete=models.CASCADE, default=1)
    sections = models.ForeignKey(sections_Models, on_delete=models.CASCADE, default=1)
    name       = models.CharField(max_length=150,null=True )  
    photo      = models.ImageField(upload_to=uplodeimgeuniversity ,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name
    

class sectionsVideoArry_Models(models.Model):
    created_by_sectionsVideoArry = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by_sectionsVideoArry')
    university = models.ForeignKey(university_Models, on_delete=models.CASCADE, default=1)
    sections = models.ForeignKey(sections_Models, on_delete=models.CASCADE, default=1)
    name       = models.CharField(max_length=150,null=True )  
    link       = models.CharField(max_length=3000,null=True )  
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name





    
    
    
# <-----------------------------------------------------------------FormAplctionUser_Models-------------------------------------------------------------------------->
def uplodephoto_Acca (instance, filname):
    return '/%Y/%m/%d/'.join(['FormAplctionUser_Models' , str(instance.Name_UserAll), filname])

def uplodephoto_Pass (instance, filname):
    return '/%Y/%m/%d/'.join(['FormAplctionUser_Models' , str(instance.Name_UserAll), filname])


class FormAplctionUser_Models(models.Model):
    created_by_FormAplctionUser = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by_FormAplctionUser')
    university = models.ForeignKey(university_Models, on_delete=models.CASCADE, default=1)
    sections = models.ForeignKey(sections_Models, on_delete=models.CASCADE, default=1)
    Name_UserAll       = models.CharField(max_length=150,null=True )  
    phone       = models.CharField(max_length=150,null=True )  
    famile_Name_User       = models.CharField(max_length=150,null=True )  
    photo      = models.ImageField(upload_to=uplodephoto_Pass ,blank=True,null=True)
    Acca      = models.ImageField(upload_to=uplodephoto_Acca ,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.Name_UserAll
    
# <-----------------------------------------------------------------Tasks_Models-------------------------------------------------------------------------->



    
class Package_Models(models.Model):
    created_by_Package = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by_Package')
    university = models.ForeignKey(university_Models, on_delete=models.CASCADE, default=1)
    sections = models.ForeignKey(sections_Models, on_delete=models.CASCADE, default=1)
    Name_Package       = models.CharField(max_length=150,null=True )  
    description= models.TextField(max_length=700,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.Name_Package
    
    

    
class Tasks_Models(models.Model):
    created_by_Tasks = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by_Tasks')
    university = models.ForeignKey(university_Models, on_delete=models.CASCADE, default=1)
    sections = models.ForeignKey(sections_Models, on_delete=models.CASCADE, default=1)
    Package = models.ForeignKey(Package_Models, on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    Name_Tasks       = models.CharField(max_length=150,null=True )  
    description= models.TextField(max_length=700,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.Name_Tasks
    
    
    
    
    # <-----------------------------------------------------------------Tasks_Models-------------------------------------------------------------------------->
class PhoneTrns_Models(models.Model):
    options = (
        ('vodafone', 'Vodafone'),
        ('orange',   'Orange'),
        ('etisalat', 'Etisalat'),
        ('Bank', 'Bank')

    )
    Name_Compony = models.CharField( max_length=20, choices=options, default='vodafone', null=False, blank=False )
    created_by_PhoneTrns = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by_PhoneTrns')
    university = models.ForeignKey(university_Models, on_delete=models.CASCADE, default=1)
    # Name_Compony = models.CharField(max_length=150,null=True )  
    PhoneTrns = models.IntegerField("")
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.Name_Compony
    
    
    
    

    # <-----------------------------------------------------------------تاكيد الدفع -------------------------------------------------------------------------->
def uplodephoto_Apathy (instance, filname):
    return '/%Y/%m/%d/'.join(['paymentConfirmation_Models' , str(instance.university.name), filname])

from django.db import transaction

from django.db import models, transaction
from django.conf import settings


class PaymentConfirmation_Models(models.Model):
    created_by_PaymentConfirmation = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by_PaymentConfirmation'
    )
    Assistsnt = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Assistsnt'
    )
    university = models.ForeignKey(university_Models, on_delete=models.CASCADE, default=1)
    sections = models.ForeignKey(sections_Models, on_delete=models.CASCADE, default=1)
    Package = models.ForeignKey(Package_Models, on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    Apathy = models.ImageField(upload_to=uplodephoto_Apathy, blank=True, null=True)
    created_at_py = models.DateTimeField(auto_now_add=True, null=True)
    created_at_py2 = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        # Call the parent save method
        super().save(*args, **kwargs)

        # Use a transaction to ensure atomicity
        with transaction.atomic():
            # Get or create the chat room based on the user
            chat_room, created = Room.objects.get_or_create(
                name=f"{self.created_by_PaymentConfirmation.user_name}"
                # 's chat room
            )

            # Add the user to the chat room if they're not already a member
            if not chat_room.users.filter(id=self.created_by_PaymentConfirmation.id).exists():
                chat_room.users.add(self.created_by_PaymentConfirmation)

            # Add the assistant to the chat room if they're not already a member
            if not chat_room.users.filter(id=self.Assistsnt.id).exists():
                chat_room.users.add(self.Assistsnt)

            # If the chat room was just created, add the payment creator and assistant to the room
            if created:
                chat_room.users.add(self.created_by_PaymentConfirmation, self.Assistsnt)


    