def run_all_scrapers():
    try:
        from scrapers.devpost_scraper import push_events_to_api as devpost
        from scrapers.internshala_scraper import push_events_to_api as internshala
        from scrapers.eventbrite_scraper import push_events_to_api as eventbrite
        from scrapers.unstop_scraper import push_events_to_api as unstop
        from scrapers.mlh_scraper import push_events_to_api as mlh

        print("🚀 Running Devpost scraper...")
        devpost()

        print("🚀 Running Internshala scraper...")
        internshala()

        print("🚀 Running Eventbrite scraper...")
        eventbrite()

        print("🚀 Running Unstop scraper...")
        unstop()

        print("🚀 Running MLH scraper...")
        mlh()

        print("✅ All scrapers completed")

    except Exception as e:
        print("❌ Error in scrapers:", e)