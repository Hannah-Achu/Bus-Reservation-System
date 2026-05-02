import os

class Config:
    SECRET_KEY                     = os.environ.get("SECRET_KEY", "transitflow-secret-key-2026-secure")
    JWT_SECRET_KEY                 = os.environ.get("JWT_SECRET_KEY", "transitflow-jwt-secret-key-2026-secure")
    JWT_ALGORITHM                  = "HS256"
    JWT_TOKEN_LOCATION             = ["headers"]   # ✅ only look for token in headers
    JWT_HEADER_NAME                = "Authorization"
    JWT_HEADER_TYPE                = "Bearer"
    JWT_COOKIE_CSRF_PROTECT        = False         # ✅ disable CSRF
    # Point to your existing MySQL database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:dominion@localhost/BusReservationSystem"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

