from flask import Blueprint, request, jsonify
from models import Schedule, Route, Bus, Seat, RouteStop, Stop

buses_bp = Blueprint("buses", __name__)


@buses_bp.route("/search", methods=["GET"])
def search_schedules():
    """
    Search by origin stop name, destination stop name, and optional date.
    GET /api/buses/search?origin=Palakkad&destination=Kochi&date=2026-04-25
    """
    origin      = request.args.get("origin", "")
    destination = request.args.get("destination", "")
    date        = request.args.get("date")          # YYYY-MM-DD

    # Find routes that contain both the origin and destination stops
    origin_routes = db.session.query(RouteStop.route_id)\
        .join(Stop, Stop.stop_id == RouteStop.stop_id)\
        .filter(Stop.stop_name.ilike(f"%{origin}%")).subquery()

    dest_routes = db.session.query(RouteStop.route_id)\
        .join(Stop, Stop.stop_id == RouteStop.stop_id)\
        .filter(Stop.stop_name.ilike(f"%{destination}%")).subquery()

    matching_route_ids = db.session.query(origin_routes.c.route_id)\
        .filter(origin_routes.c.route_id == dest_routes.c.route_id).all()
    route_ids = [r[0] for r in matching_route_ids]

    schedules = Schedule.query.filter(Schedule.route_id.in_(route_ids)).all()

    results = []
    for s in schedules:
        if date and s.departure_time.strftime("%Y-%m-%d") != date:
            continue
        # Count available seats for this bus
        available = Seat.query.filter_by(
            bus_id=s.bus_id, seat_status="Available"
        ).count()
        results.append({
            "schedule_id":   s.schedule_id,
            "route":         s.route.route_name,
            "bus_number":    s.bus.bus_number,
            "bus_type":      s.bus.bus_type,
            "departure":     s.departure_time.isoformat(),
            "fare":          float(s.fare),
            "available_seats": available
        })

    return jsonify(results)


@buses_bp.route("/<int:bus_id>/seats", methods=["GET"])
def get_seats(bus_id):
    """
    Get all seats for a bus with their current status.
    GET /api/buses/1/seats
    """
    seats = Seat.query.filter_by(bus_id=bus_id).all()
    return jsonify([{
        "seat_id":     s.seat_id,
        "seat_no":     s.seat_no,
        "seat_type":   s.seat_type,
        "restriction": s.restriction,
        "status":      s.seat_status
    } for s in seats])


@buses_bp.route("/routes", methods=["GET"])
def get_routes():
    """List all routes with their stops in order."""
    routes = Route.query.all()
    result = []
    for r in routes:
        result.append({
            "route_id":   r.route_id,
            "route_name": r.route_name,
            "stops": [{
                "stop_name":            rs.stop.stop_name,
                "order":                rs.stop_order,
                "distance_from_start":  float(rs.distance_from_start)
            } for rs in sorted(r.stops, key=lambda x: x.stop_order)]
        })
    return jsonify(result)
