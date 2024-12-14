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
git clone <repository_url>
cd amazon-scraper
```
### 2. Install Dependencies:

Activate your virtual environment (if you created one) and install the required packages listed in requirements.txt:
```bash
pip install -r requirements.txt
```

### 4. Install Chrome and ChromeDriver:

This project uses Selenium for web scraping, which requires Chrome and ChromeDriver.

Download and install Google Chrome if you haven't already.
Download ChromeDriver from the official website (https://chromedriver.chromium.org/downloads) and ensure it's compatible with your Chrome version.
Make sure ChromeDriver is accessible from your command line. You can either:
Add the directory containing ChromeDriver to your system's PATH environment variable.
Specify the path to the ChromeDriver executable within the project script.

### 5. Set Up the Database (Optional):

By default, this project uses SQLite for data storage. If you prefer a different database (e.g., PostgreSQL), you can configure it in the Django settings. To use the default SQLite database, run the following command to create the database schema:

```bash
python manage.py migrate
```

### 6. Run the Development Server:

Start the Django development server:

```bash
python manage.py runserver
```
The server will be running at:

http://127.0.0.1:8000/


### 7. Access the Application:

Open your web browser and navigate to http://127.0.0.1:8000/.
You'll see a form where you can enter a product name (e.g., "mobiles").
Enter a product name and click "Search".
The page will display a list of products with their titles, images, ratings, and prices.
You can click the "Download CSV" button to download these product details in a CSV file format.
