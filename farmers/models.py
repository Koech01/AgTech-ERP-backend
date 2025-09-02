from django.db import models
from users.models import User


# Create your models here.
class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userFarmer')
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username}'