import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";

function App() {
  const [events, setEvents] = useState([]);
  const [filter, setFilter] = useState("all");
  const [search, setSearch] = useState("");
  const [locationFilter, setLocationFilter] = useState("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/events?ts=" + Date.now())
      .then((res) => res.json())
      .then((data) => {
        setEvents(data.events || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const filteredEvents = events
    .filter((event) => {
      
      if (filter === "upcoming") return event.status === "upcoming";
      if (filter === "ongoing") return event.status === "ongoing";
      if (filter === "hackathon") return event.category === "hackathon";
      if (filter === "internship") return event.category === "internship";

return true;
    })
    .filter((event) => {
      if (!search) return true;
      return (
        (event.title || "").toLowerCase().includes(search.toLowerCase()) ||
        (event.location || "").toLowerCase().includes(search.toLowerCase())
      );
    })
    .filter((event) => {
      if (locationFilter === "all") return true;
      const loc = (event.location || "").toLowerCase();
      if (locationFilter === "online") return loc.includes("online");
      return loc.includes(locationFilter);
    })
    .sort((a, b) => new Date(b.start_date) - new Date(a.start_date));

  const ParticleBackground = () => (
    <div className="fixed inset-0 -z-10 overflow-hidden">
      {[...Array(25)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute w-1 h-1 bg-white rounded-full opacity-30"
          animate={{ y: [0, window.innerHeight] }}
          transition={{ duration: 8 + i, repeat: Infinity, ease: "linear" }}
          style={{ left: `${(i * 7) % 100}%` }}
        />
      ))}
    </div>
  );

  const SkeletonCard = () => (
    <div className="animate-pulse bg-white/10 p-5 rounded-xl">
      <div className="h-4 bg-white/20 mb-3 w-3/4"></div>
      <div className="h-3 bg-white/20 mb-2"></div>
      <div className="h-3 bg-white/20 w-1/2"></div>
    </div>
  );

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-black via-gray-900 to-gray-800 text-white">
      <ParticleBackground />

      {/* SIDEBAR */}
      <div className="w-64 fixed h-full bg-white/5 backdrop-blur-xl border-r border-white/10 p-5 hidden md:block">
        <h2 className="text-xl font-bold mb-6">🚀 DASHBOARD</h2>
        {["ALL", "UPCOMING", "ONGOING", "HACKATHON", "INTERNSHIP"].map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f.toLowerCase())}
            className={`block w-full text-left px-3 py-2 rounded-lg mb-2 ${
              filter === f.toLowerCase()
                ? "bg-gradient-to-r from-blue-500 to-purple-500"
                : "hover:bg-white/10"
            }`}
          >
            {f}
          </button>
        ))}
      </div>

      {/* MAIN */}
      <div className="flex-1 ml-64">

        {/* NAVBAR (FIXED) */}
        <div className="fixed top-0 left-64 right-0 bg-black/40 backdrop-blur-xl border-b border-white/10 p-4 flex justify-between items-center z-50">
          <h1 className="text-2xl font-bold tracking-wide">
            STUDENT EVENT AGGREGATOR
          </h1>

          <div className="flex gap-3">
            <input
              placeholder="Search..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="px-3 py-2 rounded-lg bg-white/10 border border-white/20 focus:outline-none"
            />

            <select
              value={locationFilter}
              onChange={(e) => setLocationFilter(e.target.value)}
              className="px-3 py-2 rounded-lg bg-gray-900 border border-white/20 focus:outline-none"
            >
              <option value="all">ALL</option>
              <option value="online">ONLINE</option>
              <option value="india">INDIA</option>
              <option value="nagpur">NAGPUR</option>
            </select>
          </div>
        </div>

        {/* CONTENT */}
        <div className="p-6 pt-24 grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {loading
            ? [...Array(6)].map((_, i) => <SkeletonCard key={i} />)
            : filteredEvents.map((event, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4 }}
                  whileHover={{ scale: 1.05 }}
                  className="bg-white/10 backdrop-blur-lg p-5 rounded-xl border border-white/10"
                >
                  <h2 className="font-semibold mb-2">
                    {(event.title || "").replace(/\[.*?\]\s*/, "")}
                  </h2>

                  <p className="text-sm text-gray-300 mb-1">📍 {event.location}</p>
                  <p className="text-sm text-gray-400 mb-3">
                    {event.start_date
                      ? new Date(event.start_date).toDateString()
                      : "TBD"}
                  </p>

                  <a
                    href={event.event_url}
                    target="_blank"
                    rel="noreferrer"
                    className="block text-center py-2 rounded-lg bg-gradient-to-r from-blue-500 to-purple-500"
                  >
                    VIEW EVENT
                  </a>
                </motion.div>
              ))}
        </div>
      </div>
    </div>
  );
}

export default App;