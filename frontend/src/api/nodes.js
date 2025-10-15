import { fetchJSON } from "./client";
import { API_BASE } from "./client";
//export async function fetchNodes(shareId, parentId = null) {
//  const url = parentId
//    ? `/nodes?share_id=${shareId}&parent_id=${parentId}`
//    : `/nodes?share_id=${shareId}`;
//  return fetchJSON(url);
//}

// Second Version
//
//
//export async function fetchNodesPaged({
//  shareId,
//  parentId = null,
//  limit = 200,
//  offset = 0,
//  q = "",
//  kind = "all", // all|file|dir
//}) {
//  const params = new URLSearchParams({
//    share_id: String(shareId),
//    limit: String(limit),
//    offset: String(offset),
//    kind,
//  });
//  if (parentId !== null && parentId !== undefined) params.set("parent_id", String(parentId));
//  if (q) params.set("q", q);
//
//  const res = await fetch(`${API_BASE}/nodes?${params.toString()}`);
//  if (!res.ok) throw new Error(`Nodes API: ${res.status}`);
//  return res.json(); // { items, next_offset }
//}

// Third Version


export async function fetchNodesPaged({
  shareId,
  parentId = null,
  limit = 200,
  offset = 0,
  q = "",
  kind = "all",
  days = "",   // 👈 new
}) {
  const params = new URLSearchParams({
    share_id: String(shareId),
    limit: String(limit),
    offset: String(offset),
    kind,
  });

  if (parentId !== null && parentId !== undefined) {
    params.set("parent_id", String(parentId));
  }
  if (q) params.set("q", q);
  if (days) params.set("days_ago", days); // 👈 send to backend

  const res = await fetch(`${API_BASE}/nodes?${params.toString()}`);
  if (!res.ok) throw new Error(`Nodes API: ${res.status}`);
  return res.json();
}
