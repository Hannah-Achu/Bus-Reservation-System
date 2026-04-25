from flask import Flask, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from routesauth import auth_bp
from routesbuses import buses_bp
from routesbookings import bookings_bp

def create_app():
    app = Flask(__name__)
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
    
    return app
    

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
