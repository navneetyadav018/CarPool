from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='category')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
# baked dish category
    
# baked dish 

    
class Car(models.Model):
    car_id = models.IntegerField(default=0)
    car_name = models.CharField(max_length=30,default="")
    car_desc = models.CharField(max_length=300,default="")
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="car/images",default="")

    def __str__(self):
        return self.car_name

class Order(models.Model) :
    STATUS_CHOICES = [
        ('SUCCESSFUL', 'Successful'),
        ('CANCELLED', 'Cancelled'),
    ]
    user= models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    order_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=90,default="")
    email = models.CharField(max_length=50,default="")
    phone = models.CharField(max_length=20,default="")
    address = models.CharField(max_length=500,default="")
    city = models.CharField(max_length=50,default="")
    cars = models.CharField(max_length=50,default="")
    days_for_rent = models.IntegerField(default=0)
    date = models.CharField(max_length=50,default="")
    loc_from = models.CharField(max_length=50,default="")
    loc_to = models.CharField(max_length=50,default="")
   
    
    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"
    from django.contrib.auth.models import User


   
class Profile(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
  geneder_choices = (
    ('male','Male'),
    ('female','Female'),
    ('other','Other')
  )
  name = models.CharField(max_length=50)
  
 
 
  bio = models.CharField(max_length=200,default=1)
  gender= models.CharField(max_length=10,choices=geneder_choices)
  image = models.ImageField(upload_to='profiles')
  age = models.IntegerField()
  email = models.EmailField()
  number = models.CharField(max_length=10)
  
  # photo = models.ImageField(upload_to='profile')

  def __str__(self):
    return self.name
  
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question
    
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    feedback_text = models.TextField() # Provide a default value
    rating = models.PositiveIntegerField()  # Assuming rating is out of 5
    created_at = models.DateTimeField(default=timezone.now)  # Set default to current time
    class Meta:
        unique_together = ['order', 'user']
    
    def __str__(self):
        return f'Feedback by {self.name} for Order {self.order.order_id}'
    