from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.user.username

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, related_name="orders")
    date_ordered = models.DateTimeField(auto_now_add=True)

    

