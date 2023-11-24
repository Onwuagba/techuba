from django.db import models
from django.core.validators import RegexValidator

class Address(models.Model):
    COUNTRIES = {
    ('NG', 'Nigeria'), 
    ('GH', 'Ghana'), 
    ('SN', 'Senegal'), 
    ('CIV', 'Ivory Coast')
    }
    number = models.CharField(max_length=6, null=True, blank=True)
    street = models.CharField(max_length=30, null=True, blank=True, validators=[RegexValidator(regex='^[a-zA-z]*$', message='No numbers allowed', code='invalid_street_name')])
    city = models.CharField(max_length=30, null=True, blank=True, validators=[RegexValidator(regex='^[a-zA-z]*$', message='No numbers allowed', code='invalid_city_name')])
    state = models.CharField(max_length=30, null=True, blank=True, validators=[RegexValidator(regex='^[a-zA-z]*$', message='No numbers allowed', code='invalid_state_name')])
    country = models.CharField(max_length=5, null=True, blank=True, choices=COUNTRIES,default='NG',)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.number} {self.street} {self.city} {self.state}, {self.country}"