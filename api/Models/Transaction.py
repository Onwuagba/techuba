from django.db import models
from ..models import User
from django.utils import timezone
from datetime import datetime

class Transaction(models.Model):
    sender = models.CharField(max_length=30, null=False)
    receiver = models.CharField(max_length=30, null=False)
    amount = models.BigIntegerField(null=False)
    transaction_date = models.DateTimeField(null=False)

    def __str__(self):
        return self.sender