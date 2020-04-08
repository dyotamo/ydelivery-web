import os

from lib.telerivet import API


def send_sms(contact, message):
    tr = API(os.environ['TELERIVET_API_SECRET'])
    project = tr.initProjectById(os.environ['TELERIVET_PROJECT_ID'])
    project.sendMessage(content=message, to_number=contact)
