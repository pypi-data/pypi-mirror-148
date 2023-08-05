import smtplib
import ssl
from threading                              import Thread


class SendWishEmail(Thread):

    def __init__(self, wish_type, birth_employees, **kwargs):
        super(SendWishEmail, self).__init__()
        self.OUTGOING_PORT   = 587
        self.EMAIL_SERVER    = 'smtp.gmail.com'
        self.birth_employees = birth_employees
        self.ann_employees   = kwargs.get('anniversary_employees')
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
        print(f"EMAIL_SERVER  = {self.EMAIL_SERVER}")
        print(f"OUTGOING_PORT = {self.OUTGOING_PORT}\n")
        print("*****  PLEASE YOUR SERVER AND PORT YOU'D LIKE TO USE DIFFERENT ONES.\n")

        input_server = input('Please your mail server:      ')
        input_port   = input('Please your mail SMTP Port:      \n')

        if input_server:
            self.EMAIL_SERVER = input_server
        if input_port:
            self.OUTGOING_PORT = int(input_port)

        email_address     = input('Enter the sender email:   ')
        email_password    = input('Enter the sender Password:   ')
        rcv_email_address = input('Enter the receiver Email:   ')

        # Create a secure SSL context
        ssl_context = ssl.create_default_context()

        if not email_address or not email_password or not rcv_email_address:
            print("\nSENDER'S EMAIL & PASSWORD, AND RECEIVER EMAIL ARE REQUIRED!")
            print('EMAIL NOT SENT !!!')
            return

        with smtplib.SMTP(self.EMAIL_SERVER, self.OUTGOING_PORT) as wish_server:
            wish_server.ehlo()
            wish_server.starttls(context=ssl_context)
            wish_server.ehlo()

            wish_server.login(email_address, email_password)

            subject = f"{self.title} wishes."
            body    = f"Happy {self.title} {self.employees}"
            msg     = f"Subject: {subject}\n\n{body}"

            wish_server.sendmail(email_address, rcv_email_address, msg)
            print('EMAIL SENT **********')
