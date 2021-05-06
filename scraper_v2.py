import requests
import time
import smtplib

from bs4 import BeautifulSoup
from datetime import datetime

URL = ""
TIME_INTERVAL_IN_SECONDS=120

def send_email(msg):
    fromaddr = 'TOADDR@gmail.com'
    toaddrs  = ['FROMADDR@gmail.com']
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    
    server.login(fromaddr, "PASSWORD")
    server.sendmail(fromaddr, toaddrs, msg)

    server.quit()

def scrape_data():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    floors = soup.find_all("p", {"class": "floor_plan_name"})
    floors = [x.get_text().strip() for x in floors]
    
    return floors

old_data = scrape_data()

while True:
    # interval to keep checking
    time.sleep(TIME_INTERVAL_IN_SECONDS)
    try:
        new_data = scrape_data()
    # in case of network error don't crash
    except Exception as e:
        print(str(e))
        continue
    
    # check to see if there is any new data
    intersection = list(set(old_data) - set(new_data))

    curr_time = datetime.now().time()
    print("Checked changes and found: ",len(intersection),"\ttime: ",str(curr_time))

    # some changes have occured -> send email
    if len(intersection) > 0:
        old_data = new_data
        subject = 'PyBot Beep Boop, CHECK APT!'
        body = URL + "\n" + '\n'.join(intersection)
        msg = f"Subject: {subject}\n\n{body}"

        send_email(msg)
        
        
