#!/usr/bin/env python3
"""
Script de test pour le nettoyage du devis ADF
"""

import os
from pdf_modifier import PDFModifier

def test_nettoyage_adf():
    """Test du nettoyage spécifique pour le devis ADF"""
    
    print("🧹 Test de Nettoyage - Devis ADF")
    print("=" * 40)
    
    # Créer le modificateur avec configuration de nettoyage
    modifier = PDFModifier()
    
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
        output_filename = f"nettoyé_{pdf_file}"
        output_path = os.path.join("output", output_filename)
        
        print(f"\n🔧 Nettoyage de: {pdf_file}")
        
        # Obtenir les informations du PDF original
        info_original = modifier.get_pdf_info(input_path)
        print(f"   📊 PDF original: {info_original.get('num_pages', 'N/A')} pages")
        
        # Appliquer le nettoyage
        success = modifier.modify_pdf(input_path, output_path)
        
        if success:
            print(f"   ✅ Nettoyage réussi: {output_filename}")
            
            # Vérifier le résultat
            info_nettoye = modifier.get_pdf_info(output_path)
            print(f"   📊 PDF nettoyé: {info_nettoye.get('num_pages', 'N/A')} pages")
            
            # Afficher les zones nettoyées
            print(f"   🧹 Zones nettoyées:")
            print(f"      - Logo ADF et cadre (haut droite)")
            print(f"      - Section promotionnelle (bas de page)")
            
        else:
            print(f"   ❌ Erreur lors du nettoyage de {pdf_file}")
    
    print(f"\n📁 Fichiers nettoyés disponibles dans 'output/'")
    return True

def afficher_zones_nettoyage():
    """Affiche les zones qui seront nettoyées"""
    
    print("\n🎯 Zones de nettoyage configurées:")
    print("-" * 35)
    
    from config import LOGO_ZONES
    
    for i, (x, y, width, height) in enumerate(LOGO_ZONES, 1):
        print(f"   Zone {i}: Position ({x}, {y}) - Taille {width}x{height}")
        
        if i == 1:
            print(f"            → Logo ADF et cadre d'informations")
        elif i == 2:
            print(f"            → Section promotionnelle en bas")
        elif i == 3:
            print(f"            → Logo ADF supplémentaire")
    
    print(f"\n💡 Pour ajuster les zones, modifiez LOGO_ZONES dans config.py")

def main():
    """Fonction principale"""
    
    # Afficher les zones de nettoyage
    afficher_zones_nettoyage()
    
    # Lancer le test de nettoyage
    success = test_nettoyage_adf()
    
    if success:
        print("\n🎉 Test de nettoyage terminé!")
        print("\n📖 Prochaines étapes:")
        print("   1. Vérifiez les PDF nettoyés dans 'output/'")
        print("   2. Ajustez les zones dans config.py si nécessaire")
        print("   3. Relancez le test jusqu'à satisfaction")
        print("   4. Passez à la phase suivante (ajout de texte/couleurs)")
    else:
        print("\n❌ Placez votre devis ADF dans 'static/' et relancez")

if __name__ == "__main__":
    main() 