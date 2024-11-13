from flask import Flask, request, jsonify, render_template
from google.cloud import translate_v2 as translate
import os

app = Flask(__name__)

# Load credentials from environment variable if deployed, else use `key.json` locally
if os.getenv("GOOGLE_CREDENTIALS"):
    credentials_info = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
    translate_client = translate.Client.from_service_account_info(credentials_info)
else:
    translate_client = translate.Client.from_service_account_json("key.json")

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

# Initialize the Translation client
translate_client = translate.Client()

@app.route('/')
def index():
    """Serve the HTML frontend."""
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    """Handle translation requests."""
    try:
        # Parse the incoming JSON request
        data = request.get_json()
        text = data.get('text')
        target_language = data.get('target_language')

        if not text or not target_language:
            return jsonify({"error": "Missing 'text' or 'target_language'"}), 400

        # Debugging: Print incoming text and target language
        print(f"Text to translate: {text}")
        print(f"Target language: {target_language}")

        # Perform the translation
        translation = translate_client.translate(text, target_language=target_language)

        # Debugging: Print the translated text
        print(f"Translation: {translation['translatedText']}")

        return jsonify({"translation": translation['translatedText']})
    except Exception as e:
        # Debugging: Print the exception
        print(f"Error during translation: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

