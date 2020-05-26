from twilio.twiml.messaging_response import MessagingResponse
import time

# This requires us to have the front end system first
# Add after creating the front end system


def sms_reply(text, link):
    resp = MessagingResponse()
    resp.message(text)
    resp.redirect(link)

    return resp

