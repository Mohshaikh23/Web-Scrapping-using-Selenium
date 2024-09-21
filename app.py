from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import streamlit as st
# from streamlit_extras.stylable_container import stylable_container
import time

# Function for Data Extraction
def data_extractor(product):
    driver = webdriver.Chrome()
    data = {
        "title": [],
        "link": [], 
        "price": [],
        "rating": [],
        "MRP": [],
        "Reviews_count": [],
        "discount_percentage": [],
        "Delivery": [],
        "delivery_date": [],
        "image": []  # Add the 'image' key to store image URLs
    }

    for i in range(1, 2):
        driver.get(f"https://www.amazon.in/s?k={product}&page={i}&crid=1895KSWNLJ6QB&sprefix={product}%2Caps%2C349&ref=nb_sb_noss_1")
        
        elems = driver.find_elements(By.CLASS_NAME, "puis-card-container")
        for elem in elems:
            d = elem.get_attribute("outerHTML")
            soup = BeautifulSoup(d, "html.parser")
            
            # Safely extract each field with checks to prevent 'NoneType' errors
            title_tag = soup.find("h2")
            title = title_tag.get_text() if title_tag else "N/A"
            
            link_tag = soup.find("h2").find("a") if title_tag else None
            link = f'https://amazon.in/' + link_tag['href'] if link_tag else "N/A"
            
            price_tag = soup.find("span", attrs={'class': 'a-price-whole'})
            price = price_tag.get_text() if price_tag else "N/A"
            
            mrp_tag = soup.find("span", class_="a-price a-text-price")
            mrp = mrp_tag.find("span", class_="a-offscreen").get_text().replace("₹","") if mrp_tag else "N/A"
            
            reviews_tag = soup.find("span", attrs={'class': 'a-size-base s-underline-text'})
            reviews_count = reviews_tag.get_text() if reviews_tag else "N/A"
            
            rating_tag = soup.find('span', class_='a-icon-alt')
            rating = rating_tag.get_text() if rating_tag else "N/A"
            
            discount_tag = soup.find("span", string=lambda x: x and "%" in x)
            discount_percentage = discount_tag.get_text().replace("(", "").replace(")", "").strip() if discount_tag else "N/A"
            
            image_container = soup.find('div', class_='s-product-image-container')
            img_tag = image_container.find('img', class_='s-image') if image_container else None
            img_src = img_tag['src'] if img_tag else "N/A"

            delivery_tag   = soup.find("div",attrs={'class':"a-row a-size-base a-color-secondary s-align-children-center"})
            Delivery = delivery_tag .find('span',attrs={'class':'a-color-base'}).get_text().strip() if delivery_tag  else "N/A"
            delivery_date = delivery_tag .find('span',attrs={'class':'a-color-base a-text-bold'}).get_text().strip() if delivery_tag  else "N/A"

            # Storing the data into the dictionary
            data["title"].append(title)
            data["link"].append(link)
            data["price"].append(price)
            data["rating"].append(rating)
            data["MRP"].append(mrp)
            data["Reviews_count"].append(reviews_count)
            data["discount_percentage"].append(discount_percentage)
            data["Delivery"].append(Delivery)
            data["delivery_date"].append(delivery_date)
            data["image"].append(img_src)  
            
    time.sleep(2)
    driver.close()
    return data

def create_product_grid(df):
    cols = 3  # Number of columns
    rows = len(df) // cols + (1 if len(df) % cols > 0 else 0)

    for row in range(rows):
        columns = st.columns(cols)
        for col in range(cols):
            index = row * cols + col
            if index < len(df):
                with columns[col]:
                    with st.container(height=300):
                        st.image(df['image'][index], 
                            #  caption=df['title'][index], 
                            use_column_width="auto"
                            )
                    st.write(f"**Product:** {df['title'][index]}")
                    c1,c2 = st.columns(2)
                    with c1:
                        st.write(f"**Price:** {df['price'][index]}")
                        st.write(f"**Reviews:** {df['Reviews_count'][index]}")
                        st.write(f"**Delivery:** {df['Delivery'][index]}")
                    with c2:
                        st.write(f"**MRP:** {df['MRP'][index]}")
                        st.write(f"**Discount:** {df['discount_percentage'][index]}")
                        st.write(f"**Delivery Date:** {df['delivery_date'][index]}")
                    st.write(f"**Rating:** {df['rating'][index]}")
                    
                    # st.button(f"[Copy Link]({df['link'][index]})")
