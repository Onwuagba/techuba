from django.db import models
from django.core.validators import RegexValidator
from .User import User

class Account(models.Model):
    username = models.ForeignKey(User, on_delete=models.DO_NOTHING, null= False)
    account_number = models.CharField(max_length=10, null=False, unique=True, default='' )
    account_balance = models.BigIntegerField(default=0, null=False)
    pin = models.IntegerField(max_length=4, null=False, unique=False)


