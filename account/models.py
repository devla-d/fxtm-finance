from django.db import models 
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings 

import random
import json
import string
#from uuid import uuid4






class Account(AbstractUser):
    fullname    = models.CharField(max_length=100,blank=True,null=True)
    #username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email       = models.EmailField(verbose_name='email', max_length=60, unique=True )
    zipcode    = models.CharField(max_length=30,blank=True,null=True)
    country    = models.CharField(max_length=100,blank=True,null=True)
    
    address    = models.CharField(max_length=100,blank=True,null=True)
    gender    = models.CharField(max_length=100,blank=True,null=True)
    state    = models.CharField(max_length=100,blank=True,null=True)
    city    = models.CharField(max_length=100,blank=True,null=True)

    date_of_birth = models.DateTimeField(blank=True,null=True)

    profile_image = models.ImageField(blank=True, null=True, upload_to='uploads')
    phone = models.CharField(max_length=30, blank=True,null=True,unique=True)
    balance = models.IntegerField(default=0, blank=True,null=True)
    deposite_balance = models.IntegerField(default=0, blank=True,null=True)
    total_amount_invested = models.IntegerField(default=0, blank=True,null=True)
    total_investement_count = models.IntegerField(default=0, blank=True,null=True)
    withdraw_total = models.IntegerField(default=0, blank=True,null=True) 
    is_email_verifield = models.BooleanField(default=False)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']



    def __str__(self):
        return self.email