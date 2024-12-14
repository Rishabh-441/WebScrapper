# Amazon Scraper Project

This is a web scraper built using **Selenium** and **BeautifulSoup** to scrape Amazon product details like title, image, price, and rating. The scraped data is displayed in a Django web application, and users can download the results as a CSV file.

## Features

- Search for products on Amazon.
- View product details including title, image, price, and rating.
- Download the product data as a CSV file.

## Requirements

- Python 3.x
- Google Chrome
- ChromeDriver (compatible with your version of Chrome)
- Virtual Environment (optional but recommended)

## Setup Instructions

Follow the steps below to clone the project and set it up on your local machine.

### 1. Clone the Repository

Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/Rishabh-441/WebScrapper/tree/main
cd amazon-scraper
```
### 2. Install Dependencies:

Activate your virtual environment (if you created one) and install the required packages listed in requirements.txt:
```bash
pip install -r requirements.txt
```

### 3. Install Chrome and ChromeDriver:

This project uses Selenium for web scraping, which requires Chrome and ChromeDriver.

Download and install Google Chrome if you haven't already.
Download ChromeDriver from the official website (https://chromedriver.chromium.org/downloads) and ensure it's compatible with your Chrome version.
Make sure ChromeDriver is accessible from your command line. You can either:
Add the directory containing ChromeDriver to your system's PATH environment variable.
Specify the path to the ChromeDriver executable within the project script.

### 4. Set Up the Database (Optional):

By default, this project uses SQLite for data storage. If you prefer a different database (e.g., PostgreSQL), you can configure it in the Django settings. To use the default SQLite database, run the following command to create the database schema:

```bash
python manage.py migrate
```

### 5. Run the Development Server:

Start the Django development server:

```bash
python manage.py runserver
```
The server will be running at:

http://127.0.0.1:8000/


### 6. Access the Application:

Open your web browser and navigate to http://127.0.0.1:8000/.
You'll see a form where you can enter a product name (e.g., "mobiles").
Enter a product name and click "Search".
The page will display a list of products with their titles, images, ratings, and prices.
You can click the "Download CSV" button to download these product details in a CSV file format.


## Base Code:

```bash
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm
import time

# Configure Chrome to run in headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')  # Enable headless mode
chrome_options.add_argument('--disable-gpu')  # Disable GPU for headless compatibility
chrome_options.add_argument('--window-size=1920,1080')  # Set default window size for rendering

# Initialize the Chrome WebDriver with the options
driver = webdriver.Chrome(options=chrome_options)
# Open Amazon
driver.get('https://www.amazon.in/s?k=mobiles&crid=370P9AP6N85PI&sprefix=laptops%2Caps%2C214&ref=nb_sb_noss_2')
html_data = BeautifulSoup(driver.page_source, 'html.parser')
no_of_pages = int(html_data.find('span', {'class' : 's-pagination-item s-pagination-disabled'}).text)
print(no_of_pages)

titles = []
images = []
ratings = []
prices = []

for page in tqdm(range(no_of_pages)):
    driver.get('https://www.amazon.in/s?k=mobiles&crid=370P9AP6N85PI&sprefix=laptops%2Caps%2C214&ref=nb_sb_noss_2&page='+str(page+1))
    time.sleep(2)
    html_data = BeautifulSoup(driver.page_source, 'html.parser')
    products = html_data.find_all('div', {'data-component-type': 's-search-result'})
    for product in products:
        title = product.find('h2', {'class': 'a-size-medium a-spacing-none a-color-base a-text-normal'})
        image_url = product.find('img')
        rating = product.find('span', {'class': 'a-icon-alt'})
        price = product.find('span', {'class': 'a-price-whole'})
        titles.append(title.text)
        images.append(image_url['src'])
        if rating is None:
            ratings.append("No rating")
        else:
            ratings.append(rating.text)

        if price is None:
            prices.append('NA')
        else:
            prices.append(int(price.text.replace(',','').strip('.')))

data = pd.DataFrame({'titles':titles, 'image_url':images, 'ratings':ratings, 'prices':prices})
print(data)
data.to_csv('Laptop Products.csv')
# Pause the script to keep the browser open
input("Press Enter to close the browser...")
driver.quit()

```
