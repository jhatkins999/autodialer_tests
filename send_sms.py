from twilio.rest import Client
import time

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
# Make sure to add security // I assume these will require an API call and be given based on the user permissions
account_sid = 'ACb3cc029d14a5c2dccfaa71b9036309bc'
auth_token = '57f5a6b74554f21b815ca61b597a6fbf'
client = Client(account_sid, auth_token)
rodda = '+19176134279'
jacob = '+16514922091'
ny_num = '+19175400288'


# We can only send max one message per second
def send_messages(voters, text, number):
    dates = []
    statuses = []
    errors = []
    prices = []
    delay = 1.01
    for voter in voters:
        start_time = time.time()
        message = client.messages.create(
            body=text,
            from_=number,
            to=voter.number
        )
        statuses.append(message.status)
        errors.append(message.error_code)
        prices.append(message.price)
        dates.append(message.date_sent)
        time.sleep(delay - time.time() + start_time)

    return {'voters': voters,
            'number': number,
            'text': text,
            'status': statuses,
            'error': errors,
            'price': prices,
            'date': dates
            }
