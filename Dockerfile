# Image de base légère
FROM python:3.11-slim

# Dossier de travail dans le conteneur
WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code de l'application
COPY app_qrgen.py .

# On informe Docker que le conteneur écoute sur le port 5000
EXPOSE 5050

# Commande de démarrage
CMD ["python", "app_qrgen.py"]
