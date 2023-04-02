from django.db import models
from django.contrib.auth.models import User
from users.models import NewUser
from django.conf import settings
from dateutil.relativedelta import relativedelta
from django.db import models

import datetime



# Create your models here.
def uplodeimgeLessons (instance, filname):
    return '/%Y/%m/%d/'.join(['UserProfile' , str(instance.FristName), filname])
class UserProfile(models.Model):
    # owner5=models.OneToOneField(NewUser,on_delete=models.CASCADE,related_name='owner5')
    # ownerr = models.OneToOneField(
    #     settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner')
    # FristName=models.CharField(max_length=200,null=True,blank=True)

    options2 = (
        ('first stage', 'First Stage'),
        ('second stage', 'Second Stage'),
        ('third stage','Third Stage'),
        ('fourth stage','Fourth Stage'),
    )
    options = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('others','Others')
    )
    gender = models.CharField(
        max_length = 20,
        choices = options,
        default = 'male',
        null=False,
        blank=False
        )
    # dob=models.DateField(null=True,blank=True,default=None)
    phone=models.IntegerField(max_length=20,null=True,blank=True)
    LastName=models.CharField(max_length=200,null=True,blank=True)
    Nationality=models.CharField(max_length=200,null=True,blank=True)
    FirstLanguage=models.CharField(max_length=200,null=True,blank=True)
    SecondLanguage=models.CharField(max_length=200,null=True,blank=True)
    TheeducationalStage = models.CharField(
        max_length = 40,
        choices = options2,
        default = 'first stage',
        null=False,
        blank=False
        )

    image  = models.ImageField(upload_to=uplodeimgeLessons ,blank=True,null=True)


    dob = models.DateField(max_length=8)
    age = models.IntegerField() 
    def __str__(self):
        today = datetime.today()
        delta = relativedelta(today, self.dob)
        return str(delta.years)

        