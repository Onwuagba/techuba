from django.db import models
from django.core.validators import RegexValidator
from .Address import Address
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
        
    
class User(models.Model):
    PHONE_CODES = {
    ('AF', '+93'),  # Afghanistan
    ('AL', '+355'),  # Albania
    ('DZ', '+213'),  # Algeria
    ('AD', '+376'),  # Andorra
    ('AO', '+244'),  # Angola
    ('AG', '+1-268'),  # Antigua and Barbuda
    ('AR', '+54'),  # Argentina
    ('AM', '+374'),  # Armenia
    ('AU', '+61'),  # Australia
    ('AT', '+43'),  # Austria
    ('AZ', '+994'),  # Azerbaijan
    ('BS', '+1-242'),  # Bahamas
    ('BH', '+973'),  # Bahrain
    ('BD', '+880'),  # Bangladesh
    ('BB', '+1-246'),  # Barbados
    ('BY', '+375'),  # Belarus
    ('BE', '+32'),  # Belgium
    ('BZ', '+501'),  # Belize
    ('BJ', '+229'),  # Benin
    ('BT', '+975'),  # Bhutan
    ('BO', '+591'),  # Bolivia
    ('BA', '+387'),  # Bosnia and Herzegovina
    ('BW', '+267'),  # Botswana
    ('BR', '+55'),  # Brazil
    ('BN', '+673'),  # Brunei
    ('BG', '+359'),  # Bulgaria
    ('BF', '+226'),  # Burkina Faso
    ('BI', '+257'),  # Burundi
    ('CV', '+238'),  # Cabo Verde
    ('KH', '+855'),  # Cambodia
    ('CM', '+237'),  # Cameroon
    ('CA', '+1'),  # Canada
    ('CF', '+236'),  # Central African Republic
    ('TD', '+235'),  # Chad
    ('CL', '+56'),  # Chile
    ('CN', '+86'),  # China
    ('CO', '+57'),  # Colombia
    ('KM', '+269'),  # Comoros
    ('CG', '+242'),  # Congo
    ('CR', '+506'),  # Costa Rica
    ('HR', '+385'),  # Croatia
    ('CU', '+53'),  # Cuba
    ('CY', '+357'),  # Cyprus
    ('CZ', '+420'),  # Czechia
    ('DK', '+45'),  # Denmark
    ('DJ', '+253'),  # Djibouti
    ('DM', '+1-767'),  # Dominica
    ('DO', '+1-809'),  # Dominican Republic
    ('EC', '+593'),  # Ecuador
    ('EG', '+20'),  # Egypt
    ('SV', '+503'),  # El Salvador
    ('GQ', '+240'),  # Equatorial Guinea
    ('ER', '+291'),  # Eritrea
    ('EE', '+372'),  # Estonia
    ('ET', '+251'),  # Ethiopia
    ('FJ', '+679'),  # Fiji
    ('FI', '+358'),  # Finland
    ('FR', '+33'),  # France
    ('GA', '+241'),  # Gabon
    ('GM', '+220'),  # Gambia
    ('GE', '+995'),  # Georgia
    ('DE', '+49'),  # Germany
    ('GH', '+233'),  # Ghana
    ('GR', '+30'),  # Greece
    ('GD', '+1-473'),  # Grenada
    ('GT', '+502'),  # Guatemala
    ('GN', '+224'),  # Guinea
    ('GW', '+245'),  # Guinea-Bissau
    ('GY', '+592'),  # Guyana
    ('HT', '+509'),  # Haiti
    ('HN', '+504'),  # Honduras
    ('HU', '+36'),  # Hungary
    ('IS', '+354'),  # Iceland
    ('IN', '+91'),  # India
    ('ID', '+62'),  # Indonesia
    ('IR', '+98'),  # Iran
    ('IQ', '+964'),  # Iraq
    ('IE', '+353'),  # Ireland
    ('IL', '+972'),  # Israel
    ('IT', '+39'),  # Italy
    ('JM', '+1-876'),  # Jamaica
    ('JP', '+81'),  # Japan
    ('JO', '+962'),  # Jordan
    ('KZ', '+7'),  # Kazakhstan
    ('KE', '+254'),  # Kenya
    ('KI', '+686'),  # Kiribati
    ('KP', '+850'),  # North Korea
    ('KR', '+82'),  # South Korea
    ('KW', '+965'),  # Kuwait
    ('KG', '+996'),  # Kyrgyzstan
    ('LA', '+856'),  # Laos
    ('LV', '+371'),  # Latvia
    ('LB', '+961'),  # Lebanon
    ('LS', '+266'),  # Lesotho
    ('LR', '+231'),  # Liberia
    ('LY', '+218'),  # Libya
    ('LI', '+423'),  # Liechtenstein
    ('LT', '+370'),  # Lithuania
    ('LU', '+352'),  # Luxembourg
    ('MK', '+389'),  # North Macedonia
    ('MG', '+261'),  # Madagascar
    ('MW', '+265'),  # Malawi
    ('MY', '+60'),  # Malaysia
    ('MV', '+960'),  # Maldives
    ('ML', '+223'),  # Mali
    ('MT', '+356'),  # Malta
    ('MH', '+692'),  # Marshall Islands
    ('MR', '+222'),  # Mauritania
    ('MU', '+230'),  # Mauritius
    ('MX', '+52'),  # Mexico
    ('FM', '+691'),  # Micronesia
    ('MD', '+373'),  # Moldova
    ('MC', '+377'),  # Monaco
    ('MN', '+976'),  # Mongolia
    ('ME', '+382'),  # Montenegro
    ('MA', '+212'),  # Morocco
    ('MZ', '+258'),  # Mozambique
    ('MM', '+95'),  # Myanmar
    ('NA', '+264'),  # Namibia
    ('NR', '+674'),  # Nauru
    ('NP', '+977'),  # Nepal
    ('NL', '+31'),  # Netherlands
    ('NZ', '+64'),  # New Zealand
    ('NI', '+505'),  # Nicaragua
    ('NE', '+227'),  # Niger
    ('NG', '+234'),  # Nigeria
    # ... (Add more countries as needed)
}
    
    firstname = models.CharField(max_length=30, validators=[RegexValidator(regex='^[a-zA-z]*$', message='No numbers allowed in your firstname', code='invalid_firstname')])
    lastname = models.CharField(max_length=30, validators=[RegexValidator(regex='^[a-zA-z]*$', message='No numbers allowed in your lastname', code='invalid_lastname')])
    username = models.CharField(max_length=30, unique=True)
    country_code = models.CharField(max_length=5, choices=PHONE_CODES,default='NG',)
    phone = models.CharField(max_length=11, unique=True, validators=[RegexValidator(regex=r'^\+?1?\d{9,14}$',message='Enter a valid phone number.',code='invalid_phone_number')])
    email = models.EmailField(unique=True, primary_key=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, null=True)
    password = models.CharField(max_length=128)

    def __str__(self):
            return f"{self.firstname} {self.lastname}, {self.username}"