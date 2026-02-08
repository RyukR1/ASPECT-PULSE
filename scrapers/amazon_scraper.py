import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_page_html(url):
    """
    Fetches the HTML content of a given URL.
    
    Args:
        url (str): The URL of the page to fetch.
        
    Returns:
        str: The HTML content of the page, or None if the request fails.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        print(f"Successfully fetched HTML from {url}")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def extract_reviews(html_content):
    """
    Extracts review text from the HTML of an Amazon product page.
    
    Args:
        html_content (str): The HTML content of the product page.
        
    Returns:
        pd.DataFrame: A DataFrame containing the reviews.
    """
    if not html_content:
        return pd.DataFrame()
        
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        # Find all review containers. The class names might change over time.
        reviews = soup.find_all('div', {'data-hook': 'review'})
        
        review_data = []
        print(f"Found {len(reviews)} reviews on the page.")
        
        for review in reviews:
            # Extract the main review text
            review_body = review.find('span', {'data-hook': 'review-body'})
            if review_body:
                review_text = review_body.get_text(strip=True)
                review_data.append({'review_text': review_text})
                
        df = pd.DataFrame(review_data)
        return df
    except Exception as e:
        print(f"Error extracting reviews: {e}")
        return pd.DataFrame()

if __name__ == '__main__':
    # Example: Scrape reviews for a Samsung Galaxy S23
    # Note: This URL points to the reviews page. You might need to update it.
    PRODUCT_URL = "https://www.amazon.com/Samsung-Galaxy-S23-SM-S918B-DS/product-reviews/B0BN222X3S/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    
    print(f"Starting Amazon scraper for product: {PRODUCT_URL}")
    
    html = get_page_html(PRODUCT_URL)
    
    if html:
        reviews_df = extract_reviews(html)
        
        if not reviews_df.empty:
            print("\n--- Sample of fetched reviews ---")
            print(reviews_df.head())
            
            # Save to CSV
            output_path = '../data/amazon_reviews_samsung_s23.csv'
            reviews_df.to_csv(output_path, index=False)
            print(f"\nReviews saved to {output_path}")
        else:
            print("No reviews were extracted. The website structure may have changed.")
    else:
        print("Failed to fetch the product page.")
