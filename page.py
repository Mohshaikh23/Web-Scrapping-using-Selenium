import streamlit as st
import os
import pandas as pd
from bs4 import BeautifulSoup

# Web Scraping data path (assumes you've already scraped and saved data to "data" directory)
data_path = "data"
scraped_data = {"title": [], "link": [], "price": [], "image": [], "rating": []}

# Extracting the data from HTML files
for file in os.listdir(data_path):
    try:
        with open(f"{data_path}/{file}", "r", encoding="utf-8") as f:
            html_doc = f.read()
        soup = BeautifulSoup(html_doc, "html.parser")
        
        # Extracting required fields
        title = soup.find("h2").get_text() if soup.find("h2") else 'N/A'
        link = f'https://amazon.in/' + soup.find("h2").find("a")['href'] if soup.find("h2") else 'N/A'
        price = soup.find("span", class_='a-price-whole').get_text() if soup.find("span", class_='a-price-whole') else 'N/A'
        image_container = soup.find('div', class_='s-product-image-container')
        img_tag = image_container.find('img', class_='s-image')['src'] if image_container else 'N/A'
        rating = soup.find('span', class_='a-icon-alt').get_text() if soup.find('span', class_='a-icon-alt') else 'N/A'
        
        # Storing data in dictionary
        scraped_data["title"].append(title)
        scraped_data["link"].append(link)
        scraped_data["price"].append(price)
        scraped_data["image"].append(img_tag)
        scraped_data["rating"].append(rating)
    
    except Exception as e:
        st.error(f"Error processing {file}: {e}")

# Converting the data into a pandas DataFrame
df = pd.DataFrame(scraped_data)

# Display the scraped data using Streamlit
st.title('Amazon Laptop Scraper')
st.write("This is the data extracted from Amazon:")

# Display the data in a table
st.dataframe(df)

# Provide an option to download the data as CSV
st.download_button(label='Download CSV', data=df.to_csv(index=False), file_name='scraped_data.csv', mime='text/csv')

# Display images (if any available)
st.subheader('Images:')
for img_url in df['image']:
    if img_url != 'N/A':
        st.container(height=200)
        st.image(img_url, width=150)