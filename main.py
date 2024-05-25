import time
import json
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


ROOT_FOLDER = Path(__file__).parent
CHROMEDRIVER_EXEC = ROOT_FOLDER / 'drivers' / 'chromedriver'

def make_chrome_browser(*options: str) -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()

    # chrome_options.add_argument('--headless')
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    chrome_service = Service(
        executable_path=str(CHROMEDRIVER_EXEC),
    )

    browser = webdriver.Chrome(
        service=chrome_service,
        options=chrome_options
    )

    return browser

TIME_TO_WAIT = 5 

city = "João-Pessoa-~-PB"
default_check_in_date = "2024-09-14"
default_check_out_date = "2024-09-23"
number_of_adults = 3
filter_room_type = "Entire%20home%2Fapt"
min_bedrooms = 2
amenities_pool = 7
amenities_pool = 9
full_amenities_pool = '&amenities%5B%5D=7'
full_amenities_parking = '&amenities%5B%5D=9'

# Prompt user for check-in and check-out dates with default values
check_in_date = input(f"Enter check-in date (default: {default_check_in_date}): ") or default_check_in_date
check_out_date = input(f"Enter check-out date (default: {default_check_out_date}): ") or default_check_out_date


# Construct the dynamic URL
dynamic_url = f"https://www.airbnb.com.br/s/{city}/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date={check_in_date}&monthly_length=3&monthly_end_date={check_out_date}&price_filter_input_type=0&channel=EXPLORE&query={city}&place_id=ChIJ16OaATnorAcRNNsmbZxKQW4&location_bb=wOHbfcILLDrA54aNwgvhSQ%3D%3D&date_picker_type=calendar&checkin={check_in_date}&checkout={check_out_date}&adults={number_of_adults}&room_types%5B%5D={filter_room_type}&min_bedrooms={min_bedrooms}{full_amenities_parking}"

options = ()

browser = make_chrome_browser(*options)
browser.get(dynamic_url)


def format_city_name(city):
    parts = city.split("-")
    formatted_city = " ".join(part.capitalize() for part in parts if part)
    return formatted_city

# Define desired check-in and check-out dates (replace with your specific dates)
check_in_date = "2024-05-20"  # Adjust format as needed by the website
check_out_date = "2024-05-25"  # Adjust format as needed by the website

time.sleep(TIME_TO_WAIT)  # Wait for results to load

# Find all listing cards
# Locate the target element using the CSS selector
target_element = browser.find_element(By.CSS_SELECTOR, "#site-content > div")

# Extract the HTML content from the current page
current_page_html = browser.page_source
# Use BeautifulSoup to parse the extracted HTML
soup = BeautifulSoup(current_page_html, 'html.parser')
# Locate the target element using the CSS selector
target_element = soup.find('div', id="site-content")

results = []
listings = soup.find_all("div", class_="lxq01kf")

for listing in listings:
    # Extract the title of the listing
    title = listing.find("div", class_="t1jojoys").get_text(strip=True) if listing.find("div", class_="t1jojoys") else 'N/A'
    # Extracting the description
    description_section = listing.find("div", class_="fb4nyux")
    description = description_section.get_text(strip=True) if description_section else 'N/A'

    beds = 'N/A'
    date_range = 'N/A'

    # Find all subtitle divs for the number of beds nd date range within the listing
    beds_and_dates = listing.find_all("div", {"data-testid": "listing-card-subtitle"})
    for subtitle in beds_and_dates:
        text = subtitle.get_text(strip=True)
        
        # Check if the subtitle text contains information about beds
        if 'quartos' in text.lower():
            beds = text
        # Check if the subtitle text looks like a date range
        elif '-' in text or '-' in text:
            date_range = text
    
    # Extracting the day price
    day_price = listing.find("span", class_="_14y1gc").get_text(strip=True) if listing.find("span", class_="_14y1gc") else 'N/A'

    # Extracting full price of the range date
    full_price_section = listing.find("div", class_="_tt122m")
    full_price = full_price_section.get_text(strip=True).split('R$')[-1] if full_price_section else 'N/A'
    
    # Extracting the rating
    rating = listing.find("span", class_="ru0q88m").get_text(strip=True) if listing.find("span", class_="ru0q88m") else 'N/A'


    # Extracting the listing URL. The URL is relative, need to prepend the base Airbnb URL.
    listing_url_section = listing.find("div", class_="c14whb16") 
    listing_url = (
        "https://www.airbnb.com" + listing_url_section.find("a")["href"] if listing_url_section else ""
    )

    # Create a dictionary for the current listing
    listing_data = {
        "City": format_city_name(city),
        "Check In": check_in_date,
        "Check Out": check_out_date,
        "Title": title,
        "Description": description,
        "Beds": beds,
        "Day Price": day_price,
        "Full Price": full_price,
        "Rating": rating,
        "Date Range": date_range,
        "Listing URL": listing_url
    }

    # Append the listing dictionary to the results list
    results.append(listing_data)


    # write the results to a JSON file
with open('airbnb_results.json', 'w') as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

# Save results to Excel
df = pd.DataFrame(results)
timestamp = time.strftime("%d-%m-%Y %H_%M_%S")
file_path = 'airbnb_scraping.xlsx'


with pd.ExcelWriter(file_path, engine='openpyxl', mode='a' if Path(file_path).exists() else 'w') as writer:
    df.to_excel(writer, index=False, sheet_name=timestamp)
   


browser.quit()