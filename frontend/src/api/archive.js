import { API_BASE } from "./client";

export async function scheduleArchive(region, location, share, paths) {
  const res = await fetch(`${API_BASE}/archive/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      region_code: region,
      location_code: location,
      share_unc: share.unc_path,
      paths: paths,
    }),
  });

  if (!res.ok) throw new Error(`Archive API failed: ${res.status}`);
  return res.json();
}
