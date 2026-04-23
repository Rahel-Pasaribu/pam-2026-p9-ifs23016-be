from flask import Blueprint, request, jsonify
from app.services.motivation_service import (
    create_book_recommendations,
    get_all_book_recommendations
)

motivation_bp = Blueprint("motivation", __name__)

@motivation_bp.route("/", methods=["GET"])
def index():
    return "API telah berjalan! Dibuat oleh Rahel Cantik!"


@motivation_bp.route("/book/generate", methods=["POST"])
def generate():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    genre = data.get("genre")
    total = data.get("total")

    if not genre:
        return jsonify({"error": "Genre is required"}), 400

    if total is None:
        return jsonify({"error": "Total is required"}), 400

    if total <= 0:
        return jsonify({"error": "Total harus besar dari 0"}), 400

    if total > 10:
        return jsonify({"error": "Total maksimal harus 10"}), 400

    try:
        result = create_book_recommendations(genre, total)

        return jsonify({
            "genre": genre,
            "total": len(result),
            "data": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@motivation_bp.route("/book", methods=["GET"])
def get_all():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=100, type=int)

    data = get_all_book_recommendations(page=page, per_page=per_page)

    return jsonify(data)