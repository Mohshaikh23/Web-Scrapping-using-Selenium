from bs4 import BeautifulSoup
import pandas as pd
import os

data = {"title":[],"link":[],"price":[]}

for file in os.listdir("data"):
    try:
        with open(f"data/{file}") as f:
            html_doc = f.read()
        soup = BeautifulSoup(html_doc,"html.parser")
        
        title = soup.find("h2").get_text()
        link =f'https://amazon.in/'+ soup.find("h2").find("a")['href']
        price = soup.find("span",attrs={'class':'a-price-whole'}).get_text()
        data["title"].append(title)
        data["link"].append(link)
        data["price"].append(price)
        df = pd.DataFrame(data)
        df.to_csv('Data.csv')
    except Exception as e:
        print(e)
