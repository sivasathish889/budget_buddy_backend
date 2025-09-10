from django.db import models
from datetime import date
# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=30, )
    email = models.EmailField(unique=True)
    phone = models.BigIntegerField(verbose_name="Phone Number", null=True,)
    DOB = models.DateField(verbose_name="Date of birth", null=True, )
    goal = models.IntegerField(blank=True,null=True, verbose_name="Goal", default=0)
    password = models.CharField(max_length=500, verbose_name="Password", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_age(self):
         today = date.today()
         age = today.year - self.DOB.year - ((today.month, today.day) < (self.DOB.month, self.DOB.day))
         return age
    class Meta:
        db_table = "Users"
    
    
    

class Catagory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "Catagory"

class Expense(models.Model):

    amount = models.FloatField()
    description = models.CharField(max_length=100)
    category = models.ForeignKey(Catagory, on_delete=models.CASCADE, null=True)
    date = models.DateField(default=date.today)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.description
    
    class Meta:
        db_table = "Expense"





