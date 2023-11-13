from django.db import models
from django.core.validators import RegexValidator

class Address(models.Model):
    COUNTRIES = {
    ('NG', 'Nigeria'), 
    ('GH', 'Ghana'), 
    ('SN', 'Senegal'), 
    ('CIV', 'Ivory Coast')
    }
    number = models.CharField(max_length=6)
    street = models.CharField(max_length=30, validators=[RegexValidator(regex='^[a-zA-z]*$', message='No numbers allowed', code='invalid_firstname')])
    city = models.CharField(max_length=30, validators=[RegexValidator(regex='^[a-zA-z]*$', message='No numbers allowed', code='invalid_firstname')])
    state = models.CharField(max_length=30, validators=[RegexValidator(regex='^[a-zA-z]*$', message='No numbers allowed', code='invalid_firstname')])
    country = models.CharField(max_length=5, choices=COUNTRIES,default='NG',)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.state}, {self.country}"