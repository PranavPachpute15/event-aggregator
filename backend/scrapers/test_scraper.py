import requests
from bs4 import BeautifulSoup
import urllib3

# Disable warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://example.com"

response = requests.get(url, verify=False)

soup = BeautifulSoup(response.text, "html.parser")

print("Page Title:", soup.title.text)