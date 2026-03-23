import React, { useEffect, useState } from "react";

function App() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/events")
      .then((res) => res.json())
      .then((data) => setEvents(data.events))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 to-gray-200 p-8">
      
      {/* HEADER */}
      <h1 className="text-4xl font-bold text-center mb-10 text-gray-800">
        🚀 Student Event Aggregator
      </h1>

      {/* GRID */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">

        {events.map((event, index) => (
          <div
            key={index}
            className="bg-white rounded-2xl shadow-md hover:shadow-xl transition duration-300 p-5 border border-gray-200"
          >
            {/* TITLE */}
            <h2 className="text-xl font-semibold text-gray-800 mb-3">
              {event.title}
            </h2>

            {/* LOCATION */}
            <p className="text-gray-600 text-sm mb-1">
              📍 <span className="font-medium">{event.location}</span>
            </p>

            {/* DATE */}
            <p className="text-gray-600 text-sm mb-3">
              📅 {new Date(event.start_date).toDateString()}
            </p>

            {/* BUTTON */}
            <a
              href={event.event_url}
              target="_blank"
              rel="noreferrer"
              className="inline-block mt-3 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              View Event →
            </a>
          </div>
        ))}

      </div>
    </div>
  );
}

export default App;