from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# Setup main options
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # To run Chrome in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
options.add_argument(f"user-agent={user_agent}")
driver = webdriver.Chrome(options=options)

# First get all the live channels into a list
homepage = "https://thetvapp.to/tv/"
driver.get(homepage)
channels = re.findall('a href=\"/tv/(.*?)/\"', driver.page_source)

# Enumerate and print the list then wait for user to input a number
for i, channel in enumerate(channels):
    print(i, channel.replace('-', ' '))
while True:
    try:
        selection = int(input("Please select a channel number: "))
        if selection < 0 or selection >= len(channels):
            print(f"Please select a number between 0 and {len(channels) - 1}.")
            continue
    except ValueError:
        print("Sorry, numbers only.")
        continue
    else:
        break

url = homepage + str(channels[selection])
print(f'Scraping page for playlist at {url}')



def extract_desired_url(requests):
    # Search for the desired URL in the requests
    for request in requests:
        if "m3u8?token=" in request:
            return request
    return None


def get_get_requests():
    global driver
    try:
        # Execute JavaScript to capture network requests
        requests = driver.execute_script("""
            var performance = window.performance || window.webkitPerformance || window.msPerformance || window.mozPerformance;
            if (!performance) {
                return [];
            }
            var entries = performance.getEntriesByType("resource");
            var urls = [];
            for (var i = 0; i < entries.length; i++) {
                urls.push(entries[i].name);
            }
            return urls;
        """)
        return requests
    except Exception as e:
        print("An error occurred:", e)
        return None



driver.get(url)
time.sleep(1)  # Adjust this if needed - this is the wait for the player to receive the decoded url
get_requests = get_get_requests()

# Extract the desired URL
if get_requests:
    desired_url = extract_desired_url(get_requests)
    if desired_url:
        print("Playlist URL found:", desired_url)
    else:
        print("No Playlist URL found in the requests.")
else:
    print("No GET requests found.")

driver.quit()
