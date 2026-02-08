// ------- Helpers -------
function getToken() {
  return localStorage.getItem("access_token");
}

function setToken(token) {
  localStorage.setItem("access_token", token);
}

function clearToken() {
  localStorage.removeItem("access_token");
}

function authHeaders(extra = {}) {
  const t = getToken();
  return {
    ...extra,
    ...(t ? { "Authorization": `Bearer ${t}` } : {}),
  };
}

async function apiFetch(url, options = {}) {
  const res = await fetch(url, options);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = data?.error?.message || `HTTP ${res.status}`;
    const code = data?.error?.code || "ERROR";
    throw { status: res.status, code, message: msg, data };
  }
  return data;
}

function requireAuthOrRedirect() {
  if (!getToken()) {
    window.location.href = "/login/";
  }
}

function logout() {
  clearToken();
  window.location.href = "/login/";
}

// ------- Auth -------
async function doLogin(phone, password) {
  const data = await apiFetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone, password }),
  });
  setToken(data.access_token);
  return data;
}

async function doRegister(name, phone, password) {
  const data = await apiFetch("/api/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, phone, password }),
  });
  setToken(data.access_token);
  return data;
}

// ------- Trips -------
async function fetchTrips(params = {}) {
  const qs = new URLSearchParams(params).toString();
  const url = qs ? `/api/trips?${qs}` : "/api/trips";
  return apiFetch(url, { headers: authHeaders() });
}

async function fetchTrip(tripId) {
  return apiFetch(`/api/trips/${tripId}`, { headers: authHeaders() });
}

// ------- Seats -------
async function fetchSeats(tripId) {
  return apiFetch(`/api/trips/${tripId}/seats`, { headers: authHeaders() });
}

// ------- Reservations -------
async function createReservation(tripId, seatIds) {
  return apiFetch("/api/reservations", {
    method: "POST",
    headers: authHeaders({ "Content-Type": "application/json" }),
    body: JSON.stringify({ trip_id: tripId, seat_ids: seatIds }),
  });
}

async function fetchReservations(params = {}) {
  const qs = new URLSearchParams(params).toString();
  const url = qs ? `/api/reservations?${qs}` : "/api/reservations";
  return apiFetch(url, { headers: authHeaders() });
}

async function cancelReservation(reservationId) {
  return apiFetch(`/api/reservations/${reservationId}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
}