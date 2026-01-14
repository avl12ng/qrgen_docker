import io
import zipfile
import qrcode
from flask import Flask, render_template_string, request, send_file

app = Flask(__name__)

# Le code HTML est intégré ici pour n'avoir qu'un seul fichier à gérer
HTML_TEMPLATE = '''
<!doctype html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Générateur QR Docker</title>
    <link rel="stylesheet" href="https://unpkg.com/mvp.css">
    <style>
        body { max-width: 800px; margin: 0 auto; padding: 20px; }
        header { text-align: center; margin-bottom: 40px; }
        textarea { width: 100%; height: 100px; }
    </style>
</head>
<body>
    <header>
        <h1>Générateur QR Code</h1>
        <p>Interface web sous Docker - Génération Unitaire & Batch</p>
    </header>

    <main>
        <section>
            <form method="post">
                <header><h2>Option 1 : Génération Unique</h2></header>
                <label for="text_data">Entrez le texte ou l'URL :</label>
                <input type="text" id="text_data" name="text_data" placeholder="Ex: https://monsite.com">
                <button type="submit">Télécharger le QR (PNG)</button>
            </form>
        </section>

        <hr>

        <section>
            <form method="post" enctype="multipart/form-data">
                <header><h2>Option 2 : Import Fichier (Batch)</h2></header>
                <label for="file_data">Importez un fichier .txt ou .csv (une valeur par ligne) :</label>
                <input type="file" id="file_data" name="file_data" accept=".csv, .txt">
                <button type="submit">Générer et télécharger le ZIP</button>
            </form>
        </section>
    </main>
</body>
</html>
'''

def generate_qr_io(data):
    """Génère un QR code et le retourne sous forme de bytes en mémoire."""
    img = qrcode.make(data)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # --- CAS 1 : TEXTE UNIQUE ---
        text_data = request.form.get('text_data')
        if text_data:
            buf = generate_qr_io(text_data)
            return send_file(buf, mimetype='image/png', as_attachment=True, download_name="qrcode.png")

        # --- CAS 2 : FICHIER IMPORTÉ ---
        file = request.files.get('file_data')
        if file and file.filename != '':
            try:
                # Lecture et décodage du fichier
                content_str = file.read().decode('utf-8')
                lines = content_str.splitlines()
            except UnicodeDecodeError:
                return "Erreur : Le fichier n'est pas en UTF-8.", 400
            
            # Création du ZIP en mémoire
            memory_file = io.BytesIO()
            with zipfile.ZipFile(memory_file, 'w') as zf:
                count = 0
                for i, line in enumerate(lines):
                    clean_line = line.strip()
                    if clean_line: # On ignore les lignes vides
                        qr_buf = generate_qr_io(clean_line)
                        # Nom du fichier dans le zip : qr_1.png, qr_2.png...
                        filename = f"qr_{i+1}.png"
                        zf.writestr(filename, qr_buf.getvalue())
                        count += 1
            
            if count == 0:
                return "Le fichier est vide.", 400

            memory_file.seek(0)
            return send_file(memory_file, mimetype='application/zip', as_attachment=True, download_name="qrcodes_pack.zip")

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    # Écoute sur 0.0.0.0 indispensable pour Docker
    app.run(host='0.0.0.0', port=5050)
