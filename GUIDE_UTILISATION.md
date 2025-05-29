# 🚀 Guide d'Utilisation Rapide - Modificateur de Devis PDF

## ⚡ Démarrage Rapide

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Démarrage de l'application
```bash
python start.py
```

### 3. Utilisation
- Ouvrez votre navigateur à `http://localhost:8000`
- Téléchargez votre devis PDF
- Cliquez sur "Modifier le PDF"
- Téléchargez le résultat

## 🎯 Modifications Automatiques

L'application applique automatiquement :

✅ **Suppression des logos** - Masque les logos dans les coins  
✅ **Ajout de couleurs** - Barres colorées en haut, bas et côté  
✅ **Texte personnalisé** - "DEVIS MODIFIÉ AUTOMATIQUEMENT"  
✅ **Filigrane** - "MODIFIÉ" en diagonal  
✅ **Numéros de page** - Si activé dans la config  

## ⚙️ Personnalisation

### Modifier les couleurs
Éditez `config.py` :
```python
COLORS = {
    'primary': Color(0.2, 0.4, 0.8, 1),    # Bleu
    'secondary': Color(0.1, 0.7, 0.3, 1),  # Vert
    'accent': Color(0.9, 0.3, 0.1, 1),     # Rouge-orange
}
```

### Modifier les textes
```python
TEXTS_TO_ADD = [
    {
        'text': 'VOTRE TEXTE ICI',
        'position': (50, 750),
        'font_size': 12,
        'color': COLORS['accent']
    }
]
```

### Activer/Désactiver les modifications
```python
MODIFICATIONS = {
    'remove_logo': True,     # Masquer logos
    'change_colors': True,   # Ajouter couleurs
    'add_text': True,        # Ajouter texte
    'add_watermark': True    # Ajouter filigrane
}
```

## 🧪 Test et Démonstration

### Voir des exemples
```bash
python demo.py
```
Crée 5 PDF d'exemple avec différentes configurations dans `output/`

### Tester l'API
```bash
python test_api.py
```
Teste que l'application fonctionne correctement

## 📁 Structure des Fichiers

```
v2/
├── main.py              # Application FastAPI
├── pdf_modifier.py      # Logique de modification
├── config.py           # Configuration
├── start.py            # Script de démarrage
├── demo.py             # Démonstration
├── static/             # Fichiers de test
├── uploads/            # Temporaire (auto-nettoyé)
└── output/             # PDF modifiés
```

## 🔧 Commandes Utiles

| Commande | Description |
|----------|-------------|
| `python start.py` | Démarrer l'application |
| `python demo.py` | Voir des exemples |
| `python test_api.py` | Tester l'API |
| `python pdf_modifier.py` | Test du module PDF |

## 🎨 Exemples de Personnalisation

### Devis Commercial
```python
TEXTS_TO_ADD = [
    {
        'text': 'PROPOSITION COMMERCIALE',
        'position': (50, 750),
        'font_size': 14,
        'color': COLORS['primary']
    }
]
```

### Devis Confidentiel
```python
WATERMARK_CONFIG = {
    'text': 'CONFIDENTIEL',
    'font_size': 50,
    'rotation': 45,
    'color': Color(1, 0, 0, 0.3)  # Rouge transparent
}
```

### Masquer logos spécifiques
```python
LOGO_ZONES = [
    (0, 750, 200, 100),      # Coin supérieur gauche
    (400, 750, 200, 100),    # Coin supérieur droit
    (250, 400, 100, 50),     # Zone centrale
]
```

## 🚨 Dépannage

### Erreur "Module not found"
```bash
pip install -r requirements.txt
```

### Erreur "Port already in use"
Changez le port dans `main.py` :
```python
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### PDF corrompu
Vérifiez que votre PDF d'entrée n'est pas protégé par mot de passe

## 📞 Support

1. Vérifiez ce guide
2. Testez avec `python demo.py`
3. Consultez les logs dans la console
4. Vérifiez `config.py` pour la personnalisation

---

🎉 **Votre application est prête !** Placez votre PDF de test dans `static/` et commencez à modifier vos devis automatiquement. 