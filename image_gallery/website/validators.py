from django.core.exceptions import ValidationError
from django.utils import timezone as tz

def deny_future_date(value):
    if value > tz.now().date():
        raise ValidationError('Please select a valid date.')
