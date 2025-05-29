#!/usr/bin/env python3
"""
Script de démonstration pour le Modificateur de Devis PDF
"""

import os
import time
from pdf_modifier import PDFModifier
from config import MODIFICATIONS, COLORS, TEXTS_TO_ADD

def demo_pdf_modifications():
    """Démonstration des différentes modifications possibles"""
    
    print("🎬 Démonstration du Modificateur de Devis PDF")
    print("=" * 50)
    
    # Créer le modificateur
    modifier = PDFModifier()
    
    # Créer les répertoires nécessaires
    os.makedirs("static", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    # 1. Créer un PDF d'exemple
    sample_pdf = "static/demo_devis.pdf"
    print("📄 Création d'un PDF d'exemple...")
    if modifier.create_sample_pdf(sample_pdf):
        print(f"✅ PDF d'exemple créé: {sample_pdf}")
    else:
        print("❌ Erreur lors de la création du PDF d'exemple")
        return
    
    # 2. Démonstration des différentes configurations
    demos = [
        {
            'name': 'Modification Standard',
            'output': 'output/demo_standard.pdf',
            'config': None  # Configuration par défaut
        },
        {
            'name': 'Suppression de logos uniquement',
            'output': 'output/demo_logos_only.pdf',
            'config': {
                'modifications': {
                    'remove_logo': True,
                    'change_colors': False,
                    'add_text': False,
                    'add_watermark': False
                }
            }
        },
        {
            'name': 'Couleurs personnalisées',
            'output': 'output/demo_colors.pdf',
            'config': {
                'modifications': {
                    'remove_logo': False,
                    'change_colors': True,
                    'add_text': False,
                    'add_watermark': False
                },
                'colors': {
                    'primary': COLORS['accent'],  # Rouge-orange
                    'secondary': COLORS['primary'],  # Bleu
                }
            }
        },
        {
            'name': 'Texte personnalisé',
            'output': 'output/demo_text.pdf',
            'config': {
                'modifications': {
                    'remove_logo': False,
                    'change_colors': False,
                    'add_text': True,
                    'add_watermark': False
                },
                'texts_to_add': [
                    {
                        'text': 'DEVIS PERSONNALISÉ',
                        'position': (100, 700),
                        'font_size': 16,
                        'color': COLORS['accent'],
                        'font': 'Helvetica-Bold'
                    },
                    {
                        'text': 'Offre spéciale - Remise 10%',
                        'position': (100, 680),
                        'font_size': 12,
                        'color': COLORS['secondary'],
                        'font': 'Helvetica-Oblique'
                    }
                ]
            }
        },
        {
            'name': 'Modification complète',
            'output': 'output/demo_complete.pdf',
            'config': {
                'modifications': {
                    'remove_logo': True,
                    'change_colors': True,
                    'add_text': True,
                    'add_watermark': True
                }
            }
        }
    ]
    
    print(f"\n🔧 Démonstration de {len(demos)} configurations différentes:")
    print("-" * 50)
    
    for i, demo in enumerate(demos, 1):
        print(f"\n{i}. {demo['name']}")
        
        # Créer un nouveau modificateur avec la configuration spécifique
        demo_modifier = PDFModifier(demo['config'])
        
        # Appliquer les modifications
        success = demo_modifier.modify_pdf(sample_pdf, demo['output'])
        
        if success:
            print(f"   ✅ Créé: {demo['output']}")
            
            # Afficher les informations du PDF
            info = demo_modifier.get_pdf_info(demo['output'])
            print(f"   📊 Pages: {info.get('num_pages', 'N/A')}")
        else:
            print(f"   ❌ Erreur lors de la création de {demo['output']}")
    
    print(f"\n📁 Tous les fichiers de démonstration sont dans le dossier 'output/'")
    print("🌐 Vous pouvez maintenant démarrer l'application web avec: python start.py")

def show_configuration():
    """Affiche la configuration actuelle"""
    
    print("\n⚙️  Configuration actuelle:")
    print("-" * 30)
    
    print("🔧 Modifications activées:")
    for key, value in MODIFICATIONS.items():
        status = "✅" if value else "❌"
        print(f"   {status} {key}")
    
    print(f"\n🎨 Couleurs configurées: {len(COLORS)} couleurs")
    print(f"📝 Textes à ajouter: {len(TEXTS_TO_ADD)} textes")
    
    print("\n💡 Pour personnaliser, modifiez le fichier 'config.py'")

def main():
    """Fonction principale de démonstration"""
    
    # Afficher la configuration
    show_configuration()
    
    # Lancer la démonstration
    demo_pdf_modifications()
    
    print("\n" + "=" * 50)
    print("🎉 Démonstration terminée!")
    print("\n📖 Prochaines étapes:")
    print("   1. Examinez les fichiers PDF créés dans 'output/'")
    print("   2. Modifiez 'config.py' selon vos besoins")
    print("   3. Démarrez l'application: python start.py")
    print("   4. Testez avec vos propres PDF!")

if __name__ == "__main__":
    main() 