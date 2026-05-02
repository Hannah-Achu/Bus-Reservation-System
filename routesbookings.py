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
    try:
        user_id = int(get_jwt_identity())
        print(f"DEBUG user_id: {user_id}")

        d = request.get_json(force=True, silent=True)
        print(f"DEBUG request body: {d}")

        if not d:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        user     = User.query.get(user_id)
        schedule = Schedule.query.get(d.get("schedule_id"))
        seat     = Seat.query.get(d.get("seat_id"))

        print(f"DEBUG user: {user}, schedule: {schedule}, seat: {seat}")

        if not user:
            return jsonify({"error": "User not found"}), 404
        if not schedule:
            return jsonify({"error": "Schedule not found"}), 404
        if not seat:
            return jsonify({"error": "Seat not found"}), 404

        if seat.bus_id != schedule.bus_id:
            return jsonify({"error": "Seat does not belong to this bus"}), 400
        if seat.seat_status == "Booked":
            return jsonify({"error": "Seat is already booked"}), 409
        if not seat_allowed(seat, user):
            return jsonify({"error": f"Seat restricted to {seat.restriction} only"}), 403

        booking = Booking(
            user_id     = user_id,
            schedule_id = schedule.schedule_id,
            seat_id     = seat.seat_id,
            pnr         = generate_pnr(),
            total_fee   = schedule.fare
        )
        seat.seat_status = "Booked"
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

    except Exception as e:
        print(f"DEBUG ERROR: {str(e)}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@bookings_bp.route("/my", methods=["GET"])
@jwt_required()
def my_bookings():
    """Get all bookings for the logged-in user."""
    user_id  = int(get_jwt_identity())
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
    user_id = int(get_jwt_identity())
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
        "booking_id": b.booking_id,
        "pnr":        b.pnr,
        "route":      b.schedule.route.route_name,
        "bus":        b.schedule.bus.bus_number,
        "bus_type":   b.schedule.bus.bus_type,
        "seat_no":    b.seat.seat_no,
        "seat_type":  b.seat.seat_type,
        "departure":  b.schedule.departure_time.isoformat(),
        "total_fee":  float(b.total_fee)
    })
