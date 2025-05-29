#!/usr/bin/env python3
"""
Script de test pour l'API du modificateur de PDF
"""

import requests
import os
import time

def test_api():
    """Test simple de l'API"""
    base_url = "http://localhost:8000"
    
    print("🧪 Test de l'API Modificateur de PDF")
    print("=" * 40)
    
    # Test 1: Vérifier que le serveur répond
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Serveur accessible")
        else:
            print(f"❌ Erreur serveur: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Impossible de se connecter au serveur: {e}")
        print("💡 Assurez-vous que l'application est démarrée avec 'python start.py'")
        return False
    
    # Test 2: Vérifier l'upload de PDF
    test_pdf = "static/sample_devis.pdf"
    if os.path.exists(test_pdf):
        try:
            with open(test_pdf, 'rb') as f:
                files = {'file': ('test.pdf', f, 'application/pdf')}
                response = requests.post(f"{base_url}/upload-pdf/", files=files, timeout=30)
                
            if response.status_code == 200:
                result = response.json()
                print("✅ Upload et modification réussis")
                print(f"📄 Fichier modifié: {result.get('filename', 'N/A')}")
                print(f"🔗 URL de téléchargement: {result.get('download_url', 'N/A')}")
                return True
            else:
                print(f"❌ Erreur lors de l'upload: {response.status_code}")
                print(f"   Détails: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur lors de l'upload: {e}")
            return False
    else:
        print(f"❌ Fichier de test non trouvé: {test_pdf}")
        return False

def wait_for_server(max_wait=30):
    """Attend que le serveur soit prêt"""
    print("⏳ Attente du démarrage du serveur...")
    
    for i in range(max_wait):
        try:
            response = requests.get("http://localhost:8000", timeout=2)
            if response.status_code == 200:
                print("✅ Serveur prêt!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(1)
        if i % 5 == 0:
            print(f"   Attente... ({i}/{max_wait}s)")
    
    print("❌ Timeout: le serveur n'a pas démarré à temps")
    return False

if __name__ == "__main__":
    # Attendre que le serveur soit prêt
    if wait_for_server():
        # Lancer les tests
        success = test_api()
        if success:
            print("\n🎉 Tous les tests sont passés!")
            print("🌐 Ouvrez http://localhost:8000 dans votre navigateur")
        else:
            print("\n❌ Certains tests ont échoué")
    else:
        print("\n❌ Impossible de se connecter au serveur")
        print("💡 Démarrez l'application avec: python start.py") 