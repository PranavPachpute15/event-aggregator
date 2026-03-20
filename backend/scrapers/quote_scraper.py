import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "http://quotes.toscrape.com"

response = requests.get(url, verify=False)
soup = BeautifulSoup(response.text, "html.parser")

quotes = soup.find_all("div", class_="quote")

api_url = "http://127.0.0.1:5000/add-event"

for q in quotes:
    text = q.find("span", class_="text").text.encode("utf-8", "ignore").decode("utf-8")
    author = q.find("small", class_="author").text
    tags = [tag.text for tag in q.find_all("a", class_="tag")]

    # Convert quote → event format
    data = {
        "title": text[:50],  # short title
        "description": f"By {author} | Tags: {', '.join(tags)}",
        "event_url": "http://quotes.toscrape.com",
        "source": "QuotesScraper",
        "category": "Inspiration",
        "start_date": "2026-04-01 10:00:00",
        "end_date": "2026-04-02 18:00:00",
        "location": "Online"
    }

    response = requests.post(api_url, json=data)

    print(response.json())