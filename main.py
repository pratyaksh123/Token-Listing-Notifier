import os
from mailer import Mailer
from dotenv import load_dotenv

load_dotenv()
PASSWORD = os.getenv('PASSWORD')
mail = Mailer(email='tyagipratyaksh@gmail.com',
              password=PASSWORD)

mail.send(receiver='tyagi.6@iitj.ac.in',  # Email From Any service Provider
          subject='TEST',
          message='HI, This Message From Python :)')

print(mail.status)