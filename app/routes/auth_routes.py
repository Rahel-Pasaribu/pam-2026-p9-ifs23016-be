from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)

# Data akun statis
USER_DATA = {
    "username": "Acel",
    "password": "acel123"
}

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Data tidak ditemukan"}), 400

    username = data.get("username")
    password = data.get("password")

    if username == USER_DATA["username"] and password == USER_DATA["password"]:
        # Mengembalikan token dummy untuk keperluan praktikum
        return jsonify({
            "message": "Login berhasil!",
            "token": "dummy-token-acel-123",
            "user": {
                "username": "acel",
            }
        }), 200

    return jsonify({"error": "Username atau password salah!"}), 401

@auth_bp.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logout berhasil!"}), 200
