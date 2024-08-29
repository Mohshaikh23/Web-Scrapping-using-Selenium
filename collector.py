from bs4 import BeautifulSoup
import pandas as pd
import os

data = {"title":[],"link":[],"price":[],"image":[],"rating":[]}

for file in os.listdir("data"):
    # Exception handling
    try:
        with open(f"data/{file}") as f:
            html_doc = f.read()
        soup = BeautifulSoup(html_doc,"html.parser")
        

        title = soup.find("h2").get_text()
        link =f'https://amazon.in/'+ soup.find("h2").find("a")['href']
        price = soup.find("span",attrs={'class':'a-price-whole'}).get_text()
        image_container = soup.find('div', class_='s-product-image-container')
        img_tag = image_container.find('img', class_='s-image')['src']
        rating = soup.find('span', class_='a-icon-alt').get_text()


        #Storing the data into dictionary
        data["title"].append(title)
        data["link"].append(link)
        data["price"].append(price)
        data["image"].append(img_tag)
        data["rating"].append(rating)
        
        
        #convertingthe extarcted data into dataframe
        df = pd.DataFrame(data)

        # Storing the extracted data into csv file
        df.to_csv('Data.csv')

    except Exception as e:
        print(e)
