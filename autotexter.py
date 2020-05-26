from send_sms import *
import json
import requests
import datetime
from recieve_sms import *

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
                            self.user.id, mass)
            )
        return contacts

    def message_reply(self, voter, user, text, number): # Find out methods related to messaging response
        sms_reply(text)
        return TextContact(datetime.datetime, text, number, voter.number, voter,
                            self.user_id, False)


class User(object):
    def __init__(self, user_id):
        link = apilink+"/users/users/"+str(user_id)
        jfile = requests.get(link, params={"id" : user_id}).json
        fields = json.loads(jfile)
        self.id = user_id
        self.url = fields['url']
        self.username = fields['username']
        self.first_name = fields['first_name']
        self.last_name = fields['last_name']
        self.email = fields['email']
        self.groups = fields['groups']
        self.is_superuser = fields['is_superuser']
        self.is_staff = fields['is_staff']


class Voter(object):
    def __init__(self, voter_id):
        link = apilink+"/campaigns/voters/"+str(voter_id)
        jfile = requests.get(link, params={"id" : voter_id})
        fields = json.loads(jfile)
        self.id = voter_id
        self.name = fields["name"]
        self.number = fields['phone_number']
        self.campaignKey = fields["campaign"]


class Campaign(object):
    def __init__(self, id):
        link = apilink + "/campaigns/campaigns/"+str(id)
        jfile = requests.get(link, params={"id": id})
        fields = json.loads(jfile)
        self.id = id
        self.name = fields['name']


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
            'timestamp_sms' : self.timestamp,
            'body'          : self.body,
            'sender'        : self.sender,
            'receiver'      : self.receiver,
            'voter'         : self.voter.name,
            'user'          : self.user_key,
            'mass'          : self.mass
        }
        json.dump(data, "temp.txt")
        return json.load('temp.txt')

    def update_API(self):
        link = apilink+'/autodialer/sms_contacts/'
        jfile = self.output_json()
        r = requests.post(ur=link, data=jfile)
        return r




