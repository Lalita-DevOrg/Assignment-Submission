import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'})



def tracker(url, TrackingPrice):
    page = requests.get(url,headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')

# product title
    for title in soup.find_all("span", class_="B_NuCI"):
        print(title.get_text())
# to prevent script from crashing when there isn't a price for the product
    try:
     for price in soup.find_all("div", class_="_30jeq3 _16Jk6d"):
         priceFlipkart =float(price.get_text().replace('₹', '').replace(',', ''))
    except:
        priceFlipkart = ''     

    if(priceFlipkart <= float(TrackingPrice.replace(',', ''))):
        send_email(url)

def send_email(url):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('lalitasgawas@gmail.com','tjxeiyjkcpqdiaid')

    subject = 'Price fell down'
    body = 'Check the link '+url
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail('lalitasgawas@gmail.com','lalitasgawas@gmail.com',msg)
    server.quit()

# imports a csv file with the url's to scrape
prod_tracker = pd.read_csv(r'C:\Users\Lalita Gawas\Documents\Trailhead Practices\DSA\Product_Trackers.csv', sep=',')
for i in range(0, len(prod_tracker["url"])):
    tracker(prod_tracker["url"][i],prod_tracker["TrackingPrice"][i])
    