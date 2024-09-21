from bs4 import BeautifulSoup
import pandas as pd


data = {"title":[],
        "link":[], 
        "price":[],
        "rating":[],
        "MRP":[],
        "Reviews_count":[],
        "discount_percentage":[],
        "Delivery":[],
        "delivery_date":[],
        "image":[],
        }
    
# for file in os.listdir("data"):
    # Exception handling
try:
    with open("data/laptop0.html",'r',encoding='utf-8') as f:
        html_doc = f.read()
    soup = BeautifulSoup(html_doc,"html.parser")
    
    title = soup.find("h2").get_text()
    link =f'https://amazon.in/'+ soup.find("h2").find("a")['href']
    price = soup.find("span",attrs={'class':'a-price-whole'}).get_text()
    MRP = soup.find("span", class_="a-price a-text-price").find("span", class_="a-offscreen").get_text()
    reviews_count = soup.find("span",attrs={'class':'a-size-base s-underline-text'}).get_text()
    rating = soup.find('span', class_='a-icon-alt').get_text()
    discount_percentage = soup.find("span", string=lambda x: x and "%" in x).get_text()    
    image_container = soup.find('div', class_='s-product-image-container')
    if image_container:
        img_tag = image_container.find('img', class_='s-image')
        if img_tag:
            img_src = img_tag['src']
        else:
            img_src = None  # Handle case where img tag doesn't exist
    else:
        img_src = None  # Handle case where image container doesn't exist                rating = soup.find('span', class_='a-icon-alt').get_text()
    delivery_doc  = soup.find("div",attrs={'class':"a-row a-size-base a-color-secondary s-align-children-center"})
    Delivery = delivery_doc.find('span',attrs={'class':'a-color-base'}).get_text().strip()
    delivery_date = delivery_doc.find('span',attrs={'class':'a-color-base a-text-bold'}).get_text().strip()


    #Storing the data into dictionary
    data["title"].append(title)
    data["link"].append(link)
    data["price"].append(price)
    data["image"].append(img_tag)
    data["rating"].append(rating)
    data["MRP"].append(MRP)
    data["Reviews_count"].append(reviews_count)
    data["discount_percentage"].append(discount_percentage.replace("(", "").replace(")", "").strip())
    data["Delivery"].append(Delivery)
    data["delivery_date"].append(delivery_date)

   #convertingthe extarcted data into dataframe
    df = pd.DataFrame(data)
    print(df)
    # # Storing the extracted data into csv file
    df.to_csv('exampledata.csv')

except Exception as e:
    print(e)
