from send_sms import *
import json
import datetime


class AutoTexter(object):
    def __init__(self, user, campaign):
        self.user = user
        self.campaign = campaign

    def send_message(self, voters: list, text, number, mass: bool):
        data = send_messages(voters, text, number)
        with open('log' + str(self.campaign.name) + str(datetime.date) + '.txt', 'w') as logfile:
            json.dump(data, logfile)
        logfile.close()
        contacts = []
        for i in range(len(data['voters'])):
            contacts.append(
                TextContact(data['date'][i], text, number, data['voters'][i].number, data['voters'][i],
                            self.user.foreign_key, mass)
            )
        return contacts

    def update_user(self):
        return self.user


class User(object):
    def __init__(self, json_data):  # maybe the init will be the proper api call instead
        pass


class Voter(object):  # maybe the init will be the proper api call instead
    def __init__(self, json_data):
        pass


class Campaign(object):  # maybe the init will be the proper api call instead
    def __init__(self, json_data):
        pass


class TextContact(object):
    def __init__(self, timestamp, body, sender, receiver, voter, user_key, mass):
        self.timestamp = timestamp
        self.body = body
        self.sender = sender
        self.receiver = receiver
        self.voter = voter
        self.user_key = user_key
        self.mass = mass

    def output_json(self):
        data = {
            'timestamp' : self.timestamp,
            'body'      : self.body,
            'sender'    : self.sender,
            'receiver'  : self.receiver,
            'voter'     : self.voter,
            'user_key'  : self.user_key,
            'mass'      : self.mass
        }
        return json.dump(data)
