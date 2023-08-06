import os
import smtplib
import ssl
import time

from dotenv                                 import load_dotenv
from threading                              import Thread


load_dotenv()

class SendWishEmail(Thread):

    def __init__(self, wish_type, employees_list, **kwargs):
        super(SendWishEmail, self).__init__()
        self.crontab         = kwargs.get('crontab')
        self.GMAIL_PORT      = os.getenv('GMAIL_PORT')
        self.GMAIL_SERVER    = os.getenv('GMAIL_SERVER')
        self.GMAIL_SENDER    = os.getenv('GMAIL_SENDER')
        self.GMAIL_PASSWORD  = os.getenv('GMAIL_PASSWORD')
        self.GMAIL_RECEIVER  = os.getenv('GMAIL_RECEIVER')
        self.birth_employees = employees_list
        self.ann_employees   = employees_list #kwargs.get('anniversary_employees')
        self.wish_type       = wish_type
        self.title           = 'Birthday'
        self.employees       = ','.join(self.birth_employees)
        if self.wish_type == '2':
            self.title = 'Work Anniversary'
            self.employees = ','.join(self.ann_employees)

    def run(self):
        self.send_generic_email()

    def send_generic_email(self):

        print("\n********** SENDING EMAIL ****************\n")
        print("SETTINGS ARE AS FOLLOWS:  \n")
        print(f"EMAIL_SERVER  = {self.GMAIL_SERVER}")
        print(f"OUTGOING_PORT = {self.GMAIL_PORT}\n")

        if not self.GMAIL_PORT or not self.GMAIL_SERVER or not self.GMAIL_SENDER or \
                not self.GMAIL_PASSWORD or not self.GMAIL_RECEIVER:
            print("*****  PLEASE ENTER YOUR SERVER AND PORT YOU'D LIKE TO USE DIFFERENT ONES.\n")

            input_server      = input('Please your mail server:      ')
            input_port        = input('Please your mail SMTP Port:      \n')
            email_address     = input('Enter the sender email:   ')
            email_password    = input('Enter the sender Password:   ')
            rcv_email_address = input('Enter the receiver Email:   ')

            if input_server:
                self.GMAIL_SERVER = input_server
            if input_port:
                self.GMAIL_PORT = int(input_port)
            if email_address:
                self.GMAIL_SENDER = email_address
            if email_password:
                self.GMAIL_PASSWORD = email_password
            if rcv_email_address:
                self.GMAIL_RECEIVER = rcv_email_address

            if not self.crontab and (not input_server or not input_port or not email_address or
                                     not email_password or not rcv_email_address):
                print("\nSENDER'S EMAIL & PASSWORD, AND RECEIVER EMAIL ARE REQUIRED!")
                print('EMAIL NOT SENT !!!\n')
                print('******** THANK YOU FOR USING OUR APP *********')
                time.sleep(1)
                return

        # Create a secure SSL context
        ssl_context = ssl.create_default_context()

        try:

            with smtplib.SMTP(self.GMAIL_SERVER, self.GMAIL_PORT) as wish_server:
                wish_server.ehlo()
                wish_server.starttls(context=ssl_context)
                wish_server.ehlo()

                wish_server.login(self.GMAIL_SENDER, self.GMAIL_PASSWORD)

                subject = f"{self.title} wishes."
                body = f"Happy {self.title} {self.employees}"
                msg = f"Subject: {subject}\n\n{body}"

                wish_server.sendmail(self.GMAIL_SENDER, self.GMAIL_RECEIVER, msg)
                print('EMAIL SENT **********\n')
                print('******** THANK YOU FOR USING OUR APP *********')
                time.sleep(1)

        except Exception as e:
            print('Trouble sending this email.')
            raise e
