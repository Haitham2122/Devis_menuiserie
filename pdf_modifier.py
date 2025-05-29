import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.colors import Color, white, black, red, blue, green
from reportlab.lib.units import mm, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import io
import os
from PIL import Image
import logging

# Importer la configuration
try:
    from config import (
        MODIFICATIONS, COLORS, TEXTS_TO_ADD, TEXT_REPLACEMENTS,
        LOGO_ZONES, WATERMARK_CONFIG, COLOR_BARS, ADVANCED_CONFIG,
        LOGGING_CONFIG
    )
except ImportError:
    # Configuration par défaut si config.py n'est pas disponible
    MODIFICATIONS = {
        'remove_logo': True,
        'change_colors': True,
        'add_text': True,
        'modify_existing_text': True,
        'change_background': False,
        'add_watermark': True
    }
    COLORS = {
        'primary': Color(0.2, 0.4, 0.8, 1),
        'secondary': Color(0.1, 0.7, 0.3, 1),
        'accent': Color(0.9, 0.3, 0.1, 1),
        'text': Color(0.1, 0.1, 0.1, 1),
        'watermark': Color(0.9, 0.9, 0.9, 0.3)
    }
    TEXTS_TO_ADD = [
        {
            'text': 'DEVIS MODIFIÉ AUTOMATIQUEMENT',
            'position': (50, 750),
            'font_size': 12,
            'color': COLORS['accent'],
            'font': 'Helvetica-Bold'
        }
    ]
    TEXT_REPLACEMENTS = {
        'DEVIS': 'PROPOSITION COMMERCIALE',
        'Devis': 'Proposition'
    }
    LOGO_ZONES = [
        (0, 750, 200, 100),
        (400, 750, 200, 100)
    ]
    WATERMARK_CONFIG = {
        'text': 'MODIFIÉ',
        'font_size': 40,
        'rotation': 45,
        'color': COLORS['watermark'],
        'font': 'Helvetica'
    }
    COLOR_BARS = [
        {'position': 'top', 'color': COLORS['primary'], 'thickness': 20},
        {'position': 'bottom', 'color': COLORS['secondary'], 'thickness': 15}
    ]
    ADVANCED_CONFIG = {'add_page_numbers': True}
    LOGGING_CONFIG = {'level': 'INFO'}

# Configuration du logging
log_level = getattr(logging, LOGGING_CONFIG.get('level', 'INFO'))
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

class PDFModifier:
    """Classe pour modifier les PDF de devis automatiquement"""
    
    def __init__(self, custom_config=None):
        """
        Initialise le modificateur PDF avec la configuration
        
        Args:
            custom_config: Configuration personnalisée (optionnel)
        """
        self.modifications = MODIFICATIONS.copy()
        self.color_replacements = COLORS.copy()
        self.texts_to_add = TEXTS_TO_ADD.copy()
        self.text_replacements = TEXT_REPLACEMENTS.copy()
        self.logo_zones = LOGO_ZONES.copy()
        self.watermark_config = WATERMARK_CONFIG.copy()
        self.color_bars = COLOR_BARS.copy()
        self.advanced_config = ADVANCED_CONFIG.copy()
        
        # Appliquer la configuration personnalisée si fournie
        if custom_config:
            self._apply_custom_config(custom_config)

    def _apply_custom_config(self, custom_config):
        """Applique une configuration personnalisée"""
        if 'modifications' in custom_config:
            self.modifications.update(custom_config['modifications'])
        if 'colors' in custom_config:
            self.color_replacements.update(custom_config['colors'])
        if 'texts_to_add' in custom_config:
            self.texts_to_add = custom_config['texts_to_add']
        if 'text_replacements' in custom_config:
            self.text_replacements.update(custom_config['text_replacements'])

    def modify_pdf(self, input_path: str, output_path: str) -> bool:
        """
        Modifie un PDF selon les paramètres configurés
        
        Args:
            input_path: Chemin vers le PDF d'entrée
            output_path: Chemin vers le PDF de sortie
            
        Returns:
            bool: True si la modification a réussi, False sinon
        """
        try:
            logger.info(f"Début de la modification du PDF: {input_path}")
            
            # Lire le PDF original
            with open(input_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Créer un nouveau PDF avec les modifications
                packet = io.BytesIO()
                can = canvas.Canvas(packet, pagesize=A4)
                
                # Traiter chaque page
                for page_num in range(len(pdf_reader.pages)):
                    logger.info(f"Traitement de la page {page_num + 1}")
                    
                    # Obtenir les dimensions de la page
                    page = pdf_reader.pages[page_num]
                    page_width = float(page.mediabox.width)
                    page_height = float(page.mediabox.height)
                    
                    # Appliquer les modifications sur cette page
                    self._apply_modifications_to_page(can, page_num, page_width, page_height)
                    
                    # Nouvelle page pour la suivante (sauf pour la dernière)
                    if page_num < len(pdf_reader.pages) - 1:
                        can.showPage()
                
                can.save()
                
                # Fusionner avec le PDF original
                packet.seek(0)
                overlay_pdf = PyPDF2.PdfReader(packet)
                
                # Créer le PDF final
                pdf_writer = PyPDF2.PdfWriter()
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    
                    # Appliquer l'overlay si disponible
                    if page_num < len(overlay_pdf.pages):
                        overlay_page = overlay_pdf.pages[page_num]
                        page.merge_page(overlay_page)
                    
                    pdf_writer.add_page(page)
                
                # Ajouter des métadonnées personnalisées si configuré
                if self.advanced_config.get('add_custom_metadata'):
                    metadata = self.advanced_config['add_custom_metadata']
                    pdf_writer.add_metadata(metadata)
                
                # Sauvegarder le PDF modifié
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                
                logger.info(f"PDF modifié sauvegardé: {output_path}")
                return True
                
        except Exception as e:
            logger.error(f"Erreur lors de la modification du PDF: {str(e)}")
            return False

    def _apply_modifications_to_page(self, canvas_obj, page_num: int, page_width: float, page_height: float):
        """Applique les modifications à une page spécifique"""
        
        # 1. Masquer les logos
        if self.modifications.get('remove_logo', False):
            self._remove_logos(canvas_obj, page_width, page_height)
        
        # 2. Ajouter des éléments de couleur
        if self.modifications.get('change_colors', False):
            self._add_color_elements(canvas_obj, page_width, page_height)
        
        # 3. Ajouter du texte personnalisé
        if self.modifications.get('add_text', False):
            self._add_custom_text(canvas_obj, page_num)
        
        # 4. Ajouter un filigrane
        if self.modifications.get('add_watermark', False):
            self._add_watermark(canvas_obj, page_width, page_height)
        
        # 5. Ajouter des numéros de page
        if self.advanced_config.get('add_page_numbers', False):
            self._add_page_number(canvas_obj, page_num, page_width, page_height)

    def _remove_logos(self, canvas_obj, page_width: float, page_height: float):
        """Masque les logos en ajoutant des rectangles blancs"""
        
        canvas_obj.setFillColor(white)
        for x, y, width, height in self.logo_zones:
            # Ajuster les coordonnées si nécessaire
            adj_x = min(x, page_width - width) if x + width > page_width else x
            adj_y = min(y, page_height - height) if y + height > page_height else y
            canvas_obj.rect(adj_x, adj_y, width, height, fill=1, stroke=0)

    def _add_custom_text(self, canvas_obj, page_num: int):
        """Ajoute du texte personnalisé"""
        
        for text_config in self.texts_to_add:
            canvas_obj.setFillColor(text_config['color'])
            font = text_config.get('font', 'Helvetica-Bold')
            canvas_obj.setFont(font, text_config['font_size'])
            
            x, y = text_config['position']
            # Ajuster la position pour les pages suivantes
            if page_num > 0:
                y -= 20 * page_num
            
            canvas_obj.drawString(x, y, text_config['text'])

    def _add_color_elements(self, canvas_obj, page_width: float, page_height: float):
        """Ajoute des éléments colorés selon la configuration"""
        
        for bar_config in self.color_bars:
            position = bar_config['position']
            color = bar_config['color']
            thickness = bar_config['thickness']
            
            canvas_obj.setFillColor(color)
            
            if position == 'top':
                canvas_obj.rect(0, page_height - thickness, page_width, thickness, fill=1, stroke=0)
            elif position == 'bottom':
                canvas_obj.rect(0, 0, page_width, thickness, fill=1, stroke=0)
            elif position == 'left':
                canvas_obj.rect(0, 0, thickness, page_height, fill=1, stroke=0)
            elif position == 'right':
                canvas_obj.rect(page_width - thickness, 0, thickness, page_height, fill=1, stroke=0)

    def _add_watermark(self, canvas_obj, page_width: float, page_height: float):
        """Ajoute un filigrane selon la configuration"""
        
        canvas_obj.saveState()
        canvas_obj.translate(page_width/2, page_height/2)
        canvas_obj.rotate(self.watermark_config.get('rotation', 45))
        canvas_obj.setFillColor(self.watermark_config['color'])
        
        font = self.watermark_config.get('font', 'Helvetica')
        font_size = self.watermark_config.get('font_size', 40)
        canvas_obj.setFont(font, font_size)
        
        text = self.watermark_config.get('text', 'MODIFIÉ')
        canvas_obj.drawCentredString(0, 0, text)
        canvas_obj.restoreState()

    def _add_page_number(self, canvas_obj, page_num: int, page_width: float, page_height: float):
        """Ajoute un numéro de page"""
        
        canvas_obj.setFillColor(self.color_replacements.get('text', black))
        canvas_obj.setFont("Helvetica", 10)
        page_text = f"Page {page_num + 1}"
        canvas_obj.drawRightString(page_width - 50, 30, page_text)

    def update_modifications(self, new_modifications: dict):
        """Met à jour les paramètres de modification"""
        self.modifications.update(new_modifications)

    def update_colors(self, new_colors: dict):
        """Met à jour les couleurs utilisées"""
        self.color_replacements.update(new_colors)

    def update_texts(self, new_texts: list):
        """Met à jour les textes à ajouter"""
        self.texts_to_add = new_texts

    def update_text_replacements(self, new_replacements: dict):
        """Met à jour les remplacements de texte"""
        self.text_replacements.update(new_replacements)

    def update_logo_zones(self, new_zones: list):
        """Met à jour les zones de logos à masquer"""
        self.logo_zones = new_zones

    def get_pdf_info(self, pdf_path: str) -> dict:
        """Obtient des informations sur le PDF"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                info = {
                    'num_pages': len(pdf_reader.pages),
                    'title': pdf_reader.metadata.title if pdf_reader.metadata else None,
                    'author': pdf_reader.metadata.author if pdf_reader.metadata else None,
                    'creator': pdf_reader.metadata.creator if pdf_reader.metadata else None,
                    'pages_info': []
                }
                
                for i, page in enumerate(pdf_reader.pages):
                    page_info = {
                        'page_number': i + 1,
                        'width': float(page.mediabox.width),
                        'height': float(page.mediabox.height),
                        'rotation': page.rotation if hasattr(page, 'rotation') else 0
                    }
                    info['pages_info'].append(page_info)
                
                return info
                
        except Exception as e:
            logger.error(f"Erreur lors de la lecture des informations PDF: {str(e)}")
            return {}

    def create_sample_pdf(self, output_path: str):
        """Crée un PDF d'exemple pour tester les modifications"""
        
        try:
            can = canvas.Canvas(output_path, pagesize=A4)
            width, height = A4
            
            # Titre
            can.setFont("Helvetica-Bold", 24)
            can.drawString(100, height - 100, "DEVIS N° 2024-001")
            
            # Logo simulé (rectangle)
            can.setFillColor(blue)
            can.rect(50, height - 150, 100, 50, fill=1)
            can.setFillColor(white)
            can.setFont("Helvetica-Bold", 12)
            can.drawString(70, height - 135, "LOGO")
            
            # Informations
            can.setFillColor(black)
            can.setFont("Helvetica", 12)
            y_pos = height - 200
            
            infos = [
                "Entreprise: ABC Company",
                "Date: 28/05/2024",
                "Client: XYZ Corp",
                "",
                "Description des services:",
                "- Service 1: 1000€ HT",
                "- Service 2: 500€ HT",
                "",
                "Total HT: 1500€",
                "TVA (20%): 300€",
                "Total TTC: 1800€"
            ]
            
            for info in infos:
                can.drawString(100, y_pos, info)
                y_pos -= 20
            
            can.save()
            logger.info(f"PDF d'exemple créé: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la création du PDF d'exemple: {str(e)}")
            return False

# Exemple d'utilisation et de test
if __name__ == "__main__":
    modifier = PDFModifier()
    
    # Créer un PDF d'exemple si nécessaire
    sample_pdf = "static/sample_devis.pdf"
    if not os.path.exists(sample_pdf):
        os.makedirs("static", exist_ok=True)
        print("Création d'un PDF d'exemple...")
        modifier.create_sample_pdf(sample_pdf)
    
    # Test avec le fichier exemple
    test_input = sample_pdf
    test_output = "output/test_modified.pdf"
    
    os.makedirs("output", exist_ok=True)
    
    if os.path.exists(test_input):
        print("Test de modification PDF...")
        success = modifier.modify_pdf(test_input, test_output)
        if success:
            print(f"✅ Test réussi! Fichier modifié: {test_output}")
            
            # Afficher les informations du PDF
            info = modifier.get_pdf_info(test_output)
            print(f"📄 Informations du PDF modifié:")
            print(f"   - Nombre de pages: {info.get('num_pages', 'N/A')}")
            print(f"   - Titre: {info.get('title', 'N/A')}")
        else:
            print("❌ Échec du test")
    else:
        print(f"Fichier de test non trouvé: {test_input}")
        print("Un PDF d'exemple devrait être créé automatiquement") 