# Amazon Web Scraper and Product Analysis

## Project Overview

This project is an Amazon product web scraper built using **Selenium** and a **Streamlit** dashboard for visualizing and analyzing product data. The primary purpose of this tool is to scrape product information from Amazon, analyze the data, and provide insights into the best products for reselling or affiliate marketing.

!["Loaded Data"](/Images/ss1.png)
!["Stats"](/Images/ss2.png)
!["Analysis"](/Images/ss5.png)

## Key Features

- **Web Scraper**: Automates the collection of product data from Amazon, such as title, price, rating, reviews count, MRP, delivery date, and image.
- **Data Preprocessing**: Handles missing data, converts strings to numeric formats, and extracts important attributes like `price`, `rating`, and `reviews count`.
- **Data Visualization**: Provides dynamic and interactive visualizations using Plotly and Streamlit.
- **Product Insights**: Includes multiple metrics such as Price-to-Rating Ratio, Best Seller Score, and more to identify the best products for reselling or affiliate marketing.

## Installation

### Requirements

1. Python 3.x
2. Web Scraping Dependencies:
   - `Selenium`
   - `BeautifulSoup`
3. Data Analysis and Visualization Libraries:
   - `Pandas`
   - `NumPy`
   - `Plotly`
   - `Streamlit`

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Mohshaikh23/Web-Scrapping-using-Selenium.git
   ```
2. Navigate to the project directory:
   ```bash
   cd your-repo-name
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage

### Web Scraper

1. The scraper collects the following product details from Amazon:

   - Title
   - Price
   - Rating
   - MRP
   - Reviews Count
   - Delivery Date
   - Product Image

   The scraped data is saved into a CSV file for further analysis.

### Data Preprocessing

Before analysis, the data undergoes preprocessing:

- Missing values (`N/A`) are replaced with `NaN` and removed.
- String-based prices, MRPs, and reviews are converted to numeric values for analysis.
- Ratings are extracted and standardized.

### Data Analysis & Visualizations

The Streamlit dashboard provides the following visualizations to help analyze product data:

- **Scatter Plot**: Price vs Rating, with review count as the size of the points.
- **Histograms**: Distribution of product ratings and prices.
- **Correlation Heatmap**: Shows correlations between price, rating, MRP, and reviews count.
- **Box and Violin Plots**: Show price distribution across different rating levels.
- **Sunburst Chart**: Visualizes the distribution of products by rating and price ranges.
- **Scatter Matrix**: Explores relationships between multiple product attributes.
- **Density Contour**: Displays density clusters for price vs rating.

### Key Metrics for Product Evaluation

1. **Price-to-Rating Ratio**:  
   Helps identify products with the best balance of price and quality.

   Formula:

   ```python
   data['price_to_rating_ratio'] = data['price'] / data['rating']
   ```

2. **Best Seller Score**:  
   Evaluates the best products to buy for reselling based on a combination of price, rating, and reviews count.

   Formula:

   ```python
   data['best_seller_score'] = (data['rating'] * data['Reviews_count']) / data['price']
   ```

## Visualizations

Here are some of the key visualizations provided by the dashboard:

- **Price vs Rating**: Shows how prices and ratings correlate.
- **Product Ratings Distribution**: Understand the spread of product ratings.
- **Price Distribution**: Analyze the spread of product prices across categories.
- **Correlation Heatmap**: Discover relationships between product attributes like price and reviews.
- **Box and Violin Plots**: Detailed price analysis for each rating group.
- **Sunburst Chart**: Break down products by rating and price range for easier selection.
- **Scatter Matrix**: Analyze multiple relationships simultaneously.
- **Density Contour Plot**: Shows dense clusters of product prices and ratings.

## Contributing

If you'd like to contribute to this project:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new pull request.

## License

This project is licensed under the MIT License.
