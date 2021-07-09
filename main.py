import os
import time
from mailer import Mailer
import json
import requests
from requests.structures import CaseInsensitiveDict
from termcolor import colored
from requests_html import HTMLSession
from dotenv import load_dotenv


load_dotenv()
PASSWORD = os.getenv('PASSWORD')

class ListingBot():
    def __init__(self) -> None:
        self.headers = CaseInsensitiveDict()
        self.headers["accept"] = "application/json"
        self.userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
    
    def main(self):
        # HITBTC
        hitBTC = False
        resp = requests.get("https://api.hitbtc.com/api/2/public/currency?currencies=ETL", headers=self.headers)

        if resp.status_code == 200 and resp.json() != []:
            hitBTC = True

        # PROBIT 
        probit = False
        resp = requests.get("https://api.probit.com/api/exchange/v1/currency", headers=self.headers)
        data = resp.json()
        for i in data['data']:
            if i['id'] == "ETL":
                probit = True
    
        # Bitcoin.com exchange
        btc = False
        resp = requests.get("https://api.exchange.bitcoin.com/api/2/public/currency?currencies=ETL", headers=self.headers)

        if resp.status_code == 200 and resp.json() != []:
            btc = True

        # Changelly
        chg = False
        session = HTMLSession()
        r = session.get('https://changelly.com/supported-currencies',headers={'User-Agent':self.userAgent})
        r.html.render()
        try:
            data = json.loads(r.html.find('script')[6].text)
            enabledTickers = data['props']['pageProps']['initialState']['currencies']['enabledTickers']
            for i in enabledTickers:
                if i == "etl":
                    chg = True
            
        except ValueError:
            pass

        print("Checked all exchanges !")
        temp = [hitBTC,probit,btc,chg]
        names = {0:'hitBTC',1:'probit',2:'bitcoin.com',3:'changelly'}

        msg = []
        for i in range(4):
            if temp[i]:
                msg.append(names[i])

        if msg != []:
            self.send_mail(" ,".join(msg))
            
    def send_mail(self, msg):
        mail = Mailer(email='tyagipratyaksh@gmail.com',
                    password=PASSWORD)

        mail.send(receiver=['tyagi.6@iitj.ac.in','swami.2@iitj.ac.in','aniketkesari007@gmail.com'],  # Email From Any service Provider
                subject='ETL Listing Update',
                message=f'ETL has been listed on this exchange -{msg}')


if __name__ == "__main__":
    sleep_time = 15 * 60  # Converting 15 minutes to seconds
    while True:
        bot = ListingBot()
        bot.main()
        print(colored("Waiting 15 mins..", "blue"))
        t = sleep_time
        while t:
            mins, secs = divmod(t, 60)
            timer = "{:02d}:{:02d}".format(mins, secs)
            print(colored(timer, "yellow"), end="\r")
            time.sleep(1)
            t -= 1
