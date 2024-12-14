import csv
from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

def home(request):
    """Render the home page with the form."""
    return render(request, 'scraper/home.html')


def search_product(request):
    product_name = request.GET.get('product_name', '').strip()
    if not product_name:
        return HttpResponse("Please enter a valid product name.")

    # Construct the Amazon search URL
    search_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"

    # Set up Chrome WebDriver in headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Headless mode for faster scraping
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(search_url)
        html_data = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the number of pages
        try:
            no_of_pages = int(html_data.find('span', {'class' : 's-pagination-item s-pagination-disabled'}).text)
        except AttributeError:
            # If pagination info is not found, default to 1 page
            no_of_pages = 1

        # List to hold product details
        titles, images, ratings, prices = [], [], [], []

        for page in tqdm(range(no_of_pages)):
            driver.get(f'{search_url}&page={page + 1}')
            time.sleep(2)  # Sleep to simulate human browsing and avoid detection

            html_data = BeautifulSoup(driver.page_source, 'html.parser')
            products = html_data.find_all('div', {'data-component-type': 's-search-result'})

            for product in products:
                title = product.find('div', {'data-cy': 'title-recipe'})
                image_url = product.find('img')
                rating = product.find('span', {'class': 'a-icon-alt'})
                price = product.find('span', {'class': 'a-price-whole'})

                titles.append(title.get_text(separator=' ', strip=True) if title else 'N/A')
                images.append(image_url['src'] if image_url else 'N/A')
                ratings.append(rating.text if rating else 'No rating')
                prices.append(price.text.replace(',', '').strip() if price else 'NA')

        # Prepare data for rendering
        product_details = [{'Title': title, 'Image_URL': image, 'Rating': rating, 'Price': price}
                           for title, image, rating, price in zip(titles, images, ratings, prices)]

        # Store the product details in the session for later use (this line)
        request.session['product_details'] = product_details

        context = {'product_name': product_name, 'products': product_details}
        return render(request, 'scraper/results.html', context)

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}")

    finally:
        # Ensure WebDriver quits even in case of errors
        driver.quit()


def download_csv(request):
    # Get the product details from the session or as a query parameter (same data used in search_product view)
    product_details = request.session.get('product_details', [])

    # Create a response with the appropriate CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="product_data.csv"'

    writer = csv.DictWriter(response, fieldnames=['Title', 'Image_URL', 'Rating', 'Price'])
    writer.writeheader()

    # Write the rows for each product
    for product in product_details:
        writer.writerow(product)

    return response
