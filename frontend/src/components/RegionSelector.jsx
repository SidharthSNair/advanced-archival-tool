import { useEffect, useState } from "react";
import { fetchJSON } from "../api/client";

export default function RegionSelector({ onShareSelect }) {
  const [regions, setRegions] = useState([]);
  const [locations, setLocations] = useState([]);
  const [shares, setShares] = useState([]);

  const [region, setRegion] = useState(null);
  const [location, setLocation] = useState(null);
  const [share, setShare] = useState(null);

  // Load regions on mount
  useEffect(() => {
    fetchJSON("/regions/").then(setRegions);
  }, []);

  const handleRegion = (code) => {
    setRegion(code);
    setLocation(null);
    setShare(null);
    setLocations([]);
    setShares([]);
    if (code) {
      fetchJSON(`/regions/${code}/locations`).then(setLocations);
    }
  };

  const handleLocation = (code) => {
    setLocation(code);
    setShare(null);
    setShares([]);
    if (code) {
      fetchJSON(`/regions/locations/${code}/shares`).then(setShares);
    }
  };

  const handleShare = (share) => {
    setShare(share);
    if (share) {
      onShareSelect({ share, region, location });
    }
  };

  return (
    <div className="p-4 space-y-4 bg-white rounded shadow">
      <div>
        <label className="block text-sm font-medium">Region</label>
        <select
          className="mt-1 block w-full border rounded p-2"
          value={region || ""}
          onChange={(e) => handleRegion(e.target.value)}
        >
          <option value="">Select Region</option>
          {regions.map((r) => (
            <option key={r.code} value={r.code}>
              {r.name}
            </option>
          ))}
        </select>
      </div>

      {locations.length > 0 && (
        <div>
          <label className="block text-sm font-medium">Location</label>
          <select
            className="mt-1 block w-full border rounded p-2"
            value={location || ""}
            onChange={(e) => handleLocation(e.target.value)}
          >
            <option value="">Select Location</option>
            {locations.map((l) => (
              <option key={l.code} value={l.code}>
                {l.name}
              </option>
            ))}
          </select>
        </div>
      )}

      {shares.length > 0 && (
        <div>
          <label className="block text-sm font-medium">Share</label>
          <select
            className="mt-1 block w-full border rounded p-2"
            value={share?.id || ""}
            onChange={(e) =>
              handleShare(shares.find((s) => s.id === Number(e.target.value)))
            }
          >
            <option value="">Select Share</option>
            {shares.map((s) => (
              <option key={s.id} value={s.id}>
                {s.unc_path}
              </option>
            ))}
          </select>
        </div>
      )}
    </div>
  );
}
