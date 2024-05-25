# Web Scraping Airbnb

This Python script performs web scraping on Airbnb to gather information about listings in a specific city. It utilizes Selenium for web scraping and BeautifulSoup for HTML parsing. The scraped data is saved to both a JSON file and an Excel file.

## Prerequisites
- Python 3.x
- Selenium
- BeautifulSoup
- Pandas
- Chrome WebDriver (chromedriver)

## Requirements
The script requires the following Python packages. You can install them using pip:

```plaintext
selenium
beautifulsoup4
pandas
```

## Installation
1. Install Python 3.x from [python.org](https://www.python.org/downloads/)
2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Download Chrome WebDriver from [chromedriver.chromium.org](https://sites.google.com/chromium.org/driver/)
4. Extract the chromedriver executable and place it in the 'drivers' folder in the project directory.
```