import streamlit as st
import pandas as pd
from app import data_extractor,create_product_grid
import os

# Title of the app
st.title("Amazon Web Scraper")

# Sidebar input
with st.sidebar:
    st.header("Product Search")
    product = st.text_input('Enter the product name', '')
    product_search = st.button("Submit")

    library = st.button('Library')


# Check if the product search button is clicked
if product_search:
    if product.strip():  # Ensure product name is not empty or just spaces
        try:
            # Call the data_extractor function and pass the product
            data = data_extractor(product)
            if data:  # Ensure data is not empty
                df = pd.DataFrame(data)
                df.to_csv(f"saved_data/{product}_data.csv",index=False)
                # Display the extracted data in a table
                st.subheader(f"Search Results for: {product}")
                # st.dataframe(df)
                # Provide an option to download the data as CSV
                st.download_button(
                    label='Download CSV',
                    data=df.to_csv(index=False),
                    file_name=f'{product}_scraped_data.csv',
                    mime='text/csv'
                )

                create_product_grid(df)
            else:
                st.warning("No data was found for the search term.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a product name to search.")

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")

# Function to display the selected file data
def display_file_data(file):
    try:
        # Try to read the selected file into a DataFrame
        df = pd.read_csv(f'saved_data/{file}')
        
        # Debugging: Show the shape and first few rows of the DataFrame
        st.write(f"{df.shape[0]} Items fetched")

        # Show the DataFrame in a Streamlit table
        csv = convert_df(df)
        # st.dataframe(df)
        st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name=f"{file}.csv",
                    )

        # Call the grid creation function (if defined)
        if 'create_product_grid' in globals():
            create_product_grid(df)
        else:
            st.warning("Function 'create_product_grid' is not defined.")
    except Exception as e:
        st.error(f"Error loading file: {e}")

# Check if "saved_data" directory exists
if os.path.exists("saved_data"):
    # List all files in "saved_data"
    lst = os.listdir("saved_data")

    if lst:
        # Create a selectbox to choose a file
        file = st.selectbox("Choose a file", lst)

        if file:  # Ensure that a file is selected
            st.text(f"Selected file: {file}")

            # Add a button to trigger file display
            if st.button("Load Selected File"):
                display_file_data(file)  # Call the function to display the file data
        else:
            st.warning("No file selected.")
    else:
        st.warning("No files found in the 'saved_data' directory.")
else:
    st.error("'saved_data' directory not found.")