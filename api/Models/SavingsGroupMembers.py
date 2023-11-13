from django.db import models
from ..Models.SavingsGroup import SavingsGroup

class SavingsGroupMembers(models.Model):
    name_of_set = models.CharField(SavingsGroup.name_of_group)
    savings_group = models.OneToOneField(SavingsGroup, on_delete=models.CASCADE, related_name="members")
    

    def __str__(self):
        return self.name_of_set