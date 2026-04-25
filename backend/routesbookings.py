import random
import string
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Booking, Schedule, Seat, User

bookings_bp = Blueprint("bookings", __name__)


def generate_pnr():
    """Generate a unique 6-character alphanumeric PNR."""
    while True:
        pnr = ''.join(random.choices(string.digits, k=6))
        if not Booking.query.filter_by(pnr=pnr).first():
            return pnr


def seat_allowed(seat: Seat, user: User) -> bool:
    """Enforce seat restrictions based on user gender and PWD status."""
    if seat.restriction == "Women" and user.gender != "Female":
        return False
    if seat.restriction == "PWD" and not user.pwd_status:
        return False
    return True


@bookings_bp.route("/", methods=["POST"])
@jwt_required()
def create_booking():
    """
    Book a specific seat on a schedule.
    Body: { "schedule_id": 1, "seat_id": 3 }
    """
    user_id = get_jwt_identity()
    d       = request.get_json()
    user     = User.query.get_or_404(user_id)
    schedule = Schedule.query.get_or_404(d["schedule_id"])
    seat     = Seat.query.get_or_404(d["seat_id"])

    # Validate seat belongs to the scheduled bus
    if seat.bus_id != schedule.bus_id:
        return jsonify({"error": "Seat does not belong to this schedule's bus"}), 400

    if seat.seat_status == "Booked":
        return jsonify({"error": "Seat already booked"}), 409

    if not seat_allowed(seat, user):
        return jsonify({"error": f"Seat {seat.seat_no} is restricted to {seat.restriction} only"}), 403

    # Create booking
    booking = Booking(
        user_id     = user_id,
        schedule_id = schedule.schedule_id,
        seat_id     = seat.seat_id,
        pnr         = generate_pnr(),
        total_fee   = schedule.fare
    )
    seat.seat_status = "Booked"   # Lock the seat
    db.session.add(booking)
    db.session.commit()

    return jsonify({
        "message":    "Booking confirmed",
        "booking_id": booking.booking_id,
        "pnr":        booking.pnr,
        "seat":       seat.seat_no,
        "route":      schedule.route.route_name,
        "departure":  schedule.departure_time.isoformat(),
        "total_fee":  float(booking.total_fee)
    }), 201


@bookings_bp.route("/my", methods=["GET"])
@jwt_required()
def my_bookings():
    """Get all bookings for the logged-in user."""
    user_id  = get_jwt_identity()
    bookings = Booking.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "booking_id": b.booking_id,
        "pnr":        b.pnr,
        "route":      b.schedule.route.route_name,
        "bus":        b.schedule.bus.bus_number,
        "seat_no":    b.seat.seat_no,
        "seat_type":  b.seat.seat_type,
        "departure":  b.schedule.departure_time.isoformat(),
        "total_fee":  float(b.total_fee)
    } for b in bookings])


@bookings_bp.route("/<int:booking_id>/cancel", methods=["DELETE"])
@jwt_required()
def cancel_booking(booking_id):
    """Cancel a booking and free the seat."""
    user_id = get_jwt_identity()
    booking = Booking.query.filter_by(
        booking_id=booking_id, user_id=user_id
    ).first_or_404()

    booking.seat.seat_status = "Available"   # Free the seat
    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": f"Booking {booking_id} cancelled, seat freed"})


@bookings_bp.route("/pnr/<string:pnr>", methods=["GET"])
def lookup_pnr(pnr):
    """Look up a booking by PNR (public, no auth needed)."""
    b = Booking.query.filter_by(pnr=pnr).first_or_404()
    return jsonify({
        "pnr":       b.pnr,
        "passenger": b.user.name,
        "route":     b.schedule.route.route_name,
        "seat_no":   b.seat.seat_no,
        "departure": b.schedule.departure_time.isoformat(),
        "total_fee": float(b.total_fee)
    })
