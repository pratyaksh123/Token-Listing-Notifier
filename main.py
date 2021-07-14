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
    def __init__(self, count) -> None:
        self.count = count
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

        # P2pB2b exchange
        p2pb2p = False
        payload={}
        headers = {}

        response = requests.request("GET", url = "http://api.p2pb2b.io/api/v2/public/markets" , headers=headers, data=payload)
        data = response.json()
        if data['success']:
            for i in data['result']:
                if 'ETL' in i:
                    p2pb2p = True
                    break
        print(f"{self.count}. Checked all exchanges !")
        temp = [hitBTC,probit,btc,p2pb2p]
        names = {0:'hitBTC',1:'probit',2:'bitcoin.com',3:'p2pb2p'}

        msg = []
        for i in range(4):
            if temp[i]:
                msg.append(names[i])

        if msg != []:
            self.send_mail(" ,".join(msg))
            
    def send_mail(self, msg):
        mail = Mailer(email='tyagipratyaksh@gmail.com',
                    password=PASSWORD)

        mail.send(receiver=['tyagi.6@iitj.ac.in'],  # Email From Any service Provider
                subject='ETL Listing Update',
                message=f'ETL has been listed on this exchange -{msg}')


if __name__ == "__main__":
    sleep_time = 15 * 60  # Converting 15 minutes to seconds
    count = 0
    while True:
        bot = ListingBot(count)
        bot.main()
        print(colored("Waiting 15 mins..", "blue"))
        t = sleep_time
        while t:
            mins, secs = divmod(t, 60)
            timer = "{:02d}:{:02d}".format(mins, secs)
            print(colored(timer, "yellow"), end="\r")
            time.sleep(1)
            t -= 1
        count += 1
