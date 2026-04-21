import requests
from datetime import datetime, timedelta

API_URL = "https://www.eventbrite.com/api/v3/destination/search/"


def scrape_eventbrite():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        params = {
            "q": "tech",
            "location.address": "India",
            "page": 1
        }

        response = requests.get(API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        events = data.get("events", [])

        print("Eventbrite found:", len(events))

        results = []
        today = datetime.today().date()

        for event in events:
            try:
                title = event.get("name", {}).get("text")
                event_url = event.get("url")

                start = event.get("start", {}).get("local")
                end = event.get("end", {}).get("local")

                if not title or not event_url:
                    continue

                # 🔥 FIX DATES
                try:
                    start_date = datetime.fromisoformat(start).date() if start else today + timedelta(days=2)
                except:
                    start_date = today + timedelta(days=2)

                try:
                    end_date = datetime.fromisoformat(end).date() if end else start_date + timedelta(days=2)
                except:
                    end_date = start_date + timedelta(days=2)

                # ❌ Skip past
                if end_date < today:
                    continue

                event_data = {
                    "title": f"[Eventbrite] {title.strip()}",
                    "description": "",
                    "event_url": event_url,
                    "source": "Eventbrite",
                    "category": "event",
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "location": "India"
                }

                results.append(event_data)

            except Exception as e:
                print("Parse error:", e)

        print(f"Eventbrite total: {len(results)}")
        return results

    except Exception as e:
        print("Eventbrite failed:", e)
        return []