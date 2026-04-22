from app.extensions import SessionLocal
from app.models.motivation import Motivation
from app.models.request_log import RequestLog
from app.services.llm_service import generate_from_llm
from app.utils.parser import parse_llm_response

def create_book_recommendations(genre: str, total: int):
    session = SessionLocal()

    try:
        prompt = f"""
        Anda adalah seorang kurator buku berpengalaman. Dalam format JSON, buat {total} rekomendasi buku yang sangat cocok untuk seseorang yang menyukai genre "{genre}".
        Setiap rekomendasi harus mencakup atribut berikut:
        - Judul
        - Pengarang
        - Tahun Terbit
        - Sinopsis Singkat
        - Alasan Rekomendasi
        - Rating (skala 1-10)

        Format JSON harus seperti ini:
        {{
            "motivations": [
                {{
                    "text": "Judul: [judul], Pengarang: [nama], Tahun Terbit: [tahun], Sinopsis: [sinopsis singkat], Alasan: [alasan rekomendasi], Rating: [angka]/10"
                }}
            ]
        }}
        PENTING: Hanya berikan JSON, jangan ada teks penjelasan lain. Gunakan bahasa Indonesia.
        """

        result = generate_from_llm(prompt)
        recommendations = parse_llm_response(result)

        # save request log (menggunakan field theme untuk menyimpan genre)
        req_log = RequestLog(theme=genre)
        session.add(req_log)
        session.commit()

        saved = []

        for item in recommendations:
            text = item.get("text")

            m = Motivation(
                text=text,
                request_id=req_log.id
            )
            session.add(m)
            saved.append(text)

        session.commit()

        return saved

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def get_all_book_recommendations(page: int = 1, per_page: int = 100):
    session = SessionLocal()

    try:
        query = session.query(Motivation)

        total = query.count()

        data = (
            query
            .order_by(Motivation.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        result = [
            {
                "id": m.id,
                "text": m.text,
                "created_at": m.created_at.isoformat()
            }
            for m in data
        ]

        return {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page,
            "data": result
        }

    finally:
        session.close()