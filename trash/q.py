import cfscrape
from bs4 import BeautifulSoup
import time

# Initialize a Cloudflare scraper instance
scraper = cfscrape.create_scraper()

# URL you want to scrape (replace 'your_url_here' with the actual URL)
code = "158576702"

url = f"https://www.ceneo.pl/{code}#tab=reviews"

# Fetch the content of the page
response = scraper.get(url).content

time.sleep(3)

url = "https://www.ceneo.pl/158576702/opinie-7"

# Fetch the content of the page
response = scraper.get(url).content

# Use BeautifulSoup to parse the HTML content (optional, if you need to parse HTML)
soup = BeautifulSoup(response, 'html.parser')

# Example: print the title of the page to check if it's the correct page
print(soup)

# Further processing can be done based on your needs
# For example, extracting specific elements from the soup object