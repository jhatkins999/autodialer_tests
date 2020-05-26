from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACb3cc029d14a5c2dccfaa71b9036309bc'
auth_token = '57f5a6b74554f21b815ca61b597a6fbf'
client = Client(account_sid, auth_token)
rodda = '+19176134279'
jacob = '+16514922091'
ny_num = '+19175400288'


def send_messages(voters, text, number):
    dates = []
    statuses = []
    errors = []
    prices = []
    for voter in voters:
        message = client.messages.create(
            body=text,
            from_=number,
            to=voter.number
        )
        statuses.append(message.status)
        errors.append(message.error_code)
        prices.append(message.price)
        dates.append(message.date_sent)

    return {'voters' : voters,
            'number' : number,
            'status' : statuses,
            'error'  : errors,
            'price'  : prices,
            'date'   : dates
            }
