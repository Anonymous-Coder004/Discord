// utils/formatDate.js
export function formatDate(isoString) {
  return new Date(isoString).toLocaleString("en-IN", {
    year: "numeric",
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });
}
