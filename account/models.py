from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinLengthValidator

class UserManager(BaseUserManager):
    def create_user(self, password=None, **extra_fields):
        phone = extra_fields.get('country_code') and extra_fields.get('phone_no')
        if (phone is not None) or extra_fields['email']:
            user = self.model(**extra_fields)
            user.set_password(password)
            user.save()
            return user

    def create_superuser(self, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        user = self.create_user(password=password,**extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    profile = models.ImageField(upload_to='profile_pics', null=False, blank=False)
    full_name = models.CharField(validators =(MinLengthValidator(6),), max_length=50)
    email = models.EmailField(unique=True, max_length=50, null=True, error_messages={'unique':"This email has already been registered."})
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=25, blank=True, choices=(('1','Male'),('2','Female'),('3','Other')))
    country_code = models.CharField(validators =[MinLengthValidator(2)], max_length=4)
    phone_no = models.CharField(validators =[MinLengthValidator(9)], max_length=10, unique=True, null=True)
    otp = models.CharField(validators=[MinLengthValidator(6)], max_length=6)
    tfa = models.BooleanField(verbose_name='Two-Factor Authentication', default=False)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    first_name, last_name = None, None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    objects = UserManager()

    def __str__(self):
        return self.username