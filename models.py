from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from distutils.command.upload import upload
from django.contrib.auth.models import User
import datetime
# from django.contrib.auth.models import PermissionsMixin
from fileinput import  filename
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,render
from django.contrib import messages


class MyAccountManager(BaseUserManager):
    def create_user(self,name,lname,email,phone,address,city,state,pincode,password=None):
        if not email:
            raise ValueError("user must have an email address")
        user=self.model(
           email=self.normalize_email(email),
           name=name,
           lname=lname,
           phone=phone,
           address=address,
           city=city,
           state=state,
           pincode=pincode,
           
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    def create_superuser(self,password,email,**extra_fields):
        user=self.create_user(
            email=self.normalize_email(email),
            password=password,**extra_fields

         )
    
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user

    


# ,PermissionsMixin
class Account(AbstractBaseUser):
    status_choices=(('Approved','Approved'),('Pending','Pending'),('None','None'))
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,default='')
    lname=models.CharField(max_length=50,default='')
    email=models.CharField(max_length=100,unique=True)
    phone=models.BigIntegerField(default=0,unique=True)
    address=models.CharField(max_length=100,default='')
    city=models.CharField(max_length=100,default='')
    state=models.CharField(max_length=50)
    pincode=models.BigIntegerField()
    status=models.CharField(default='Approved',choices=status_choices,max_length=40)
    #required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'lname','phone','address','city','state','pincode']

    # REQUIRED_FIELDS = ['username','password']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.name} {self.lname}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
    
    def get_all_permissions(user=None):
        if user.is_superadmin:
            return set()
    






class product(models.Model):
    product_image = models.ImageField(upload_to='pics')
    product_description = models.CharField(max_length=100)
    def __str__(self):
        return self.product_description

class productcustomer(models.Model):
    product_image = models.ImageField(upload_to='pics')
    product_name = models.CharField(max_length=100,unique=True)
    product_description = models.CharField(max_length=100)
    product_price = models.IntegerField()
    stock = models.IntegerField(default=1)
    
    def __str__(self):
        return self.product_name

class Cart(models.Model):
    user =models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(productcustomer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return str(self.user)

    @property
    def total_cost(self):
        return self.quantity * self.product.product_price
class dumb(models.Model) :
    fk = models.ForeignKey(Account,on_delete=models.SET_NULL, blank=True, null=True)
    wimage = models.ImageField(upload_to='pics/',blank=True)
    date = models.DateTimeField(null=True)

    @property
    def name(self):
        return self.fk.name

    def __str__(self):
        return self.fk.name

