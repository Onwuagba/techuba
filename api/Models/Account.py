from django.db import models
import random
import string
from django.core.validators import RegexValidator
from .User import User
import bcrypt


def generate_patterned_digits():
# Define your pattern or logic to generate the ten digits
# For example, let's generate a random 10-digit number
    return ''.join(random.choices(string.digits, k=10))
class Account(models.Model):

    username = models.ForeignKey(User, on_delete=models.CASCADE, null= False, related_name="accounts")
    account_number = models.CharField(max_length=10, null=False, unique=True, default=generate_patterned_digits,)
    account_balance = models.BigIntegerField(default=0, null=False)
    pin = models.CharField(max_length=70, null=False, unique=False)

    def hash_pin(self, pin):
        salt = bcrypt.gensalt()

        hashed_pin = bcrypt.hashpw(pin.encode('utf-8'), salt)
        return hashed_pin.decode('utf-8')
    
    def save(self, *args, **kwargs):
        if self._state.adding:
            self.pin = self.hash_pin(self.pin)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return (f"{self.account_number}")
    