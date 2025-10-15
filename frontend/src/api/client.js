export const API_BASE = "http://127.0.0.1:8000";

export async function fetchJSON(url) {
  const res = await fetch(`${API_BASE}${url}`);
//  const res = await fetch(`${API_BASE}${url}`, {
//    headers: { "Content-Type": "application/json" },
//    ...options,
//  });
  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }
  return res.json();
}
