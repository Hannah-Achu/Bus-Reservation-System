from flask import Flask, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from routesauth import auth_bp
from routesbuses import buses_bp
from routesbookings import bookings_bp
import os
def create_app():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "templates"),
        static_folder=os.path.join(BASE_DIR, "static")
    )

    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)
    JWTManager(app)
    app.register_blueprint(auth_bp,      url_prefix="/api/auth")
    app.register_blueprint(buses_bp,     url_prefix="/api/buses")
    app.register_blueprint(bookings_bp,  url_prefix="/api/bookings")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/login")
    def login_page():
        return render_template("login.html")

    @app.route("/search")
    def search_page():
        return render_template("search.html")

    @app.route("/profile")
    def profile_page():
        return render_template("profile.html")

    @app.route("/my-bookings")
    def my_bookings_page():
        return render_template("booking.html")

    @app.route("/select-seats")
    def select_seats_page():
        return render_template("select_seats.html")

    return app
    

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
