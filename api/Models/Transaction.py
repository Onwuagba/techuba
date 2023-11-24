from django.db import models
from ..models import User
from django.utils import timezone
from datetime import datetime
from ..Models.Account import Account

class Transaction(models.Model):
    sender = models.CharField(max_length=30, null=False)
    receiver = models.CharField(max_length=30, null=False)
    amount = models.BigIntegerField(null=False)
    transaction_date = models.DateTimeField(null=False)

    def __str__(self):
        return self.sender
    
class TransactionHistory(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, default=000)  # New field for account number
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return str(self.account.account_number)
    
    