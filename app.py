from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from gtts import gTTS
import os
import uuid

app = Flask(__name__)
CORS(app)

# Supported languages
LANGUAGES = {
    "english": "en",
    "hindi": "hi",
    "marathi": "mr"
}

@app.route('/')
def index():
    return jsonify({"message": "Multilingual Real-Time TTS API Running!"})

@app.route('/tts', methods=['POST'])
def text_to_speech():
    """Handles text-to-speech conversion with multilingual support."""
    data = request.get_json()
    text = data.get("text", "")
    language = data.get("language", "english").lower()

    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    if language not in LANGUAGES:
        return jsonify({"error": "Unsupported language"}), 400
    
    try:
        lang_code = LANGUAGES[language]
        tts = gTTS(text=text, lang=lang_code)
        filename = f"output_{uuid.uuid4().hex}.mp3"
        filepath = os.path.join("static", filename)
        
        tts.save(filepath)
        return send_file(filepath, mimetype="audio/mpeg", as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(debug=True, host="127.0.0.1", port=5000)
