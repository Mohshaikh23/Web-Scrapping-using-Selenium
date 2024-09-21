from bs4 import BeautifulSoup
import pandas as pd


with open("data/laptop0.html",'r',encoding='utf-8') as f:
    html_doc = f.read()
soup = BeautifulSoup(html_doc,"html.parser")
delivery_doc  = soup.find("div",attrs={'class':"a-row a-size-base a-color-secondary s-align-children-center"})
Delivery = delivery_doc.find('span',attrs={'class':'a-color-base'}).get_text().strip()
delivery_date = delivery_doc.find('span',attrs={'class':'a-color-base a-text-bold'}).get_text().strip()
