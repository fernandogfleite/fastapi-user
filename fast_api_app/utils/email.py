import yagmail
from decouple import config


class Email(object):
    def __init__(self, subject, message, receiver_email):
        self.subject = subject
        self.message = message
        self.receiver_email = receiver_email
        self.yag = yagmail.SMTP(user=config(
            'SENDER_EMAIL'), password=config('PASSWORD'))

    def send_email(self):
        self.yag.send(
            to=self.receiver_email,
            subject=self.subject,
            contents=self.message
        )
