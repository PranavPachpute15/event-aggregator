import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

API_URL = "https://devpost.com/api/hackathons"


def fetch_event_details(event_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(event_url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        desc_tag = soup.find("div", class_="challenge-description")
        description = desc_tag.text.strip() if desc_tag else ""

        date_tag = soup.find("div", class_="submission-period")
        date_text = date_tag.text.strip() if date_tag else ""

        start_date = None
        end_date = None

        if date_text:
            try:
                parts = re.split(r"–|-", date_text)

                if len(parts) == 2:
                    start_str = parts[0].strip()
                    end_str = parts[1].strip()

                    year_match = re.search(r"\d{4}", end_str)
                    year = year_match.group() if year_match else ""

                    start_str = f"{start_str} {year}"

                    start_date = datetime.strptime(start_str, "%b %d %Y").date()
                    end_date = datetime.strptime(end_str, "%b %d, %Y").date()

            except Exception as e:
                print("Date parsing failed:", e)

        return description, start_date, end_date

    except Exception as e:
        print("Detail fetch failed:", e)
        return "", None, None


def scrape_devpost():
    all_events = []

    india_keywords = [
        "india", "delhi", "mumbai", "pune", "bangalore",
        "hyderabad", "chennai", "kolkata", "kanpur",
        "uttar pradesh", "maharashtra", "karnataka",
        "tamil nadu"
    ]

    today = datetime.today().date()

    try:
        for page in range(1, 6):  # reduced for speed
            print(f"Fetching Devpost page {page}...")

            response = requests.get(API_URL, params={"page": page}, timeout=10)
            response.raise_for_status()

            data = response.json()
            hackathons = data.get("hackathons", [])

            if not hackathons:
                break

            for hackathon in hackathons:
                try:
                    title = (hackathon.get("title") or "").strip()
                    event_url = hackathon.get("url")

                    if not title or not event_url:
                        continue

                    location_data = hackathon.get("displayed_location")

                    if isinstance(location_data, dict):
                        location = location_data.get("location", "Online")
                    else:
                        location = location_data or "Online"

                    location_lower = location.lower()

                    is_india = any(word in location_lower for word in india_keywords)
                    is_online = "online" in location_lower

                    if not (is_india or is_online):
                        continue

                    description, start_date, end_date = fetch_event_details(event_url)

                    if not start_date:
                        start_date = today + timedelta(days=5)

                    if not end_date:
                        end_date = start_date + timedelta(days=7)

                    if end_date < today:
                        continue

                    event = {
                        "title": f"[Devpost] {title}",
                        "description": description,
                        "event_url": event_url,
                        "source": "Devpost",
                        "category": "hackathon",
                        "start_date": start_date.strftime("%Y-%m-%d"),
                        "end_date": end_date.strftime("%Y-%m-%d"),
                        "location": location.title()
                    }

                    all_events.append(event)

                except Exception as e:
                    print("Parse error:", e)

        print(f"Devpost total: {len(all_events)}")
        return all_events

    except Exception as e:
        print("Devpost failed:", e)
        return []