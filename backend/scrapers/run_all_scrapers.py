from services.event_service import insert_event

from scrapers.devpost_scraper import scrape_devpost
from scrapers.internshala_scraper import scrape_internshala
from scrapers.eventbrite_scraper import scrape_eventbrite
from scrapers.mlh_scraper import scrape_mlh


def run_all_scrapers():
    all_events = []

    print("🚀 Running Devpost...")
    try:
        events = scrape_devpost()
        print(f"Devpost: {len(events)}")
        all_events += events
    except Exception as e:
        print("Devpost error:", e)

    print("🚀 Running Internshala...")
    try:
        events = scrape_internshala()
        print(f"Internshala: {len(events)}")
        all_events += events
    except Exception as e:
        print("Internshala error:", e)

    print("🚀 Running Eventbrite...")
    try:
        events = scrape_eventbrite()
        print(f"Eventbrite: {len(events)}")
        all_events += events
    except Exception as e:
        print("Eventbrite error:", e)

    print("🚀 Running MLH...")
    try:
        events = scrape_mlh()
        print(f"MLH: {len(events)}")
        all_events += events
    except Exception as e:
        print("MLH error:", e)

    print(f"\n🔥 TOTAL EVENTS COLLECTED: {len(all_events)}")

    inserted = 0

    # 🔥 INSERT INTO DB
    for event in all_events:
        try:
            result = insert_event(event)
            if "error" not in result:
                inserted += 1
        except Exception as e:
            print("Insert error:", e)

    print(f"✅ INSERTED INTO DB: {inserted}")