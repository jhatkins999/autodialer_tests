from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACb3cc029d14a5c2dccfaa71b9036309bc'
auth_token = '57f5a6b74554f21b815ca61b597a6fbf'
client = Client(account_sid, auth_token)
rodda = '+19176134279'
jacob = '+16514922091'
ny_num = '+19175400288'
for num in [rodda, jacob]:
    message = client.messages.create(
                     body="This is a text to %s" %num,
                     from_= ny_num,
                     to=num
                 )
    print(message.sid)

# call = client.calls.create(
#                         twiml='<Response><Say>Ahoy, World!</Say></Response>',
#                         to=jacob,
#                         from_=ny_num
#                     )

# print(call.sid)
