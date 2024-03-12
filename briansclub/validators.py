from django.core.exceptions import ValidationError

def validate_ticket_reply(value):
    if 'spam' in value.lower():
        raise ValidationError('Reply contains spam words.')