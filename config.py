"""
Configuration pour le modificateur de PDF de devis ADF
Modifiez ces paramètres selon vos besoins
"""

from reportlab.lib.colors import Color

# Configuration des modifications à appliquer
MODIFICATIONS = {
    'remove_logo': True,           # Masquer les logos et éléments indésirables
    'change_colors': False,        # Désactivé pour le nettoyage
    'add_text': False,             # Désactivé pour le nettoyage
    'modify_existing_text': False, # Désactivé pour le nettoyage
    'change_background': False,    # Désactivé pour le nettoyage
    'add_watermark': False         # Désactivé pour le nettoyage
}

# Configuration des couleurs (pour plus tard)
COLORS = {
    'primary': Color(0.2, 0.4, 0.8, 1),      # Bleu principal
    'secondary': Color(0.1, 0.7, 0.3, 1),    # Vert secondaire
    'accent': Color(0.9, 0.3, 0.1, 1),       # Rouge-orange accent
    'text': Color(0.1, 0.1, 0.1, 1),         # Gris foncé pour le texte
    'background': Color(0.98, 0.98, 0.98, 1), # Gris très clair pour l'arrière-plan
    'watermark': Color(0.9, 0.9, 0.9, 0.3)   # Gris transparent pour le filigrane
}

# Textes à ajouter sur le PDF (désactivé pour le nettoyage)
TEXTS_TO_ADD = []

# Remplacements de texte (désactivé pour le nettoyage)
TEXT_REPLACEMENTS = {}

# Zones spécifiques à masquer pour le devis ADF
LOGO_ZONES = [
    # Logo ADF et cadre d'informations en haut à droite (première page)
    (450, 700, 200, 150),    # Zone du logo ADF et cadre rouge
    
    # Section promotionnelle en bas de chaque page
    (0, 0, 600, 120),        # Zone "NOUVEAU! VOLETS BATTANTS ADF" en bas
    
    # Zones supplémentaires si nécessaire
    (580, 750, 100, 100),    # Logo ADF seul (coin supérieur droit)
]

# Configuration du filigrane (désactivé pour le nettoyage)
WATERMARK_CONFIG = {
    'text': 'MODIFIÉ',
    'font_size': 40,
    'rotation': 45,
    'color': COLORS['watermark'],
    'font': 'Helvetica'
}

# Configuration des barres colorées (désactivé pour le nettoyage)
COLOR_BARS = []

# Configuration avancée
ADVANCED_CONFIG = {
    'preserve_original_colors': True,   # Conserver les couleurs originales pendant le nettoyage
    'add_page_numbers': False,          # Pas de numéros de page pour le nettoyage
    'compress_output': True,            # Compresser le PDF de sortie
    'remove_metadata': False,           # Garder les métadonnées pour l'instant
    'add_custom_metadata': {            # Métadonnées de nettoyage
        'title': 'Devis Nettoyé',
        'author': 'Système de Nettoyage',
        'subject': 'Devis ADF Nettoyé',
        'creator': 'PDF Cleaner v1.0'
    }
}

# Messages et textes personnalisables
MESSAGES = {
    'processing': 'Nettoyage en cours...',
    'success': 'PDF nettoyé avec succès!',
    'error': 'Erreur lors du nettoyage du PDF',
    'upload_prompt': 'Téléchargez votre devis ADF à nettoyer',
    'download_text': 'Télécharger le PDF nettoyé'
}

# Configuration de l'interface utilisateur
UI_CONFIG = {
    'theme_color': '#667eea',
    'accent_color': '#764ba2',
    'success_color': '#4CAF50',
    'error_color': '#f44336',
    'max_file_size': 10 * 1024 * 1024,  # 10 MB en octets
    'allowed_extensions': ['.pdf'],
    'auto_download': True  # Téléchargement automatique après modification
}

# Configuration de logging
LOGGING_CONFIG = {
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'pdf_modifier.log',
    'max_size': 1024 * 1024,  # 1 MB
    'backup_count': 3
} 