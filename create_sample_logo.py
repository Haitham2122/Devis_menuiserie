#!/usr/bin/env python3
"""
Script pour créer un logo d'exemple
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_logo(output_path="logo.png", width=200, height=100):
    """
    Crée un logo d'exemple simple
    
    Args:
        output_path: Chemin de sortie du logo
        width: Largeur du logo
        height: Hauteur du logo
    """
    
    # Créer une image avec fond bleu
    img = Image.new('RGB', (width, height), color=(90, 177, 235))
    draw = ImageDraw.Draw(img)
    
    # Ajouter un cercle blanc
    circle_size = min(width, height) // 3
    circle_x = width // 2 - circle_size // 2
    circle_y = height // 2 - circle_size // 2
    draw.ellipse([circle_x, circle_y, circle_x + circle_size, circle_y + circle_size], 
                 fill=(255, 255, 255))
    
    # Ajouter du texte
    try:
        # Essayer d'utiliser une police système
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        # Utiliser la police par défaut si arial n'est pas disponible
        font = ImageFont.load_default()
    
    text = "LOGO"
    
    # Calculer la position du texte pour le centrer
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    
    # Dessiner le texte en noir
    draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)
    
    # Sauvegarder l'image
    img.save(output_path)
    print(f"✅ Logo d'exemple créé: {output_path}")

if __name__ == "__main__":
    create_sample_logo() 