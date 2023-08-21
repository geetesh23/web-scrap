import requests
from bs4 import BeautifulSoup
import csv


def scrape_products(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_containers = soup.find_all('div', {'data-asin': True})
    
    products_data = []

    for container in product_containers:
        
        product_title_element = container.find('span', {'class': 'a-text-normal'})
        product_title = product_title_element.text.strip() if product_title_element else 'Title not available'
        
        
        product_price_element = container.find('span', {'class': 'a-offscreen'})
        product_price = product_price_element.text.strip() if product_price_element else 'Price not available'

        
        product_rating_element = container.find('span', {'class': 'a-icon-alt'})
        product_rating = product_rating_element.text.strip() if product_rating_element else 'Rating not available'

        
        num_reviews_element = container.find('span', {'class': 'a-size-base'})
        num_reviews = num_reviews_element.text.strip() if num_reviews_element else 'Number of reviews not available'

        
        link_element = container.find('a', {'class': 'a-link-normal'})
        product_url = "https://www.amazon.in" + link_element['href'] if link_element else 'URL not available'

        products_data.append({
            'Product URL': product_url,
            'Product Name': product_title,
            'Product Price': product_price,
            'Rating': product_rating,
            'Number of Reviews': num_reviews
        })

    return products_data


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
total_pages = 20
products_data = []

for page_number in range(1, total_pages + 1):
    url = base_url + str(page_number)
    products_data.extend(scrape_products(url))


max_product_urls = 200
products_data = products_data[:max_product_urls]


csv_filename = 'amazon_products.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = products_data[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(products_data)

print(f"Scraped data for {len(products_data)} products and saved to {csv_filename}")
