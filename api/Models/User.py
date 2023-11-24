from django.db import models
from django.core.validators import RegexValidator
from .Address import Address
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.core import validators
# from ..Hashing import hash_password
import bcrypt
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

    
class User(AbstractBaseUser, PermissionsMixin):

    PHONE_CODES = {
    ('NG', '+234'),
    ('US', '+1'),  
    ('GH', '+235'),  
    }
    
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True)
    firstname = models.CharField(max_length=30, null=True)
    lastname = models.CharField(max_length=30, null=True)
    email = models.EmailField(("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    phone_code = models.CharField(choices=PHONE_CODES, max_length=10, default='NG')
    phone = models.CharField(max_length=11, null=True, unique=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, null=True, blank=True)
    transaction_pin = models.CharField(max_length=4, null=False, default='', validators=[validators.MinLengthValidator(4)])

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def hash_password(self, password):
        # Generate a salt
        salt = bcrypt.gensalt()
        # Hash the password with the salt
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password
    
    def delete(self, *args, **kwargs):
        # Handle deletion of associated address
        if self.address:
            self.address.delete()

        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.transaction_pin = self.hash_password(self.transaction_pin)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.email

