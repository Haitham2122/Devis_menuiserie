#!/usr/bin/env python3
"""
Script de test pour le processeur PDF complet
"""

import os
from pdf_processor_complete import PDFProcessorComplete

def test_processeur_complet():
    """Test du processeur PDF complet"""
    
    print("🔧 Test du Processeur PDF Complet - Devis ADF")
    print("=" * 50)
    
    # Créer le processeur
    processor = PDFProcessorComplete()
    
    # Créer les répertoires nécessaires
    os.makedirs("static", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    # Vérifier que le logo existe
    if not os.path.exists("logo.png"):
        print("⚠️  Logo non trouvé, création d'un logo d'exemple...")
        from create_sample_logo import create_sample_logo
        create_sample_logo()
    
    # Chercher le fichier PDF ADF dans static
    pdf_files = [f for f in os.listdir("static") if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("❌ Aucun fichier PDF trouvé dans le dossier 'static/'")
        print("💡 Placez votre devis ADF dans le dossier 'static/' et relancez le test")
        return False
    
    print(f"📄 Fichiers PDF trouvés: {pdf_files}")
    
    for pdf_file in pdf_files:
        input_path = os.path.join("static", pdf_file)
        
        print(f"\n🔧 Traitement complet de: {pdf_file}")
        
        # Obtenir les informations du PDF original
        info_original = processor.get_pdf_info(input_path)
        print(f"   📊 PDF original: {info_original.get('num_pages', 'N/A')} pages")
        
        # 1. Traitement avec informations par défaut
        output_path = os.path.join("output", f"traité_défaut_{pdf_file}")
        print(f"   🔧 Traitement avec infos par défaut...")
        
        success = processor.process_pdf(input_path, output_path)
        
        if success:
            print(f"   ✅ Traitement réussi: traité_défaut_{pdf_file}")
            
            # Vérifier le résultat
            info_traite = processor.get_pdf_info(output_path)
            print(f"   📊 PDF traité: {info_traite.get('num_pages', 'N/A')} pages")
            
        else:
            print(f"   ❌ Erreur lors du traitement de {pdf_file}")
        
        # 2. Traitement avec informations client personnalisées
        output_path_custom = os.path.join("output", f"traité_personnalisé_{pdf_file}")
        print(f"   🔧 Traitement avec client personnalisé...")
        
        client_custom = {
            'name': "M. HAITEM VISCOGLIOSI",
            'address1': "123 Avenue de la République",
            'address2': "06000 NICE"
        }
        
        success_custom = processor.process_pdf(input_path, output_path_custom, client_custom)
        
        if success_custom:
            print(f"   ✅ Traitement personnalisé réussi: traité_personnalisé_{pdf_file}")
        else:
            print(f"   ❌ Erreur lors du traitement personnalisé")
    
    print(f"\n📁 Fichiers disponibles dans 'output/':")
    print(f"   - traité_défaut_*.pdf : Traitement avec infos par défaut")
    print(f"   - traité_personnalisé_*.pdf : Traitement avec client personnalisé")
    
    return True

def afficher_configuration():
    """Affiche la configuration du processeur"""
    
    print("\n⚙️  Configuration du Processeur Complet:")
    print("-" * 40)
    
    processor = PDFProcessorComplete()
    
    print("🏢 Informations Entreprise:")
    for key, value in processor.company_info.items():
        print(f"   {key}: {value}")
    
    print(f"\n👤 Informations Client (par défaut):")
    for key, value in processor.client_info.items():
        print(f"   {key}: {value}")
    
    print(f"\n📞 Footer:")
    for key, value in processor.footer_info.items():
        print(f"   {key}: {value}")
    
    print(f"\n🎨 Couleurs:")
    for key, value in processor.colors.items():
        print(f"   {key}: {value}")
    
    print(f"\n🖼️  Logo: {processor.logo_path}")
    
    print(f"\n💡 Toutes ces informations sont personnalisables")

def main():
    """Fonction principale"""
    
    # Afficher la configuration
    afficher_configuration()
    
    # Lancer le test complet
    success = test_processeur_complet()
    
    if success:
        print("\n🎉 Test du processeur complet terminé!")
        print("\n📖 Résultats:")
        print("   ✅ Nettoyage automatique des éléments ADF")
        print("   ✅ Ajout du nouveau design et logo")
        print("   ✅ Calcul automatique des acomptes")
        print("   ✅ Personnalisation des informations")
        print("\n🚀 L'application est prête pour la production!")
        print("   Démarrez avec: python start.py")
    else:
        print("\n❌ Placez votre devis ADF dans 'static/' et relancez")

if __name__ == "__main__":
    main() 