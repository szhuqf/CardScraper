from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Set up Selenium WebDriver
options = Options()
options.add_argument("--headless")  # Run in headless mode (no GUI)
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Target URL for Magic 2010 singles
url = "https://starcitygames.com/shop/singles/magic-2010/"
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Scroll down to load more products
for _ in range(3):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(3)  # Wait for new items to load

# Scrape card titles and prices
cards = driver.find_elements(By.CSS_SELECTOR, '.hawk-results-item')

data = []
for card in cards:
    try:
        card_info = card.text
        name, collection, foil, price = card_info.split('\n')[:4]

        data.append({"Name": name, "Price": price})
    except:
        continue

# Close the WebDriver
driver.quit()

# Convert to DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv("magic2010_cards.csv", index=False)

print("Scraping completed. Data saved to magic2010_cards.csv.")
