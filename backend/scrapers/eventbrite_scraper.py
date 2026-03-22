import requests

API_URL = "https://www.eventbrite.com/api/v3/destination/search/"


def fetch_eventbrite_events():
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

        print("Found Eventbrite events:", len(events))

        results = []

        for event in events:
            try:
                title = event.get("name", {}).get("text")
                event_url = event.get("url")

                start = event.get("start", {}).get("local")
                end = event.get("end", {}).get("local")

                if not title or not event_url:
                    continue

                event_data = {
                    "title": title.strip(),
                    "description": "",
                    "event_url": event_url,
                    "source": "Eventbrite",
                    "category": "event",
                    "start_date": start,
                    "end_date": end,
                    "location": "India"
                }

                results.append(event_data)

            except Exception as e:
                print("Error parsing Eventbrite:", e)

        return results

    except Exception as e:
        print("Eventbrite API failed:", e)
        return []


def push_eventbrite_events():
    BACKEND_API = "http://127.0.0.1:5000/add-event"

    events = fetch_eventbrite_events()

    print("Fetched Eventbrite:", len(events))

    for event in events:
        try:
            res = requests.post(BACKEND_API, json=event)
            print(res.status_code, event["title"])
        except Exception as e:
            print("Failed to send:", e)


if __name__ == "__main__":
    push_eventbrite_events()