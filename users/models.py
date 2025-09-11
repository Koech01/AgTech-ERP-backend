from django.db import models  
from .imageUID import profileIconUID
from django.contrib.auth.models import AbstractUser 
from django.core.validators import FileExtensionValidator


# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        FARMER = 'farmer', 'Farmer'

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.FARMER)
    profile_icon = models.ImageField(upload_to=profileIconUID, null=True, blank=True, default='profileIcon.png', validators=[FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    created = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username}"
    
    def save(self, *args, **kwargs): 
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)