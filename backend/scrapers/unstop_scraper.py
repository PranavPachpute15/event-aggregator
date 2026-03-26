import requests
from datetime import datetime, timedelta

API_URL = "https://unstop.com/api/public/opportunity/search-result"


def parse_date(value):
    try:
        if isinstance(value, int):
            return datetime.fromtimestamp(value).date()
        elif isinstance(value, str) and len(value) >= 10:
            return datetime.strptime(value[:10], "%Y-%m-%d").date()
    except:
        return None
    return None


def fetch_unstop_events():
    events = []
    today = datetime.today().date()

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    for page in range(1, 6):
        print(f"\nFetching page {page}...")

        # 🔥 FIXED PARAMS (WORKING)
        params = {
            "opportunity": "hackathons",
            "per_page": 20,
            "page": page,
            "search": "",
            "sort": "recent"
        }

        try:
            res = requests.get(API_URL, params=params, headers=headers, timeout=10)
            res.raise_for_status()
        except Exception as e:
            print("Request failed:", e)
            continue

        data = res.json()

        # 🔥 DEBUG (first time only)
        if page == 1:
            print("API Response Keys:", data.keys())

        items = data.get("data", {}).get("data", [])

        print("Found:", len(items))

        if not items:
            break

        for item in items:
            try:
                title = (item.get("title") or "").strip()
                url = item.get("public_url", "")

                if not title or not url:
                    continue

                # ✅ FIX URL
                if not url.startswith("http"):
                    url = f"https://unstop.com/{url.lstrip('/')}"

                # 🔥 DATE HANDLING
                start = parse_date(item.get("start_date"))
                end = parse_date(item.get("end_date"))

                # ✅ SMART FALLBACK (IMPORTANT)
                if not start:
                    start = today + timedelta(days=2)

                if not end:
                    end = start + timedelta(days=7)

                # ❌ REMOVE PAST EVENTS EARLY
                if end < today:
                    continue

                event = {
                    "title": f"[Unstop] {title}",
                    "description": item.get("seo_description", ""),
                    "event_url": url,
                    "source": "Unstop",
                    "category": "competition",
                    "start_date": start.strftime("%Y-%m-%d"),
                    "end_date": end.strftime("%Y-%m-%d"),
                    "location": item.get("region") or "India"
                }

                events.append(event)

            except Exception as e:
                print("Error parsing:", e)

    return events


def push_unstop_events():
    BACKEND_API = "http://127.0.0.1:5000/add-event"

    events = fetch_unstop_events()

    print("\nTotal Unstop events:", len(events))

    for event in events:
        try:
            res = requests.post(BACKEND_API, json=event)
            print(res.status_code, event["title"])
        except Exception as e:
            print("Failed to send:", e)


if __name__ == "__main__":
    push_unstop_events()