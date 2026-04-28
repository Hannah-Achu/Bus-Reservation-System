const API = "http://localhost:5000/api";
const getToken = () => localStorage.getItem("token");

async function req(endpoint, method = "GET", body = null, auth = false) {
    const headers = { "Content-Type": "application/json" };
    if (auth) headers["Authorization"] = `Bearer ${getToken()}`;
    const res = await fetch(`${API}${endpoint}`, {
        method, headers,
        body: body ? JSON.stringify(body) : null
    });
    if (!res.ok) throw await res.json();
    return res.json();
}

// ── Auth ─────────────────────────────────────────────────
async function register(name, gender, pwdStatus, email, password, phone) {
    return req("/auth/register", "POST", {
        name, gender, pwd_status: pwdStatus, email, password, phone
    });
}

async function login(email, password) {
    const data = await register("/auth/login", "POST", { email, password });
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user", JSON.stringify(data.user));
    return data;
}

// ── Search ────────────────────────────────────────────────
async function searchSchedules(origin, destination, date) {
    const params = new URLSearchParams({ origin, destination, date });
    return req(`/buses/search?${params}`);
}

// ── Seats ─────────────────────────────────────────────────
async function getSeats(busId) {
    return req(`/buses/${busId}/seats`);
}

// ── Bookings ──────────────────────────────────────────────
async function bookSeat(scheduleId, seatId) {
    return req("/bookings/", "POST", { schedule_id: scheduleId, seat_id: seatId }, true);
}

async function myBookings() {
    return req("/bookings/my", "GET", null, true);
}

async function cancelBooking(bookingId) {
    return req(`/bookings/${bookingId}/cancel`, "DELETE", null, true);
}

async function lookupPNR(pnr) {
    return req(`/bookings/pnr/${pnr}`);
}
