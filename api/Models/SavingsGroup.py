from django.db import models
# from ..models import User
from ..Models.User import User

class SavingsGroup(models.Model):
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    group_name = models.CharField(max_length=50, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_break = models.DateTimeField(auto_now_add=True)
    date_fulfilled = models.DateTimeField(auto_now_add=True)
    target_amount = models.BigIntegerField(max_length=11, null=False)
    current_amount = models.BigIntegerField(null=True, default=0)
    interest = models.FloatField()
    group_members = models.ManyToManyField(User, related_name='group_members', blank=True, default='')
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.group_name