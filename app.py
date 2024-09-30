from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit as st
import numpy as np
import time
import pandas as pd
import os

# Function for Data Extraction
def data_extractor(product, num):
    driver = webdriver.Chrome()
    data = {
        "title": [],
        "link": [], 
        "price": [],
        "rating": [],
        "MRP": [],
        "Reviews_count": [],
        # "Delivery": [],
        "delivery_date": [],
        "image": []
    }

    for i in range(1, num+1):
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
            mrp = mrp_tag.find("span", class_="a-offscreen").get_text().replace("₹", "") if mrp_tag and mrp_tag.find("span", class_="a-offscreen") else "N/A"
            
            reviews_tag = soup.find("span", attrs={'class': 'a-size-base s-underline-text'})
            reviews_count = reviews_tag.get_text() if reviews_tag else "N/A"
            
            rating_tag = soup.find('span', class_='a-icon-alt')
            rating = rating_tag.get_text() if rating_tag else "N/A"
            
            image_container = soup.find('div', class_='s-product-image-container')
            img_tag = image_container.find('img', class_='s-image') if image_container else None
            img_src = img_tag['src'] if img_tag else "N/A"

            delivery_tag = soup.find("div", attrs={'class': "a-row a-size-base a-color-secondary s-align-children-center"})
            # Delivery = delivery_tag.find('span', attrs={'class': 'a-color-base'}).get_text().strip() if delivery_tag and delivery_tag.find('span', attrs={'class': 'a-color-base'}) else "N/A"
            delivery_date = delivery_tag.find('span', attrs={'class': 'a-color-base a-text-bold'}).get_text().strip() if delivery_tag and delivery_tag.find('span', attrs={'class': 'a-color-base a-text-bold'}) else "N/A"

            # Storing the data into the dictionary
            data["title"].append(title)
            data["link"].append(link)
            data["price"].append(price)
            data["rating"].append(rating)
            data["MRP"].append(mrp)
            data["Reviews_count"].append(reviews_count)
            # data["Delivery"].append(Delivery)
            data["delivery_date"].append(delivery_date)
            data["image"].append(img_src)  
            
    time.sleep(10)
    driver.close()
    return data

def data_preprocessor(df):
    if isinstance(df, dict):
        df = pd.DataFrame.from_dict(df)
        
    df.replace('N/A', np.nan, inplace=True)
    df = df.dropna()
    # Convert 'price' to float if it's in string format
    if df['price'].dtype == 'object':
        df['price'] = df['price'].str.replace(',', '').astype(float)

    # Convert 'MRP' to float if it's in string format
    if df['MRP'].dtype == 'object':
        df['MRP'] = df['MRP'].str.replace(',', '').astype(float)

    # Extract numeric ratings from 'rating' column if it's in string format
    if df['rating'].dtype == 'object':
        df['rating'] = df['rating'].astype(str).str.extract(r'(\d+\.\d+)').astype(float)
    
    # Convert 'MRP' to float if it's in string format
    if df['Reviews_count'].dtype == 'object':
        df['Reviews_count'] = df['Reviews_count'].str.replace(',', '').astype(int)
    
    return df


saved_data_path = "saved_data"

# Function to display the selected file data
def display_file_data(file):
    try:
        # Use the full path when reading the CSV file
        file_path = os.path.join(saved_data_path, file)
        df = pd.read_csv(file_path)

        st.session_state['df'] = df  # Store the loaded data in session state

        st.write(f"{df.shape[0]} Items fetched")

        # Allow CSV download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f"{file}",
            mime="text/csv"
        )
        # Call the grid creation function (if defined)
        if 'create_product_grid' in globals():
            create_product_grid(df)
        else:
            st.warning("Function 'create_product_grid' is not defined.")
    except Exception as e:
        st.error(f"Error loading file: {e}")


def create_product_grid(df):
    df = df.reset_index(drop=True)
    cols = 3  # Number of columns
    rows = len(df) // cols + (1 if len(df) % cols > 0 else 0)

    for row in range(rows):
        columns = st.columns(cols)
        for col in range(cols):
            index = row * cols + col
            if index < len(df):
                with columns[col]:
                    st.markdown(f"""
                        <div style="height: 300px; display: flex; align-items: center; justify-content: center;">
                            <img src="{df['image'][index]}" style="max-height: 100%; max-width: 100%;" />
                        </div>
                        """, unsafe_allow_html=True)

                    st.write(f"**Product:** {df['title'][index]}")
                    c1,c2 = st.columns(2)
                    with c1:
                        st.write(f"**Price:** {df['price'][index]}")
                        st.write(f"**Reviews:** {df['Reviews_count'][index]}")
                        # st.write(f"**Delivery:** {df['Delivery'][index]}")
                    with c2:
                        st.write(f"**MRP:** {df['MRP'][index]}")
                        st.write(f"**Delivery Date:** {df['delivery_date'][index]}")
                    st.write(f"**Rating:** {df['rating'][index]}")
                    
                    # st.button(f"[Copy Link]({df['link'][index]})")


def product_showcase(df, prod_num, attributes):
    # Define the number of columns per row
    columns_per_row = 5

    # Calculate the number of rows needed
    rows = (prod_num + columns_per_row - 1) // columns_per_row  # ceil(prod_num / columns_per_row)

    # Loop through each row
    for row in range(rows):
        # For each row, create the column layout
        columns = st.columns(min(columns_per_row, prod_num - row * columns_per_row))

        # Loop through each column in the current row
        for col_idx, col in enumerate(columns):
            index = row * columns_per_row + col_idx
            if index < prod_num:
                with col:
                    # Display the image with responsive height and width
                    st.container().markdown(f"""
                        <div style="height: 200px; display: flex; align-items: center; justify-content: center;">
                            <img src="{df['image'].iloc[index]}" style="max-height: 100%; max-width: 100%;" />
                        </div>
                        """, unsafe_allow_html=True)

                    # Add the title below the image
                    with st.container(height=200, border=None):
                        st.write(f"{df['title'].iloc[index]}")
                    
                    if attributes is not None:
                        # Dynamically display attributes
                        for attribute in attributes:
                            if attribute in df.columns:
                                st.write(f"**{attribute.capitalize()}:** {df[attribute].iloc[index]}")
                    else:
                        pass

def stats():
    df = st.session_state['df']  # Get the data from session state
    data = data_preprocessor(df)

    if not data.empty:
        st.header("Product Statistics")
        st.write(f"Out of {len(df)} products fetched from amazon, {len(df) - len(data)} products had null values")

        with st.container(height=60,border=1):
            c1,c2,c3,c4 = st.columns(4)
            c1.write(f"Total Products: {len(data)}")
            c2.write(f"Average Price: ₹{data['price'].mean():,.2f}")
            c3.write(f"Median Price: ₹{data['price'].median():,.2f}")
            c4.write(f"Average Rating: {data['rating'].mean():.2f} stars")
        
        #top 5 products on Amazon
        st.subheader("Top 5 products on Amazon Search")
        top_5 = data.head(5)
        product_showcase(top_5, 5,['price','MRP','Reviews_count','rating'])

        #High Reviewed Products
        st.subheader("High Reviewed Products")
        top_rated = data.sort_values(by='Reviews_count',ascending=False).head(5)
        product_showcase(top_rated,5,['price','MRP','Reviews_count','rating'])
        
         # Explanation for Price-to-Rating Ratio
        st.markdown("""
        ### Understanding the Price-to-Rating Ratio:

        The **Price-to-Rating Ratio** is a metric used to evaluate how much a product costs in relation to its customer satisfaction or quality, as reflected by its rating. It helps you determine the value a product offers based on its price and rating.

        - A **high Price-to-Rating Ratio** (higher cost per rating point) indicates that the product might be **overpriced** or that customers feel they are not getting enough value for the price they paid.
        - A **low Price-to-Rating Ratio** (lower cost per rating point) suggests the product provides **good value for money**, meaning it has a high rating relative to its price.

        """)
        #High Price-to-Rating Ratio
        st.subheader("High Price-to-Rating Ratio")
        data['price_to_rating_ratio'] = round(data['price'] / data['rating'],2)
        best_ratio = data.sort_values(by='price_to_rating_ratio',ascending=False)
        product_showcase(best_ratio, 5,['price','MRP','rating','price_to_rating_ratio'])
       
        #Low Price-to-Rating Ratio
        st.subheader("Low Price-to-Rating Ratio")
        data['price_to_rating_ratio'] = round(data['price'] / data['rating'],2)
        best_ratio = data.sort_values(by='price_to_rating_ratio',ascending=True)
        product_showcase(best_ratio, 5,['price','MRP','rating','price_to_rating_ratio'])

        # Balanced Price-to-Rating Ratio
        st.subheader("Balanced Price-to-Rating Ratio")
        data['price_to_rating_ratio'] = round(data['price'] / data['rating'], 2)
        sorted_data = data.sort_values(by='price_to_rating_ratio', ascending=True)
        middle_index = len(sorted_data) // 2
        balanced_ratio = sorted_data.iloc[middle_index-2:middle_index+3]
        product_showcase(balanced_ratio, 5, ['price', 'MRP', 'rating', 'price_to_rating_ratio'])
        
        #Price-to-Reviews Ratio
        st.subheader("Price to Review Ratio")
        st.markdown("""This metric indicates how much you are paying per review. A lower ratio might suggest a higher customer satisfaction per price paid""")
        data['price_to_reviews_ratio'] = round(data['price'] / data['Reviews_count'],2)
        sorted_data = data.sort_values(by='price_to_reviews_ratio', ascending=True)
        product_showcase(sorted_data, 5, ['price', 'Reviews_count', 'rating', 'price_to_reviews_ratio'])

        st.subheader('Discounted Products')
        st.markdown("""Calculating the discount offered between the MRP and the selling price to find heavily discounted products, which may attract buyers.""")

        #Top Discounted Products
        st.subheader("Top Discounted Products")
        data['discount_percentage'] = round(((data['MRP'] - data['price']) / data['MRP']) * 100,2)
        sorted_data = data.sort_values(by='discount_percentage', ascending=False)
        product_showcase(sorted_data, 5, ['price', 'MRP', 'rating','Reviews_count', 'discount_percentage'])

        #Least Discounted Products
        st.subheader("Least Discounted Products")
        sorted_data = data.sort_values(by='discount_percentage', ascending=True)
        product_showcase(sorted_data, 5, ['price', 'MRP', 'rating','Reviews_count', 'discount_percentage'])

        #Popularity Score
        st.subheader('Popularity Score')
        st.markdown("""Combining both the number of reviews and the average rating to determine how popular a product is.""")
        data['popularity_score'] = round(data['rating'] * data['Reviews_count'],2)
        sorted_data = data.sort_values(by='popularity_score', ascending=False)
        product_showcase(sorted_data, 5, ['price', 'MRP', 'rating','Reviews_count', 'popularity_score'])

        #Best Seller Score
        st.subheader('Best Seller Score')
        st.markdown("""
            The **Best Seller Score** is a comprehensive metric used to evaluate the best products for affiliate marketing or reselling. It combines key factors like **price**, **rating**, and **reviews count** into a single score.

            #### Formula:
            `Best Seller Score = (Price * 0.3) + (Rating * 0.4) + (Reviews Count * 0.3)`

            The formula normalizes each component to a scale of 0-1, with different weights applied to each factor:
            - **Price (30%)**: Products with lower prices score higher.
            - **Rating (40%)**: Higher ratings contribute more to the score, as customer satisfaction is crucial.
            - **Reviews Count (30%)**: A product with more reviews gains more trust and is likely more popular.

            This score helps you find the best balance between price, customer satisfaction, and product popularity.
            """)

        data['best_seller_score'] = round((data['price'] / data['price'].max()) * 0.3 + \
                            (data['rating'] / data['rating'].max()) * 0.4 + \
                            (data['Reviews_count'] / data['Reviews_count'].max()) * 0.3,2)

        sorted_data = data.sort_values(by='best_seller_score', ascending=False)
        product_showcase(sorted_data, 5, ['price', 'MRP', 'rating','Reviews_count', 'best_seller_score'])


    else:
        st.warning("No data available for analysis. Please load or scrape data first.")

def product_anlaysis():
    df = st.session_state['df']  # Get the data from session state
    df = data_preprocessor(df)

    if not df.empty:

        # Scatter Plot: Price vs Rating
        fig = px.scatter(df, x='price', y='rating', size='Reviews_count', hover_name='title',
                        color='rating', title='Price vs Rating (Size = Reviews Count)')
        
        st.markdown("""
            ### Scatter Plot: Price vs Rating (Size = Reviews Count)
            This scatter plot helps you visualize the relationship between price and rating. 
            - Each point represents a product, where the **x-axis** shows the product price and the **y-axis** shows the rating.
            - The **size of each point** is determined by the number of reviews, which gives an idea of how popular a product is.
            - By hovering over the points, you can identify specific products. Higher prices might not always correlate with better ratings, and the number of reviews adds a dimension of product credibility.
            """)
        st.plotly_chart(fig)

        # Histogram: Distribution of Product Ratings
        fig = px.histogram(df, x='rating', nbins=10, title='Distribution of Product Ratings',
                        color_discrete_sequence=['skyblue'])
        st.markdown("""
            ### Histogram: Distribution of Product Ratings
            This histogram shows the frequency distribution of product ratings.
            - It helps identify if most products have high, low, or moderate ratings. 
            - For example, a peak around 4.0 - 4.5 might suggest that most products are rated highly, while a wider spread indicates varied product quality.
            """)
        st.plotly_chart(fig)

        # Histogram: Price Distribution of Products
        fig = px.histogram(df, x='price', nbins=20, title='Price Distribution of Products',
                        color_discrete_sequence=['skyblue'])
        st.markdown("""
            ### Histogram: Price Distribution of Products
            This histogram visualizes the distribution of product prices.
            - It can help answer questions like, "Are most products clustered around a certain price range?" 
            - If there's a peak at lower price ranges, it could indicate that the majority of products are priced affordably, which could be appealing for reselling.
            """)
        st.plotly_chart(fig)

        # Heatmap: Correlation between price, rating, MRP, and Reviews_count
        corr = df[['price', 'rating', 'MRP', 'Reviews_count']].corr()
        fig = ff.create_annotated_heatmap(z=corr.values, x=corr.columns.tolist(), y=corr.columns.tolist(),
                                        colorscale='Blues', showscale=True)
        fig.update_layout(title='Correlation Heatmap')
        st.markdown("""
            ### Heatmap: Correlation Between Attributes
            This heatmap provides a correlation matrix between `price`, `rating`, `MRP`, and `Reviews_count`.
            - A value close to 1 indicates a strong positive correlation, while a value close to -1 indicates a strong negative correlation.
            - For example, if `price` and `MRP` have a high correlation, it indicates that higher MRP typically results in a higher price. Observing `Reviews_count` correlation with other attributes helps identify if more reviews are tied to better ratings.
            """)

        st.plotly_chart(fig)

        #Price Distribution by Rating
        fig = px.box(df, x='rating', y='price', title='Price Distribution by Rating',
             color='rating', points="all", color_discrete_sequence=px.colors.qualitative.Plotly)
        st.markdown("""
            ### Histogram: Distribution of Product Ratings
            This histogram shows the frequency distribution of product ratings.
            - It helps identify if most products have high, low, or moderate ratings. 
            - For example, a peak around 4.0 - 4.5 might suggest that most products are rated highly, while a wider spread indicates varied product quality.
            """)
        st.plotly_chart(fig)
        
        # Violin Plot: Price Distribution by Rating
        fig = px.violin(df, x='rating', y='price', box=True, points='all',
                 title='Price Distribution by Rating (Violin Plot)',
                 color='rating', color_discrete_sequence=px.colors.qualitative.Plotly)
        st.markdown("""
            ### Price Distribution by Rating (Violin Plot)
            This violin plot further explores the price distribution by rating, showing the density of product prices within each rating group.
            - The wider areas represent where prices are more densely populated. 
            - By comparing ratings, you can assess which ratings have more affordable or expensive products.
            """)
        st.plotly_chart(fig)

        # Sunburst Chart: Products by Rating and Price Ranges
        df['Price Range'] = pd.cut(df['price'], bins=[0, 50, 100, 150, 200, float('inf')], labels=['0-50', '50-100', '100-150', '150-200', '200+'])
        fig = px.sunburst(df, path=['rating', 'Price Range'], values='Reviews_count',
                        title='Distribution of Products by Rating and Price Ranges')
        st.markdown("""
            ### Sunburst Chart: Products by Rating and Price Ranges
            The sunburst chart offers a hierarchical view of product distribution based on rating and price range.
            - The **inner layer** represents product ratings, and the **outer layer** shows the price range for products within each rating.
            - This chart helps you understand how product prices are distributed across different ratings, which can guide pricing strategies.
            """)
        
        st.plotly_chart(fig)

        # Scatter Matrix: Exploring Relationships
        fig = px.scatter_matrix(df, dimensions=['price', 'rating', 'MRP', 'Reviews_count'],
                                title='Scatter Matrix of Product Attributes',
                                color='rating', color_continuous_scale=px.colors.sequential.Viridis)
        st.markdown("""
            ### Scatter Matrix: Exploring Relationships Between Attributes
            The scatter matrix shows the relationships between `price`, `rating`, `MRP`, and `Reviews_count`.
            - Each pair of variables is plotted against each other, allowing you to explore trends, outliers, or clusters. 
            - For instance, you can observe if products with more reviews tend to have higher prices or ratings.
            """)
        st.plotly_chart(fig)

        # Density Plot: Price Distribution
        fig = px.density_contour(df, x='price', y='rating', title='Density Contour of Price vs Rating',
                          color='rating',  # Use color to specify a variable
                        #   contours=dict(showlabels=True)
                          )  # Show contour labels
        st.markdown("""
            ### Density Contour: Price vs Rating
            This density contour plot highlights the concentration of products based on price and rating.
            - Darker areas represent regions where more products are clustered, helping you identify popular price points for different rating levels.
            - This can guide product selection by identifying the price range that aligns with high ratings.
            """)
        st.plotly_chart(fig)