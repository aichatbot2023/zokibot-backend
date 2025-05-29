from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

openai.api_key = "OVDE_STAVI_TVOJ_API_KLJUC"

predefined_responses = {
    "do you import teslas?": "✅ Yes! Kibost Car is an official Tesla importer. Learn more here: https://kibostcar.com/uvoznik-tesla-srbija/",
    "da li uvozite tesle?": "✅ Da, Kibost Car je zvanični uvoznik Tesla vozila. Više informacija: https://kibostcar.com/uvoznik-tesla-srbija/",
    # Dodaj još ako želiš...
}

@app.route("/api/zokibot", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip().lower()

    if user_message in predefined_responses:
        return jsonify({"response": predefined_responses[user_message]})

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Zokibot, a helpful and professional assistant for Kibost Car."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = completion.choices[0].message.content.strip()
        return jsonify({"response": reply})
    except Exception:
        return jsonify({"response": "⚠️ Trenutno ne možemo da odgovorimo. Molimo pokušajte kasnije."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
