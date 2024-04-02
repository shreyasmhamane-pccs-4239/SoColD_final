from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    CAT=((1,'Energy Drink'),(2,'Health Drink'),(3,'Soft Drink'),(4,'Cold Drink'))
    name=models.CharField(max_length=40,verbose_name="product name")
    price=models.FloatField()
    pdetails=models.CharField(max_length=100,verbose_name="Product details")
    cat=models.IntegerField(verbose_name="Category",choices=CAT)
    is_active=models.BooleanField(default=True,verbose_name="Available")
    pimage=models.ImageField(upload_to="image")
    
    def __str__(self):
      return self.name

class Cart(models.Model):
   uid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column="uid")
   pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
   qty=models.IntegerField(default=1)

class Order(models.Model):
      order_id=models.CharField(max_length=50)
      uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
      pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
      qty=models.IntegerField(default=1)
 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name