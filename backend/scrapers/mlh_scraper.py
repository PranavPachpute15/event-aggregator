import requests
from bs4 import BeautifulSoup

URL = "https://mlh.io/seasons/2025/events"


def fetch_mlh_events():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        events = []

        # 🔥 UPDATED SELECTOR (IMPORTANT)
        event_cards = soup.select("a.event-link")

        print("Found MLH events:", len(event_cards))

        for card in event_cards:
            try:
                title_tag = card.select_one("h3")
                date_tag = card.select_one(".event-date")
                location_tag = card.select_one(".event-location")

                title = title_tag.text.strip() if title_tag else None
                event_url = "https://mlh.io" + card.get("href")

                date_text = date_tag.text.strip() if date_tag else ""
                location = location_tag.text.strip() if location_tag else "Unknown"

                if not title or not event_url:
                    continue

                event_data = {
                    "title": title,
                    "description": date_text,
                    "event_url": event_url,
                    "source": "MLH",
                    "category": "hackathon",
                    "start_date": None,
                    "end_date": None,
                    "location": location
                }

                events.append(event_data)

            except Exception as e:
                print("Error parsing MLH event:", e)

        return events

    except Exception as e:
        print("MLH scraping failed:", e)
        return []


def push_mlh_events():
    API_URL = "http://127.0.0.1:5000/add-event"

    events = fetch_mlh_events()

    print("Fetched MLH:", len(events))

    for event in events:
        try:
            res = requests.post(API_URL, json=event)
            print(res.status_code, event["title"])
        except Exception as e:
            print("Failed to send:", e)


if __name__ == "__main__":
    push_mlh_events()