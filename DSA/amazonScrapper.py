import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib



HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'})

class ProductData:
     def __init__(self, price, url, index):
         self.price = price
         self.index = index
         self.url = url
    
     def tracker(self):
        page = requests.get(self.url,headers=HEADERS)
        soup = BeautifulSoup(page.content, 'html.parser')

        # product title
        for title in soup.find_all("span", class_="B_NuCI"):
            prodName = title.get_text()

        # to prevent script from crashing when there isn't a price for the product
        try:
            for priceVar in soup.find_all("div", class_="_30jeq3 _16Jk6d"):
                priceFlipkart =float(priceVar.get_text().replace('₹', '').replace(',', ''))
        except:
            priceFlipkart = ''     

        trackingPrice = float(self.price.replace(',', ''))
        if (priceFlipkart <= trackingPrice):
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.ehlo()
            server.starttls()
            server.ehlo()

            server.login('lalitasgawas@gmail.com','tjxeiyjkcpqdiaid')

            subject = 'Price fell down'
            body = 'Check the link '+self.url
            msg = f"Subject: {subject}\n\n{body}"

            server.sendmail('lalitasgawas@gmail.com','lalitasgawas@gmail.com',msg)
            server.quit()

            
            tracker_log = pd.DataFrame()
            log = pd.DataFrame({'url':self.url,
            "Price": self.price,
            "Title": prodName},index=[self.index])
            lastHistory = pd.read_excel(r'C:\Users\Lalita Gawas\Documents\Trailhead Practices\DSA\SearchHistory.xlsx')
            final_df = lastHistory.append(log, sort = False) 
            final_df.to_excel(r'C:\Users\Lalita Gawas\Documents\Trailhead Practices\DSA\SearchHistory.xlsx', index = False, header=True)


# imports a csv file with the url's to scrape
prod_tracker = pd.read_csv(r'C:\Users\Lalita Gawas\Documents\Trailhead Practices\DSA\Product_Trackers.csv', sep=',')
for i in range(0, len(prod_tracker["url"])):
    prod = ProductData(prod_tracker["TrackingPrice"][i],prod_tracker["url"][i],i)
    prod.tracker()








    