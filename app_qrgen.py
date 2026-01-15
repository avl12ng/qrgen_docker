import io
import os
import zipfile
import qrcode
from flask import Flask, render_template_string, request, send_file, abort
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# ==========================================
# CONFIGURATION
# ==========================================
# Read values from environment variables
API_TOKEN = os.getenv("API_TOKEN", "default_secret_token")
PORT = int(os.getenv("PORT", 5050))

# ==========================================
# I18N DICTIONARY
# ==========================================
I18N = {
    'fr': {
        'title': "Générateur de QR Code",
        'subtitle': "Outil interne - Unitaire & Batch",
        'single_title': "Génération Unique",
        'single_label': "Texte ou URL :",
        'single_btn': "Télécharger le PNG",
        'batch_title': "Import par fichier (Batch)",
        'batch_label': "Fichier .txt ou .csv (un QR par ligne) :",
        'batch_btn': "Générer le Pack ZIP",
        'footer': "Point d'entrée API activé et sécurisé.",
        'err_encoding': "Erreur d'encodage : le fichier doit être en UTF-8",
        'err_empty': "Le fichier est vide.",
        'switch': "English"
    },
    'en': {
        'title': "QR Code Generator",
        'subtitle': "Internal tool - Single & Batch",
        'single_title': "Single Generation",
        'single_label': "Text or URL:",
        'single_btn': "Download PNG",
        'batch_title': "Batch Import",
        'batch_label': "File .txt or .csv (one QR per line):",
        'batch_btn': "Generate ZIP Pack",
        'footer': "API endpoint active and secured.",
        'err_encoding': "Encoding error: file must be UTF-8",
        'err_empty': "File is empty.",
        'switch': "Français"
    }
}

HTML_TEMPLATE = '''
<!doctype html>
<html lang="{{ lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ t.title }}</title>
    <link rel="stylesheet" href="https://unpkg.com/mvp.css">
    <style>
        :root { --accent: #007bff; }
        body { max-width: 800px; margin: 0 auto; padding: 20px; font-family: sans-serif; }
        header { text-align: center; margin-bottom: 30px; }
        .lang-switch { text-align: right; margin-bottom: 10px; }
        .lang-switch a { font-size: 0.8em; text-decoration: underline; cursor: pointer; }
        section { padding: 20px; border-radius: 8px; border: 1px solid #eee; margin-bottom: 20px; }
        input[type="text"], input[type="file"] { width: 100%; margin-bottom: 10px; }
        @media (max-width: 600px) { body { padding: 10px; } button { width: 100%; } }
    </style>
</head>
<body>
    <div class="lang-switch">
        <a href="/?lang={{ 'en' if lang == 'fr' else 'fr' }}">{{ t.switch }}</a>
    </div>
    <header>
        <h1>{{ t.title }}</h1>
        <p>{{ t.subtitle }}</p>
    </header>
    <main>
        <section>
            <form method="post" action="/{{ '?lang=' + lang }}">
                <h2>{{ t.single_title }}</h2>
                <label>{{ t.single_label }}</label>
                <input type="text" name="text_data" placeholder="https://..." required>
                <button type="submit">{{ t.single_btn }}</button>
            </form>
        </section>
        <section>
            <form method="post" enctype="multipart/form-data" action="/{{ '?lang=' + lang }}">
                <h2>{{ t.batch_title }}</h2>
                <label>{{ t.batch_label }}</label>
                <input type="file" name="file_data" accept=".csv, .txt" required>
                <button type="submit">{{ t.batch_btn }}</button>
            </form>
        </section>
    </main>
    <footer style="text-align: center; color: #666; font-size: 0.8em; margin-top: 30px;">
        {{ t.footer }}
    </footer>
</body>
</html>
'''

def generate_qr_buffer(data):
    """Generates a QR code image and returns it as an in-memory BytesIO buffer."""
    qr = qrcode.QRCode(border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

def get_current_locale():
    """Detects locale: URL parameter takes priority over Browser settings."""
    lang_param = request.args.get('lang')
    if lang_param in ['fr', 'en']:
        return lang_param
    accept_languages = request.headers.get('Accept-Language', '')
    return 'fr' if 'fr' in accept_languages.lower() else 'en'

@app.route('/', methods=['GET', 'POST'])
def index():
    lang = get_current_locale()
    t = I18N[lang]

    if request.method == 'POST':
        text_data = request.form.get('text_data')
        if text_data:
            buf = generate_qr_buffer(text_data)
            return send_file(buf, mimetype='image/png', as_attachment=True, download_name="qrcode.png")

        file = request.files.get('file_data')
        if file and file.filename != '':
            try:
                lines = file.read().decode('utf-8').splitlines()
            except UnicodeDecodeError:
                return t['err_encoding'], 400
            
            memory_file = io.BytesIO()
            with zipfile.ZipFile(memory_file, 'w') as zf:
                count = 0
                for i, line in enumerate(lines):
                    content = line.strip()
                    if content:
                        qr_buf = generate_qr_buffer(content)
                        zf.writestr(f"qr_{i+1}.png", qr_buf.getvalue())
                        count += 1
                if count == 0: return t['err_empty'], 400

            memory_file.seek(0)
            return send_file(memory_file, mimetype='application/zip', as_attachment=True, download_name="qrcodes_batch.zip")

    return render_template_string(HTML_TEMPLATE, t=t, lang=lang)

@app.route('/api/generate', methods=['GET'])
def api_generate():
    """Secure API endpoint using token from environment."""
    user_token = request.args.get('token')
    if user_token != API_TOKEN:
        abort(403)

    data = request.args.get('data')
    if not data:
        return {"error": "Missing 'data' parameter"}, 400
    
    buf = generate_qr_buffer(data)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
