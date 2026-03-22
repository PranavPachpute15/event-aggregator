# Import scrapers
from devpost_scraper import push_events_to_api


def run_all_scrapers():
    print("🚀 Starting all scrapers...\n")

    # 🔹 Devpost
    print("Running Devpost scraper...")
    try:
        push_events_to_api()
        print("✅ Devpost done\n")
    except Exception as e:
        print("❌ Devpost failed:", e)

    # 🔹 Future scrapers go here
    # Example:
    # from eventbrite_scraper import push_eventbrite_events
    # push_eventbrite_events()

    print("🎉 All scrapers finished!")


if __name__ == "__main__":
    run_all_scrapers()