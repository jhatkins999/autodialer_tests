from twilio.twiml.messaging_response import MessagingResponse

# This requires us to have the front end system first
# Add after creating the front end system


def sms_reply(message):
    resp = MessagingResponse()
    resp.message(message)

    return str(resp)
