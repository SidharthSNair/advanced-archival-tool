import { useState } from "react";

export default function FiltersBar({ onChange }) {
  const [q, setQ] = useState("");
  const [kind, setKind] = useState("all");
  const [days, setDays] = useState("");

  const apply = () => onChange({ q, kind, days });

  return (
    <div className="flex items-end gap-3 bg-white p-3 rounded border">
      {/* 🔍 Search box */}
      <div className="flex-1">
        <label className="block text-xs font-medium text-gray-600">Search name</label>
        <input
          className="mt-1 w-full border rounded p-2"
          placeholder="e.g. budget, report"
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
      </div>

      {/* 📂 Type filter */}
      <div>
        <label className="block text-xs font-medium text-gray-600">Type</label>
        <select
          className="mt-1 border rounded p-2"
          value={kind}
          onChange={(e) => setKind(e.target.value)}
        >
          <option value="all">All</option>
          <option value="dir">Folders</option>
          <option value="file">Files</option>
        </select>
      </div>

      {/* 🕒 Days filter */}
      <div>
        <label className="block text-xs font-medium text-gray-600">Not modified in ≥ days</label>
        <input
          type="number"
          min="0"
          placeholder="e.g. 30"
          className="mt-1 border rounded p-2 w-28"
          value={days}
          onChange={(e) => setDays(e.target.value)}
        />
      </div>

      <button
        onClick={apply}
        className="h-10 px-4 bg-gray-900 text-white rounded hover:bg-black"
      >
        Apply
      </button>
    </div>
  );
}
