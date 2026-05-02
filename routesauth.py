from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import db, User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    d = request.get_json()
    if User.query.filter_by(email=d["email"]).first():
        return jsonify({"error": "Email already registered"}), 400

    user = User(
        name       = d["name"],
        gender     = d.get("gender", "Other"),
        pwd_status = d.get("pwd_status", False),
        email      = d["email"],
        password   = generate_password_hash(d["password"]),
        phone      = d.get("phone")
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    d = request.get_json()
    user = User.query.filter_by(email=d["email"]).first()
    if not user or not check_password_hash(user.password, d["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_access_token(identity=str(user.user_id))
    return jsonify({
        "access_token": token,
        "user": {
            "id":         user.user_id,
            "name":       user.name,
            "gender":     user.gender,
            "pwd_status": user.pwd_status
        }
    })
