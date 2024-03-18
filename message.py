#create a account in https://console.twilio.com/ and use the credentais to send the message to mobile number
#pip install twilio 

import logging
from twilio.rest import Client

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Twilio credentials
account_sid = 'ur id'
auth_token = 'ur key'
twilio_phone_number = '+twilio number'
your_phone_number = 'recieving number'

# Function to send SMS
def send_sms(message):
    client = Client(account_sid, auth_token)
    client.messages.create(
        to=your_phone_number,
        from_=twilio_phone_number,
        body=message
    )

try:
    # Your main script code here
    # If an exception occurs, it will be logged
    raise Exception("This is a test exception")
except Exception as e:
    logging.error(f'An error occurred: {str(e)}')
    send_sms(f'Error in Python script: {str(e)}')
#BT6TB2PDV2Q9Y483AKSJ2ZVV   
