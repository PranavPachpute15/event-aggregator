import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

BASE_URL = "https://internshala.com/internships/page-{}"


def fetch_internshala_events():
    events = []
    headers = {"User-Agent": "Mozilla/5.0"}

    today = datetime.today().date()

    for page in range(1, 6):
        print(f"\nFetching page {page}...")
        url = BASE_URL.format(page)

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except:
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("div", class_="individual_internship")

        if not cards:
            break

        for i, card in enumerate(cards):
            try:
                title_tag = card.find("a", class_="job-title-href")
                title = title_tag.text.strip() if title_tag else ""
                link = title_tag["href"] if title_tag else ""

                if not title or not link:
                    continue

                event_url = "https://internshala.com" + link

                company = card.find("p", class_="company-name")
                company = company.text.strip() if company else ""

                location_tag = card.find("a", class_="location_link")
                location = location_tag.text.strip() if location_tag else "India"

                # 🔥 SMART DATE LOGIC
                # mix upcoming + ongoing
                if i % 3 == 0:
                    start_date = today + timedelta(days=3)
                else:
                    start_date = today

                end_date = start_date + timedelta(days=30)

                event = {
                    "title": f"[Internshala] {title}",
                    "description": f"Internship at {company}",
                    "event_url": event_url,
                    "source": "Internshala",
                    "category": "internship",
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "location": location
                }

                events.append(event)

            except Exception as e:
                print("Error:", e)

    return events
def push_internshala_events():
    BACKEND_API = "http://127.0.0.1:5000/add-event"

    events = fetch_internshala_events()

    print("\nTotal Internshala events:", len(events))

    for event in events:
        try:
            res = requests.post(BACKEND_API, json=event)
            print(res.status_code, event["title"])
        except Exception as e:
            print("Failed to send:", e)


if __name__ == "__main__":
    push_internshala_events()