import os
import uuid
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    PermissionsMixin
)

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('rather_not_say', 'Rather not say')
)

def upload_image_path(instance, filename):
    '''Returns the upload image for profile pics
    path = app_name/<user email>/<filename>
    '''
    app_name = instance.__class__.__module__.split('.')[0]
    extension = filename.split('.')[-1]  # Corrected typo: extenstion -> extension
    filename = f"{uuid.uuid4()}.{extension}"
    return os.path.join(app_name, instance.email, filename)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class UserProfile(AbstractUser, PermissionsMixin):
    '''Custom User model
    '''
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=256)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=15, 
                              choices=GENDER_CHOICES, default="rather_not_say")
    profile_pics = models.ImageField(upload_to=upload_image_path,
                                     default='accounts/blank_avatar.png')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False )
    
    one_click_purchasing = models.CharField(max_length=64, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone', 'gender']  # Corrected field name: phone_no -> phone

    def __str__(self):
        return self.email
    
    def set_password(self, raw_password: str) -> None:
        return super().set_password(raw_password)
    
@receiver(pre_save, sender=UserProfile)
def pre_save_username_receiver(sender, instance, *args, **kwargs):
    '''Make username same as email . Username is inherited from AbstractUSer Model
    Username is uniquee
    '''
    if instance.username is None or instance.username=='':
        instance.username = instance.email
