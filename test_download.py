#!/usr/bin/env python3
"""
Script de test pour analyser le problème de téléchargement
"""

import requests
import os

def test_upload_download():
    """Test de l'upload et téléchargement"""
    
    # Vérifier qu'il y a un PDF de test
    test_files = []
    if os.path.exists("static"):
        test_files = [f for f in os.listdir("static") if f.endswith('.pdf')]
    
    if not test_files:
        print("❌ Aucun fichier PDF de test trouvé dans static/")
        return
    
    test_file = os.path.join("static", test_files[0])
    print(f"📄 Test avec: {test_file}")
    
    # Test de l'endpoint
    url = "http://localhost:8000/upload-pdf/"
    
    try:
        with open(test_file, 'rb') as f:
            files = {'file': (test_files[0], f, 'application/pdf')}
            
            print("🔧 Envoi du fichier...")
            response = requests.post(url, files=files)
            
            print(f"📊 Status Code: {response.status_code}")
            print(f"📊 Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                print(f"✅ Réponse OK - Taille: {len(response.content)} bytes")
                
                # Sauvegarder le fichier de test
                output_file = f"test_download_{test_files[0]}"
                with open(output_file, 'wb') as out:
                    out.write(response.content)
                print(f"💾 Fichier sauvegardé: {output_file}")
                
            else:
                print(f"❌ Erreur: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'application")
        print("💡 Assurez-vous que l'application est démarrée avec: python main.py")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_upload_download() 