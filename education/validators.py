from rest_framework.serializers import ValidationError


VALID_SERVICES = 'youtube'


class LinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        link_value = value.get(self.field, '')
        if VALID_SERVICES not in link_value.lower():
            raise ValidationError('Invalid link')
