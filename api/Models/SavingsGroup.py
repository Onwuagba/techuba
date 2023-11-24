from django.db import models
from ..Models.User import User
from django.utils import timezone
import random
import string


def sg_id(length=10):
    alphanumeric_chars = string.ascii_letters + string.digits
    return ''.join(random.choices(alphanumeric_chars, k=length))

class SavingsGroup(models.Model):
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    group_name = models.CharField(max_length=50, null=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_fulfilled = models.DateTimeField(blank=True, null=True)
    target_amount = models.BigIntegerField(null=False)
    current_amount = models.BigIntegerField(null=True, default=0)
    interest = models.FloatField(default=0, editable=False)
    group_members = models.ManyToManyField(User, related_name='group_members', blank=True, default='')
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.group_name
    
    def save(self, *args, **kwargs):
        if int(self.current_amount) == int(self.target_amount):
            self.date_fulfilled = timezone.now()
        super().save(*args, **kwargs)




from django.db import models
from ..models import User

class SGDeposit(models.Model):

    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sg = models.ForeignKey(SavingsGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.amount} - {self.user}" 
