from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

from django.utils import timezone


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = None
    last_name = None


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class TokenModel(models.Model):
    key = models.CharField(max_length=100, unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)


class UserProfile(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'

    GENDER_CHOICES = [
        (MALE,'Male'),
        (FEMALE,'Female')]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to=' images/')
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    

    def __str__(self):
        return self.first_name

    
    class Meta:
        ordering = ['first_name']

class HealthRecord(models.Model):   
    underlying_conditions = models.TextField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    bmi = models.DecimalField(max_digits=10, decimal_places=2)     
    datetime = models.DateTimeField(auto_now=True)
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.underlying_conditions

    class Meta:
        ordering = ['weight']

    

class UserGoal(models.Model):
    SHRED = 'Shred'
    BULK = 'Bulk'

    SIZE_CHOICES = [
        (SHRED,'Shred'),
        (BULK,'Bulk')]


    new_weight = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES)
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.new_weight

    class Meta:
        ordering = ['new_weight']

