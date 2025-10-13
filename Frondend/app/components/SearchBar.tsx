"use client";

import { useState } from "react";

export default function SearchBar({ onSearch }: { onSearch: (data: any[]) => void }) {
  const [query, setQuery] = useState("");

const handleSearch = async () => {
  if (!query.trim()) return;

  try {
    const res = await fetch(`http://127.0.0.1:2104/accounts/search/?search_word=${encodeURIComponent(query)}`, {mode: "cors"});

    if (!res.ok) {
      console.error("Search request failed:", res.status);
      onSearch([]);
      return;
    }

    const data = await res.json();

    // Перевіряємо, що повертається масив
    const results = Array.isArray(data) ? data : data.results || [];
    onSearch(results);
  } catch (err) {
    console.error("Search error:", err);
    onSearch([]);
  }
};

  return (
    <div className="flex gap-2">
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search..."
        className="border p-2 rounded-md w-64"
      />
      <button onClick={handleSearch} className="bg-green-500 text-white px-3 rounded-md">
        🔍 Search
      </button>
    </div>
  );
}
