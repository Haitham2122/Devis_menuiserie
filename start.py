#!/usr/bin/env python3
"""
Script de démarrage pour l'application Modificateur de Devis PDF
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    try:
        import fastapi
        import uvicorn
        import PyPDF2
        import reportlab
        print("✅ Toutes les dépendances sont installées")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("📦 Installation des dépendances...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dépendances installées avec succès")
            return True
        except subprocess.CalledProcessError:
            print("❌ Erreur lors de l'installation des dépendances")
            return False

def create_directories():
    """Crée les répertoires nécessaires"""
    directories = ["static", "uploads", "output"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("📁 Répertoires créés/vérifiés")

def start_application():
    """Démarre l'application FastAPI"""
    print("🚀 Démarrage de l'application...")
    print("📍 URL: http://localhost:8000")
    print("⏹️  Appuyez sur Ctrl+C pour arrêter")
    
    # Ouvrir le navigateur après un délai
    def open_browser():
        time.sleep(2)
        webbrowser.open("http://localhost:8000")
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Démarrer le serveur
    try:
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n👋 Application arrêtée")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")

def main():
    """Fonction principale"""
    print("🔧 Modificateur de Devis PDF")
    print("=" * 40)
    
    # Vérifier les dépendances
    if not check_dependencies():
        return
    
    # Créer les répertoires
    create_directories()
    
    # Démarrer l'application
    start_application()

if __name__ == "__main__":
    main() 