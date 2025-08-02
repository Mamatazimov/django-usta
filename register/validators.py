from django.core.exceptions import ValidationError

def validate_no_dash(value):
    if '-' in value:
        raise ValidationError('Username may not contain "-" character.')

