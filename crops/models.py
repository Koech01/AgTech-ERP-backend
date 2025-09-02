from django.db import models
from users.models import User


# Create your models here.
class Crop(models.Model):
    CROP_TYPES = [
        ('cereal', 'Cereal/Grain'),      
        ('legume', 'Legume'),             
        ('vegetable', 'Vegetable'),      
        ('fruit', 'Fruit'),              
        ('root_tuber', 'Root/Tuber'),     
        ('oil_crop', 'Oil Crop'),         
        ('fodder', 'Fodder/Forage'),     
        ('other', 'Other')                 
    ]
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cropFarmer')
    name = models.CharField(max_length=100)
    crop_type = models.CharField(max_length=20, choices=CROP_TYPES)
    quantity = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.crop_type} - {self.farmer.username}' 