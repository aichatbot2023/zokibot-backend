from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Bezbedno učitavanje OpenAI API ključa
openai.api_key = os.getenv("OPENAI_API_KEY")

# Predefinisani odgovori
predefined_responses = {
    "do you import teslas?": "✅ Yes! Kibost Car is an official Tesla importer. Learn more here: https://kibostcar.com/uvoznik-tesla-srbija/",
    "da li uvozite tesle?": "✅ Da, Kibost Car je zvanični uvoznik Tesla vozila. Više informacija: https://kibostcar.com/uvoznik-tesla-srbija/",
    "do you offer rentals?": "🚗 Yes, we offer Tesla rentals. Choose your model: https://kibostcar.com/rent-a-car-usluge/",
    "da li nudite rentiranje?": "🚗 Naravno! Pogledajte našu ponudu Tesla rent-a-car usluga: https://kibostcar.com/rent-a-car-usluge/",
    "can i rent a tesla with a driver?": "🧑‍✈️ Absolutely! Check our chauffeur service here: https://kibostcar.com/sa-licnim-vozacem/",
    "mogu li rentirati teslu sa vozačem?": "🧑‍✈️ Da! Pogledajte našu uslugu sa ličnim vozačem: https://kibostcar.com/sa-licnim-vozacem/",
    "do you sell or rent chargers?": "🔌 Yes, we rent and sell EV chargers. Details: https://kibostcar.com/iznajmljivanje-i-prodaja-punjaca/",
    "da li prodajete punjače?": "🔌 Da, iznajmljujemo i prodajemo punjače za električna vozila: https://kibostcar.com/iznajmljivanje-i-prodaja-punjaca/"
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
    except Exception as e:
        return jsonify({"response": "⚠️ Trenutno ne možemo da odgovorimo. Molimo pokušajte kasnije."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)