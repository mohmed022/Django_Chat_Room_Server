from email.policy import default
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from chat3.models import Room










class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_Assistant', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user
    


def uplodeimgeuser(instance, filname):
    return '/%Y/%m/%d/'.join(['NewUser', str(instance.email + "image"), filname])

def uplodeimgpassport(instance, filname):
    return '/%Y/%m/%d/'.join(['NewUser', str(instance.email + "passport"), filname])

def uplodeimgeAcademic(instance, filname):
    return '/%Y/%m/%d/'.join(['NewUser', str(instance.email + "Academic"), filname])


class NewUser(AbstractBaseUser, PermissionsMixin):
    # options2 = (
    #     ('first stage', 'First Stage'),
    #     ('second stage','Second Stage'),
    #     ('third stage', 'Third Stage'),
    #     ('fourth stage','Fourth Stage'),
    # )
    # options = (
    #     ('male', 'Male'),
    #     ('female', 'Female'),
    #     ('others', 'Others')
    # )
    userId = ShortUUIDField()
    image = models.ImageField(upload_to=uplodeimgeuser ,default='default.png' , blank=True, null=True)
    passport = models.ImageField(upload_to=uplodeimgpassport ,default='default.png' , blank=True, null=True)
    Academic = models.ImageField(upload_to=uplodeimgeAcademic ,default='default.png' , blank=True, null=True)
    country = models.CharField( max_length=20 , null=True, blank=True )
    flag = models.CharField( max_length=20 , null=True, blank=True )
    gender = models.CharField( max_length=20 , null=True, blank=True )
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True , null=True)
    first_name = models.CharField(max_length=150, blank=True , null=True)
    LastName = models.CharField(max_length=120, null=True, blank=True)
    university = models.CharField(max_length=120, null=True, blank=True)
    sections   = models.CharField(max_length=120, null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_('about'), max_length=500, blank=True)
    is_online = models.BooleanField(default=False)
    is_activeChat = models.CharField( max_length=20 , null=True, blank=True )    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_Assistant = models.BooleanField(default=False)
        # Nationality = models.CharField(max_length=80, null=True, blank=True)
    objects = CustomAccountManager()
    
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']

    def __str__(self):
        return self.user_name


@receiver(post_save, sender=NewUser)
def create_user_room(sender, instance, created, **kwargs):
    if created:
        # Create a new room for the user
        room = Room.objects.create(name=instance.user_name)
        # Add the user as a participant in the room
        room.users.add(instance)
        room.save()
        
class OnlineUser(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
 
	def __str__(self):
		return self.user.user_name

class Follow_Models(models.Model):
    Follow = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=1)
    name    = models.CharField(max_length=150,null=True )  
    created_Follow = models.ForeignKey(
    settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='created_Follow')

 
    def __str__(self):
        return self.name







