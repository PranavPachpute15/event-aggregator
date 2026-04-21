import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def scrape_quotes():
    url = "http://quotes.toscrape.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.find_all("div", class_="quote")

    today = datetime.today().date()
    events = []

    for i, q in enumerate(quotes):
        try:
            text = q.find("span", class_="text").text.strip()
            author = q.find("small", class_="author").text

            start_date = today + timedelta(days=i % 3)
            end_date = start_date + timedelta(days=1)

            event = {
                "title": text[:50],
                "description": f"By {author}",
                "event_url": "http://quotes.toscrape.com",
                "source": "Quotes",
                "category": "inspiration",
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "location": "Online"
            }

            events.append(event)

        except Exception as e:
            print("Error:", e)

    print(f"Quotes total: {len(events)}")
    return events