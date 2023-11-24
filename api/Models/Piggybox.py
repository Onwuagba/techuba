from django.db import models
from ..models import User
from django.utils import timezone
from datetime import datetime
import random
import string

class Piggybox(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="piggyboxes")
    name_of_box = models.CharField(max_length=30, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_break = models.DateTimeField(null=True, blank=True)
    date_fulfilled = models.DateTimeField(null=True, blank=True)
    target_amount = models.PositiveIntegerField(default=0, null=False)
    current_amount = models.PositiveBigIntegerField(default=0)
    interest = models.FloatField(default=0.5)



    class Meta:
        verbose_name_plural = "Piggyboxes"

    def save(self, *args, **kwargs):
        if int(self.current_amount) == int(self.target_amount):
            self.date_fulfilled = timezone.now()

        super().save(*args, **kwargs)
    
    


    def __str__(self):
        return self.name_of_box
