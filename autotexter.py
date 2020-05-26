from send_sms import *
import json
import requests
import datetime

apilink = 'localhost:8000'


class AutoTexter(object):
    def __init__(self, user_id, campaign_name):
        self.user = User(user_id)
        self.campaign = Campaign(campaign_name)

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
    def __init__(self, user_id):
        link = apilink+"/users/users/"  # Add correct API endpoint later
        jfile = requests.get(link, params={"ID" : user_id}).json
        fields = json.loads(jfile)
        self.ID = fields["ID"]
        assert(self.ID == user_id)
        self.name = fields["name"]
        self.email = fields["email"]
        self.permissions = fields["permissions"]


class Voter(object):
    def __init__(self, name):
        link = apilink+"/voters/voters"  # Add correct API endpoint later
        jfile = requests.get(link, params={"name" : name})
        fields = json.loads(jfile)
        self.name = fields['name']
        assert(self.name == name)
        self.number = fields['PhoneNumber']
        self.campaignKey = fields["ForeignKey"]


class Campaign(object):
    def __init__(self, name):
        link = apilink + "/campaigns"  # Add correct API endpoint later
        jfile = requests.get(link, params={"name": name})
        fields = json.loads(jfile)
        self.name = fields['name']
        assert(self.name == name)


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

    def update_API(self):



