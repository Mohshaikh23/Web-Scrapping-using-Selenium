import os
import streamlit as st
import pandas as pd

saved_data_path = "saved_data"



def display_file_data(file_path):
    """Function to display data of the selected file."""
    df = pd.read_csv(os.path.join(saved_data_path, file_path))  # Assuming CSV, adapt as needed
    st.dataframe(df)
    return df

def analysis(df):
    """Analysis function to perform on the data."""
    st.write("Performing analysis on the dataset...")
    # Add your analysis logic here
    st.write(df.describe())  # Example analysis

# Main Streamlit logic
file = get_file_from_user(saved_data_path)

if file:
    st.text(f"Selected file: {file}")
    load_file = st.button('Load Selected File')
    analyze_file = st.button('Analyze File')

    if load_file:
        df = display_file_data(file)
    if analyze_file:
        df = display_file_data(file)
        analysis(df)
