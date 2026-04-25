from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    user_id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name         = db.Column(db.String(100))
    gender       = db.Column(db.Enum("Male", "Female", "Other"))
    pwd_status   = db.Column(db.Boolean, default=False)   # 1 = has disability
    email        = db.Column(db.String(100), unique=True)
    password     = db.Column(db.String(255))
    phone        = db.Column(db.String(15))
    bookings     = db.relationship("Booking", backref="user", lazy=True)


class Bus(db.Model):
    __tablename__ = "buses"
    bus_id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bus_number   = db.Column(db.String(20))
    bus_type     = db.Column(db.Enum("AC", "Non-AC"))
    total_seats  = db.Column(db.Integer)
    seats        = db.relationship("Seat", backref="bus", lazy=True)
    schedules    = db.relationship("Schedule", backref="bus", lazy=True)


class Seat(db.Model):
    __tablename__ = "seats"
    seat_id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bus_id       = db.Column(db.Integer, db.ForeignKey("buses.bus_id"))
    seat_type    = db.Column(db.Enum("Window", "Aisle", "Middle"))
    seat_no      = db.Column(db.String(5))
    restriction  = db.Column(db.Enum("None", "Women", "PWD"), default="None")
    seat_status  = db.Column(db.Enum("Available", "Booked"), default="Available")


class Stop(db.Model):
    __tablename__ = "stops"
    stop_id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stop_name    = db.Column(db.String(100))


class Route(db.Model):
    __tablename__ = "routes"
    route_id     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route_name   = db.Column(db.String(100))
    stops        = db.relationship("RouteStop", backref="route", lazy=True,
                                   order_by="RouteStop.stop_order")
    schedules    = db.relationship("Schedule", backref="route", lazy=True)


class RouteStop(db.Model):
    __tablename__ = "route_stops"
    route_id             = db.Column(db.Integer, db.ForeignKey("routes.route_id"),
                                     primary_key=True)
    stop_id              = db.Column(db.Integer, db.ForeignKey("stops.stop_id"),
                                     primary_key=True)
    stop_order           = db.Column(db.Integer)
    distance_from_start  = db.Column(db.Numeric(6, 2))
    stop                 = db.relationship("Stop")


class Schedule(db.Model):
    __tablename__ = "schedules"
    schedule_id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bus_id         = db.Column(db.Integer, db.ForeignKey("buses.bus_id"))
    route_id       = db.Column(db.Integer, db.ForeignKey("routes.route_id"))
    departure_time = db.Column(db.DateTime)
    fare           = db.Column(db.Numeric(6, 2))


class Booking(db.Model):
    __tablename__ = "bookings"
    booking_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id      = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    schedule_id  = db.Column(db.Integer, db.ForeignKey("schedules.schedule_id"))
    seat_id      = db.Column(db.Integer, db.ForeignKey("seats.seat_id"))
    pnr          = db.Column(db.String(6), unique=True)
    total_fee    = db.Column(db.Numeric(6, 2))
    schedule     = db.relationship("Schedule")
    seat         = db.relationship("Seat")
