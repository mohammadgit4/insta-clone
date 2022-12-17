from twilio.rest import Client
from django.conf import settings

def send_sms(bodytext, phone_no):
    Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN).messages.create(body=bodytext, to=phone_no, from_=settings.TWILIO_PHONE_NO)