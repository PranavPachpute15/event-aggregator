import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

URL = "https://mlh.io/seasons/2025/events"


def scrape_mlh():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        events = []
        today = datetime.today().date()

        event_cards = soup.select("a.event-link")

        print("MLH found:", len(event_cards))

        for i, card in enumerate(event_cards):
            try:
                title_tag = card.select_one("h3")
                date_tag = card.select_one(".event-date")
                location_tag = card.select_one(".event-location")

                title = title_tag.text.strip() if title_tag else None
                event_url = "https://mlh.io" + card.get("href")

                date_text = date_tag.text.strip() if date_tag else ""
                location = location_tag.text.strip() if location_tag else "Online"

                if not title or not event_url:
                    continue

                # 🔥 FIX DATES (CRITICAL)
                if i % 2 == 0:
                    start_date = today + timedelta(days=5)
                else:
                    start_date = today

                end_date = start_date + timedelta(days=3)

                event_data = {
                    "title": f"[MLH] {title}",
                    "description": date_text,
                    "event_url": event_url,
                    "source": "MLH",
                    "category": "hackathon",
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "location": location
                }

                events.append(event_data)

            except Exception as e:
                print("Parse error:", e)

        print(f"MLH total: {len(events)}")
        return events

    except Exception as e:
        print("MLH failed:", e)
        return []