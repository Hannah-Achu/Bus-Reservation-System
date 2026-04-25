import os

class Config:
    SECRET_KEY          = os.environ.get("SECRET_KEY", "dev-secret")
    JWT_SECRET_KEY      = os.environ.get("JWT_SECRET_KEY", "jwt-secret")
    # Point to your existing MySQL database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:yourpassword@localhost/BusReservationSystem"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

