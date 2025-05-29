#!/usr/bin/env python3
"""
Script de test pour le nettoyage PyMuPDF du devis ADF
"""

import os
from pdf_cleaner import PDFCleaner

def test_nettoyage_pymupdf():
    """Test du nettoyage avec PyMuPDF"""
    
    print("🧹 Test de Nettoyage PyMuPDF - Devis ADF")
    print("=" * 45)
    
    # Créer le nettoyeur
    cleaner = PDFCleaner()
    
    # Créer les répertoires nécessaires
    os.makedirs("static", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    # Chercher le fichier PDF ADF dans static
    pdf_files = [f for f in os.listdir("static") if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("❌ Aucun fichier PDF trouvé dans le dossier 'static/'")
        print("💡 Placez votre devis ADF dans le dossier 'static/' et relancez le test")
        return False
    
    print(f"📄 Fichiers PDF trouvés: {pdf_files}")
    
    for pdf_file in pdf_files:
        input_path = os.path.join("static", pdf_file)
        
        print(f"\n🔧 Traitement de: {pdf_file}")
        
        # 1. Créer un aperçu des zones à masquer
        preview_path = os.path.join("output", f"aperçu_zones_{pdf_file}")
        print(f"   📋 Création de l'aperçu des zones...")
        preview_success = cleaner.preview_zones(input_path, preview_path)
        
        if preview_success:
            print(f"   ✅ Aperçu créé: aperçu_zones_{pdf_file}")
        else:
            print(f"   ❌ Erreur lors de la création de l'aperçu")
        
        # 2. Nettoyer le PDF (sans zones optionnelles)
        output_path = os.path.join("output", f"nettoyé_{pdf_file}")
        print(f"   🧹 Nettoyage en cours...")
        
        # Obtenir les informations du PDF original
        info_original = cleaner.get_pdf_info(input_path)
        print(f"   📊 PDF original: {info_original.get('num_pages', 'N/A')} pages")
        
        # Appliquer le nettoyage
        success = cleaner.clean_pdf(input_path, output_path, include_optional=False)
        
        if success:
            print(f"   ✅ Nettoyage réussi: nettoyé_{pdf_file}")
            
            # Vérifier le résultat
            info_nettoye = cleaner.get_pdf_info(output_path)
            print(f"   📊 PDF nettoyé: {info_nettoye.get('num_pages', 'N/A')} pages")
            
        else:
            print(f"   ❌ Erreur lors du nettoyage de {pdf_file}")
        
        # 3. Nettoyer avec zones optionnelles (VISCOGLIOSI)
        output_path_full = os.path.join("output", f"nettoyé_complet_{pdf_file}")
        print(f"   🧹 Nettoyage complet (avec VISCOGLIOSI)...")
        
        success_full = cleaner.clean_pdf(input_path, output_path_full, include_optional=True)
        
        if success_full:
            print(f"   ✅ Nettoyage complet réussi: nettoyé_complet_{pdf_file}")
        else:
            print(f"   ❌ Erreur lors du nettoyage complet")
    
    print(f"\n📁 Fichiers disponibles dans 'output/':")
    print(f"   - aperçu_zones_*.pdf : Aperçu des zones à masquer")
    print(f"   - nettoyé_*.pdf : PDF nettoyé (standard)")
    print(f"   - nettoyé_complet_*.pdf : PDF nettoyé (avec VISCOGLIOSI)")
    
    return True

def afficher_zones_pymupdf():
    """Affiche les zones configurées dans PyMuPDF"""
    
    print("\n🎯 Zones de nettoyage PyMuPDF:")
    print("-" * 35)
    
    cleaner = PDFCleaner()
    
    print("📄 Page 1 uniquement:")
    for i, zone in enumerate(cleaner.zones_to_clean['page1_only'], 1):
        rect = zone['rect']
        print(f"   Zone {i}: {zone['description']}")
        print(f"           Coordonnées: ({rect[0]}, {rect[1]}, {rect[2]}, {rect[3]})")
    
    print("\n📄 Toutes les pages:")
    for i, zone in enumerate(cleaner.zones_to_clean['all_pages'], 1):
        rect = zone['rect']
        print(f"   Zone {i}: {zone['description']}")
        print(f"           Coordonnées: ({rect[0]}, {rect[1]}, {rect[2]}, {rect[3]})")
    
    print("\n📄 Zones optionnelles (VISCOGLIOSI):")
    for name, zone in cleaner.optional_zones.items():
        rect = zone['rect']
        print(f"   {zone['description']}")
        print(f"           Coordonnées: ({rect[0]}, {rect[1]}, {rect[2]}, {rect[3]})")
    
    print(f"\n💡 Basé sur votre code PyMuPDF original")

def main():
    """Fonction principale"""
    
    # Afficher les zones configurées
    afficher_zones_pymupdf()
    
    # Lancer le test de nettoyage
    success = test_nettoyage_pymupdf()
    
    if success:
        print("\n🎉 Test PyMuPDF terminé!")
        print("\n📖 Prochaines étapes:")
        print("   1. Vérifiez l'aperçu des zones dans 'output/'")
        print("   2. Comparez les versions nettoyées")
        print("   3. Ajustez les coordonnées si nécessaire")
        print("   4. Passez à la phase suivante (ajout de contenu)")
    else:
        print("\n❌ Placez votre devis ADF dans 'static/' et relancez")

if __name__ == "__main__":
    main() 