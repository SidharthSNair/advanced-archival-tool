import { fetchJSON } from "./client";

export async function fetchNodes(shareId, parentId = null) {
  const url = parentId
    ? `/nodes?share_id=${shareId}&parent_id=${parentId}`
    : `/nodes?share_id=${shareId}`;
  return fetchJSON(url);
}
