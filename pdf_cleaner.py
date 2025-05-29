#!/usr/bin/env python3
"""
Module de nettoyage PDF pour devis ADF utilisant PyMuPDF
Basé sur le code utilisateur avec des coordonnées précises
"""

import fitz  # PyMuPDF
import os
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFCleaner:
    """Classe pour nettoyer les PDF de devis ADF avec PyMuPDF"""
    
    def __init__(self):
        """Initialise le nettoyeur PDF"""
        # Zones à masquer basées sur votre code
        self.zones_to_clean = {
            'page1_only': [
                # Logo ADF (haut droite)
                {'rect': (400, 20, 570, 120), 'description': 'Logo ADF'},
                
                # Tableau Code interne, Date actuelle, etc.
                {'rect': (300, 125, 570, 200), 'description': 'Tableau informations'},
                
                # Code Unique du Devis + ID Unique
                {'rect': (20, 170, 300, 210), 'description': 'Code Unique du Devis'},
            ],
            'all_pages': [
                # Bannière ADF en bas de chaque page
                {'rect': (20, 760, 570, 800), 'description': 'Bannière ADF bas de page'},
            ]
        }
        
        # Zones optionnelles (commentées dans votre code)
        self.optional_zones = {
            'viscogliosi_large': {'rect': (50, 50, 200, 90), 'description': 'VISCOGLIOSI (gros)'},
            'viscogliosi_small': {'rect': (50, 130, 300, 170), 'description': 'VISCOGLIOSI (petit)'},
        }

    def clean_pdf(self, input_path: str, output_path: str, include_optional: bool = False) -> bool:
        """
        Nettoie un PDF selon les zones configurées
        
        Args:
            input_path: Chemin vers le PDF d'entrée
            output_path: Chemin vers le PDF de sortie
            include_optional: Inclure les zones optionnelles (VISCOGLIOSI)
            
        Returns:
            bool: True si le nettoyage a réussi, False sinon
        """
        try:
            logger.info(f"Début du nettoyage du PDF: {input_path}")
            
            # Charger le PDF
            doc = fitz.open(input_path)
            
            # PAGE 1 : Supprimer les éléments spécifiques
            if len(doc) > 0:
                page1 = doc[0]
                
                # Appliquer les zones spécifiques à la page 1
                for zone in self.zones_to_clean['page1_only']:
                    rect = fitz.Rect(zone['rect'])
                    page1.add_redact_annot(rect, fill=(1, 1, 1))  # blanc
                    logger.info(f"Zone masquée page 1: {zone['description']}")
                
                # Zones optionnelles si demandées
                if include_optional:
                    for zone_name, zone in self.optional_zones.items():
                        rect = fitz.Rect(zone['rect'])
                        page1.add_redact_annot(rect, fill=(1, 1, 1))
                        logger.info(f"Zone optionnelle masquée: {zone['description']}")
            
            # TOUTES LES PAGES : Supprimer la bannière ADF en bas
            for page_num, page in enumerate(doc):
                for zone in self.zones_to_clean['all_pages']:
                    rect = fitz.Rect(zone['rect'])
                    page.add_redact_annot(rect, fill=(1, 1, 1))
                    logger.info(f"Zone masquée page {page_num + 1}: {zone['description']}")
                
                # Appliquer les masquages sur cette page
                page.apply_redactions()
            
            # Sauvegarder le PDF nettoyé
            doc.save(output_path)
            doc.close()
            
            logger.info(f"PDF nettoyé sauvegardé: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du nettoyage du PDF: {str(e)}")
            return False

    def get_pdf_info(self, pdf_path: str) -> dict:
        """Obtient des informations sur le PDF"""
        try:
            doc = fitz.open(pdf_path)
            
            info = {
                'num_pages': len(doc),
                'title': doc.metadata.get('title', None),
                'author': doc.metadata.get('author', None),
                'creator': doc.metadata.get('creator', None),
                'pages_info': []
            }
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                page_info = {
                    'page_number': page_num + 1,
                    'width': page.rect.width,
                    'height': page.rect.height,
                    'rotation': page.rotation
                }
                info['pages_info'].append(page_info)
            
            doc.close()
            return info
            
        except Exception as e:
            logger.error(f"Erreur lors de la lecture des informations PDF: {str(e)}")
            return {}

    def preview_zones(self, input_path: str, output_path: str) -> bool:
        """
        Crée un aperçu des zones qui seront masquées (avec des rectangles colorés)
        
        Args:
            input_path: Chemin vers le PDF d'entrée
            output_path: Chemin vers le PDF d'aperçu
            
        Returns:
            bool: True si l'aperçu a été créé, False sinon
        """
        try:
            logger.info(f"Création d'un aperçu des zones à masquer: {input_path}")
            
            doc = fitz.open(input_path)
            
            # PAGE 1 : Marquer les zones spécifiques
            if len(doc) > 0:
                page1 = doc[0]
                
                # Marquer les zones spécifiques à la page 1 en rouge
                for i, zone in enumerate(self.zones_to_clean['page1_only']):
                    rect = fitz.Rect(zone['rect'])
                    # Ajouter un rectangle rouge semi-transparent
                    page1.add_rect_annot(rect)
                    # Ajouter du texte pour identifier la zone
                    text_point = fitz.Point(rect.x0, rect.y0 - 10)
                    page1.insert_text(text_point, f"Zone {i+1}: {zone['description']}", 
                                    fontsize=8, color=(1, 0, 0))
            
            # TOUTES LES PAGES : Marquer la bannière en bas
            for page_num, page in enumerate(doc):
                for zone in self.zones_to_clean['all_pages']:
                    rect = fitz.Rect(zone['rect'])
                    page.add_rect_annot(rect)
                    text_point = fitz.Point(rect.x0, rect.y0 - 10)
                    page.insert_text(text_point, f"Bannière: {zone['description']}", 
                                   fontsize=8, color=(1, 0, 0))
            
            # Sauvegarder l'aperçu
            doc.save(output_path)
            doc.close()
            
            logger.info(f"Aperçu créé: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la création de l'aperçu: {str(e)}")
            return False

    def update_zones(self, new_zones: dict):
        """Met à jour les zones à nettoyer"""
        self.zones_to_clean.update(new_zones)

    def add_optional_zone(self, name: str, rect: tuple, description: str):
        """Ajoute une zone optionnelle"""
        self.optional_zones[name] = {
            'rect': rect,
            'description': description
        }

# Exemple d'utilisation et de test
if __name__ == "__main__":
    cleaner = PDFCleaner()
    
    # Chercher des fichiers PDF dans static
    static_dir = "static"
    if os.path.exists(static_dir):
        pdf_files = [f for f in os.listdir(static_dir) if f.lower().endswith('.pdf')]
        
        if pdf_files:
            for pdf_file in pdf_files:
                input_path = os.path.join(static_dir, pdf_file)
                
                # Créer un aperçu des zones
                preview_path = os.path.join("output", f"aperçu_{pdf_file}")
                cleaner.preview_zones(input_path, preview_path)
                
                # Nettoyer le PDF
                output_path = os.path.join("output", f"nettoyé_pymupdf_{pdf_file}")
                success = cleaner.clean_pdf(input_path, output_path)
                
                if success:
                    print(f"✅ PDF nettoyé avec PyMuPDF: {output_path}")
                    
                    # Afficher les informations
                    info = cleaner.get_pdf_info(output_path)
                    print(f"📄 Pages: {info.get('num_pages', 'N/A')}")
                else:
                    print(f"❌ Erreur lors du nettoyage de {pdf_file}")
        else:
            print("❌ Aucun fichier PDF trouvé dans static/")
            print("💡 Placez votre devis ADF dans static/ pour tester")
    else:
        print("❌ Dossier static/ non trouvé")
        print("💡 Créez le dossier static/ et placez-y votre devis ADF") 