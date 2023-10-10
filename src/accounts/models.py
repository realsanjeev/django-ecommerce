from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    # email as main component for auth instead of username
    email = models.EmailField(blank=False, null=False, unique=True)
    full_name = models.CharField(max_length=256)
    profile_pics = models.ImageField(upload_to='profile_pics/')
    phone_no = models.CharField(max_length=15)
    
    def __str__(self) -> str:
        return self.username