import requests

url = "http://127.0.0.1:5000/add-event"

data = {
    "title": "Web Dev Workshop 2026",
    "description": "Build AI solutions",
    "event_url": "https://example.com",
    "source": "Test",
    "category": "Workshop",
    "start_date": "2026-04-01 10:00:00",
    "end_date": "2026-04-02 18:00:00",
    "location": "Online"
}

response = requests.post(url, json=data)

print(response.json())