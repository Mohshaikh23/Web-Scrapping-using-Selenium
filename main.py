import streamlit as st
import pandas as pd
import plotly.express as px
from app import data_extractor,data_preprocessor,display_file_data,create_product_grid, stats,product_anlaysis
import os

# Title of the app
st.title("Amazon Web Scraper and Statistical Analysis")

# Create a session state for storing data
if 'df' not in st.session_state:
    st.session_state['df'] = None  # Initialize as None

# Sidebar input
with st.sidebar:
    st.header("Product Search")
    product = st.text_input('Enter the product name', '')
    num = st.number_input("Enter the number of pages required to scrape", 1, 50)
    product_search = st.button("Submit")
    library = st.button('Library')
    
# Cache the conversion of DataFrame to CSV for better performance
@st.cache_data
def convert_df(df):
    return df.to_csv().encode("utf-8")

saved_data_path = "saved_data"

# Check if the product search button is clicked
if product_search:
    if product.strip():  # Ensure product name is not empty
        try:
            data = data_extractor(product, num)
            data = data_preprocessor(data)
            if not data.empty:
                df = pd.DataFrame(data)
                
                # Ensure the saved_data directory exists
                os.makedirs('saved_data', exist_ok=True)
                
                df.to_csv(f"saved_data/{product}_data.csv", index=False)
                
                st.session_state['df'] = df  
                # Store the scraped data in session state
                
                st.subheader(f"Search Results for: {product}")
                st.download_button(
                    label='Download CSV',
                    data=df.to_csv(index=False),
                    file_name=f'{product}_scraped_data.csv',
                    mime='text/csv'
                )
                create_product_grid(df)
            else:
                st.warning("No data was found for the search term.")
        except ZeroDivisionError:
            st.error(f'Number is not divisible by 0')
    else:
        st.warning("Please enter a product name to search.")

def get_file_from_user(saved_data_path):
    """Function to get a file from the user and return the dataframe."""
    # Check if the path exists
    if os.path.exists(saved_data_path):
        # List all files in the directory
        files = os.listdir(saved_data_path)
        if files:
            file = st.selectbox("Choose a file", files,index=None)
            if file:
                return file
            else:
                st.warning("No file selected.")
        else:
            st.warning(f"No files found in the '{saved_data_path}' directory.")
    else:
        st.error(f"'{saved_data_path}' directory not found.")
    return None

# Main Streamlit logic
file = get_file_from_user(saved_data_path)

if file:
    st.text(f"Selected file: {file}")
    c1,c2,c3 = st.columns(3)
    load_file = c1.button('Load Selected File')
    Stats = c2.button('Stats')
    Product_anlaysis = c3.button('Analysis')
    

    if load_file:
        display_file_data(file)
            
    if Stats:
        stats()


    if Product_anlaysis:
        product_anlaysis()