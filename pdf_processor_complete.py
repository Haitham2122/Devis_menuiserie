#!/usr/bin/env python3
"""
Module complet de traitement PDF pour devis ADF
Basé sur le code final de l'utilisateur : nettoyage + design + calculs automatiques
"""

import fitz  # PyMuPDF
import re
import os
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFProcessorComplete:
    """Classe complète pour traiter les PDF de devis ADF"""
    
    def __init__(self, logo_path="logo.png"):
        """
        Initialise le processeur PDF complet
        
        Args:
            logo_path: Chemin vers le fichier logo à insérer
        """
        self.logo_path = logo_path
        
        # Configuration des couleurs
        self.colors = {
            'background_gray': (238/255, 238/255, 238/255),
            'accent_blue': (90/255, 177/255, 235/255),
            'text_black': (0, 0, 0),
            'white': (1, 1, 1)
        }
        
        # Configuration des textes d'entreprise
        self.company_info = {
            'name': "Fenêtre sur le monde",
            'address1': "885 BOULEVARD DES PRINCES",
            'address2': "06210 MANDELIEU-LA-NAPOULE",
            'phone': "Tél. : 06 51 17 39 39",
            'email': "E-mail : FENETRE_SUR_LE_MONDE@gmail.com"
        }
        
        # Configuration du client (par défaut)
        self.client_info = {
            'name': "Nom prénom",
            'address1': "885 BOULEVARD DES PRINCES",
            'address2': "06210 MANDELIEU-LA-NAPOULE"
        }
        
        # Configuration du footer
        self.footer_info = {
            'siret': "SIRET : 94366500000015",
            'address': "Adresse : 885 BOULEVARD DES PRINCES, 06210 MANDELIEU-LA-NAPOULE",
            'phone': "Téléphone : +33677887744"
        }

    def process_pdf(self, input_path: str, output_path: str, client_info: dict = None) -> bool:
        """
        Traite complètement un PDF : nettoyage + design + calculs
        
        Args:
            input_path: Chemin vers le PDF d'entrée
            output_path: Chemin vers le PDF de sortie
            client_info: Informations client personnalisées (optionnel)
            
        Returns:
            bool: True si le traitement a réussi, False sinon
        """
        try:
            logger.info(f"Début du traitement complet du PDF: {input_path}")
            
            # Charger le PDF
            doc = fitz.open(input_path)
            page1 = doc[0]
            
            # 1. NETTOYAGE - Supprimer les éléments indésirables
            self._clean_pdf(doc, page1)
            
            # 2. DESIGN - Ajouter le nouveau design
            self._add_design(doc, page1, client_info)
            
            # 3. CALCULS - Traiter les acomptes automatiquement
            self._process_payments(doc)
            
            # Sauvegarder le PDF traité
            doc.save(output_path)
            doc.close()
            
            logger.info(f"PDF traité sauvegardé: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement du PDF: {str(e)}")
            return False

    def _clean_pdf(self, doc, page1):
        """Phase 1: Nettoyage des éléments indésirables"""
        logger.info("Phase 1: Nettoyage en cours...")
        
        # Nettoyage en-tête et zones spécifiques page 1
        page1.add_redact_annot(fitz.Rect(30, 20, 570, 120), fill=self.colors['white'])
        page1.add_redact_annot(fitz.Rect(30, 125, 570, 200), fill=self.colors['white'])
        page1.add_redact_annot(fitz.Rect(20, 170, 300, 210), fill=self.colors['white'])
        
        # Nettoyage pied de page sur toutes les pages
        for page in doc:
            page.add_redact_annot(fitz.Rect(20, 760, 570, 800), fill=self.colors['white'])
            page.apply_redactions()

    def _add_design(self, doc, page1, client_info=None):
        """Phase 2: Ajout du nouveau design"""
        logger.info("Phase 2: Ajout du design...")
        
        # Utiliser les infos client fournies ou par défaut
        client = client_info if client_info else self.client_info
        
        # 1. LOGO
        self._add_logo(page1)
        
        # 2. INFORMATIONS ENTREPRISE
        self._add_company_info(page1)
        
        # 3. INFORMATIONS CLIENT
        self._add_client_info(page1, client)
        
        # 4. BLOC DEVIS (droite)
        self._add_quote_block(page1)
        
        # 5. LIGNE DE SÉPARATION
        self._add_separator_line(page1)
        
        # 6. FOOTER SUR TOUTES LES PAGES
        self._add_footer_all_pages(doc)

    def _add_logo(self, page1):
        """Ajouter le logo"""
        if os.path.exists(self.logo_path):
            logo_rect = fitz.Rect(30, 20, 130, 100)
            page1.insert_image(logo_rect, filename=self.logo_path)
            logger.info(f"Logo ajouté: {self.logo_path}")
        else:
            logger.warning(f"Logo non trouvé: {self.logo_path}")

    def _add_company_info(self, page1):
        """Ajouter les informations de l'entreprise"""
        # Zone de fond grise
        rect_zone_2 = fitz.Rect(30, 120, 570, 190)
        page1.draw_rect(rect_zone_2, fill=self.colors['background_gray'], color=None)
        
        # Textes entreprise
        page1.insert_text((32, 110), self.company_info['name'], 
                         fontsize=14, fontname="Helvetica-Bold", color=self.colors['text_black'])
        page1.insert_text((32, 135), self.company_info['address1'], 
                         fontsize=10, fontname="Helvetica-Bold")
        page1.insert_text((32, 150), self.company_info['address2'], 
                         fontsize=10, fontname="Helvetica-Bold")
        page1.insert_text((32, 165), self.company_info['phone'], 
                         fontsize=10, fontname="Helvetica-Bold")
        page1.insert_text((32, 180), self.company_info['email'], 
                         fontsize=10, fontname="Helvetica-Bold")

    def _add_client_info(self, page1, client_info):
        """Ajouter les informations client"""
        page1.insert_text((400, 135), client_info['name'], 
                         fontsize=10, fontname="Helvetica-Bold")
        page1.insert_text((400, 150), client_info['address1'], 
                         fontsize=10, fontname="Helvetica-Bold")
        page1.insert_text((400, 165), client_info['address2'], 
                         fontsize=10, fontname="Helvetica-Bold")

    def _add_quote_block(self, page1):
        """Ajouter le bloc devis à droite"""
        # Zone de fond grise
        rect_zone = fitz.Rect(400, 30, 570, 85)
        page1.draw_rect(rect_zone, fill=self.colors['background_gray'], color=None)
        
        # Ligne bleue
        rect_zone_1 = fitz.Rect(400, 87, 570, 88)
        page1.draw_rect(rect_zone_1, fill=self.colors['accent_blue'], color=None)
        
        # Textes du bloc devis
        page1.insert_text((415, 45), "Date :", 
                         fontsize=10, fontname="Helvetica-Bold", color=self.colors['text_black'])
        page1.insert_text((415, 60), "DEVIS N° :", 
                         fontsize=10, fontname="Helvetica-Bold", color=self.colors['text_black'])
        page1.insert_text((415, 75), "Code Client :", 
                         fontsize=10, fontname="Helvetica-Bold", color=self.colors['text_black'])

    def _add_separator_line(self, page1):
        """Ajouter la ligne de séparation"""
        ligne_zone = fitz.Rect(30, 193, 570, 194)
        page1.draw_rect(ligne_zone, fill=self.colors['accent_blue'], color=None)

    def _add_footer_all_pages(self, doc):
        """Ajouter le footer sur toutes les pages"""
        for page in doc:
            # Zone de fond grise pour le footer
            ligne_zone = fitz.Rect(30, 760, 570, 800)
            page.draw_rect(ligne_zone, fill=self.colors['background_gray'], color=None)
            
            # Textes du footer
            page.insert_text((38, 785), self.footer_info['siret'], 
                           fontsize=8, fontname="Helvetica", color=self.colors['text_black'])
            page.insert_text((140, 785), self.footer_info['address'], 
                           fontsize=8, fontname="Helvetica", color=self.colors['text_black'])
            page.insert_text((460, 785), self.footer_info['phone'], 
                           fontsize=8, fontname="Helvetica", color=self.colors['text_black'])
            
            # Ligne bleue en bas
            ligne_zone_1 = fitz.Rect(30, 802, 570, 803)
            page.draw_rect(ligne_zone_1, fill=self.colors['accent_blue'], color=None)

    def _process_payments(self, doc):
        """Phase 3: Traitement automatique des acomptes"""
        logger.info("Phase 3: Calcul des acomptes...")
        
        try:
            last_page = doc[-1]
            texte = last_page.get_text()
            lines = texte.splitlines()
            
            # Chercher la ligne "ACOMPTE 30%" puis regarder la valeur juste avant
            i = lines.index('ACOMPTE 30%')
            montant_str = lines[i - 1]  # Juste avant
            montant_str = montant_str.replace("\u202f", "").replace(" ", "").replace(",", ".").replace("EUR", "").strip()
            total_ttc = float(montant_str)
            
            # Calculer les acomptes
            acompte_30 = round(total_ttc * 0.30, 2)
            acompte_50 = round(total_ttc * 0.50, 2)
            solde_20 = round(total_ttc * 0.20, 2)
            
            # Insérer les montants calculés
            last_page.insert_text((110, 463), f": {acompte_30:.2f}  EUR", 
                                 fontsize=10, fontname="Helvetica")
            last_page.insert_text((251, 463 + 10), f"{acompte_50:.2f}  EUR", 
                                 fontsize=10, fontname="Helvetica")
            last_page.insert_text((190, 463 + 21), f" {solde_20:.2f} EUR", 
                                 fontsize=10, fontname="Helvetica")
            
            logger.info(f"✅ Total TTC détecté: {total_ttc:.2f} €")
            logger.info(f"   Acompte 30%: {acompte_30:.2f} €")
            logger.info(f"   Acompte 50%: {acompte_50:.2f} €")
            logger.info(f"   Solde 20%: {solde_20:.2f} €")
            
        except (ValueError, IndexError) as e:
            logger.warning(f"❌ Impossible de détecter le montant avant 'ACOMPTE 30%': {e}")

    def update_company_info(self, new_info: dict):
        """Met à jour les informations de l'entreprise"""
        self.company_info.update(new_info)

    def update_footer_info(self, new_info: dict):
        """Met à jour les informations du footer"""
        self.footer_info.update(new_info)

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

# Exemple d'utilisation et de test
if __name__ == "__main__":
    processor = PDFProcessorComplete()
    
    # Chercher des fichiers PDF dans static
    static_dir = "static"
    if os.path.exists(static_dir):
        pdf_files = [f for f in os.listdir(static_dir) if f.lower().endswith('.pdf')]
        
        if pdf_files:
            for pdf_file in pdf_files:
                input_path = os.path.join(static_dir, pdf_file)
                output_path = os.path.join("output", f"traité_complet_{pdf_file}")
                
                # Informations client personnalisées (optionnel)
                client_custom = {
                    'name': "M. HAITEM",
                    'address1': "123 Rue de la Paix",
                    'address2': "06000 NICE"
                }
                
                # Traiter le PDF
                success = processor.process_pdf(input_path, output_path, client_custom)
                
                if success:
                    print(f"✅ PDF traité complètement: {output_path}")
                    
                    # Afficher les informations
                    info = processor.get_pdf_info(output_path)
                    print(f"📄 Pages: {info.get('num_pages', 'N/A')}")
                else:
                    print(f"❌ Erreur lors du traitement de {pdf_file}")
        else:
            print("❌ Aucun fichier PDF trouvé dans static/")
            print("💡 Placez votre devis ADF dans static/ pour tester")
    else:
        print("❌ Dossier static/ non trouvé")
        print("💡 Créez le dossier static/ et placez-y votre devis ADF") 