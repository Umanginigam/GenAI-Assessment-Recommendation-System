const API_BASE = "http://127.0.0.1:8000";

export async function fetchRecommendations(query) {
  const response = await fetch(`${API_BASE}/recommend`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch recommendations");
  }

  return response.json();
}
