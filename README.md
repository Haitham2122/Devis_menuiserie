# 🔧 Processeur de Devis ADF - Menuiserie

Application web FastAPI pour transformer automatiquement les devis ADF en documents personnalisés avec votre identité visuelle.

## 🎯 Fonctionnalités

- **🧹 Nettoyage automatique** : Suppression des éléments ADF indésirables (logo, bannières, etc.)
- **🎨 Design personnalisé** : Application de votre logo et charte graphique
- **📊 Calculs automatiques** : Calcul des acomptes (30%, 50%, 20%) basé sur le montant total
- **⚡ Interface moderne** : Design minimaliste et professionnel
- **📱 Responsive** : Compatible desktop et mobile

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Installation des dépendances
```bash
pip install -r requirements.txt
```

### Démarrage de l'application
```bash
python main.py
```

L'application sera accessible sur : http://localhost:8000

## 📁 Structure du projet

```
├── main.py                    # Application FastAPI principale
├── pdf_processor_complete.py  # Module de traitement PDF complet
├── create_sample_logo.py      # Générateur de logo d'exemple
├── test_complet.py           # Tests complets
├── requirements.txt          # Dépendances Python
├── static/                   # Fichiers PDF d'entrée
├── output/                   # Fichiers PDF traités (temporaire)
└── uploads/                  # Fichiers temporaires (temporaire)
```

## 🔧 Utilisation

1. **Démarrer l'application** : `python main.py`
2. **Ouvrir le navigateur** : http://localhost:8000
3. **Sélectionner un PDF** : Glisser-déposer ou cliquer pour choisir
4. **Traiter le document** : Cliquer sur "Traiter le document"
5. **Télécharger** : Le fichier traité se télécharge automatiquement

## ⚙️ Configuration

### Personnalisation de l'entreprise
Modifiez les informations dans `pdf_processor_complete.py` :

```python
self.company_info = {
    'name': "Votre Entreprise",
    'address1': "Votre Adresse",
    'address2': "Code Postal Ville",
    'phone': "Tél. : XX XX XX XX XX",
    'email': "E-mail : contact@votre-entreprise.com"
}
```

### Logo personnalisé
Remplacez le fichier `logo.png` par votre logo (format PNG recommandé).

### Couleurs
Personnalisez les couleurs dans la section `colors` :

```python
self.colors = {
    'background_gray': (238/255, 238/255, 238/255),
    'accent_blue': (90/255, 177/255, 235/255),
    'text_black': (0, 0, 0),
    'white': (1, 1, 1)
}
```

## 🧪 Tests

### Test complet
```bash
python test_complet.py
```

### Test de téléchargement
```bash
python test_download.py
```

## 📋 Dépendances principales

- **FastAPI** : Framework web moderne
- **PyMuPDF (fitz)** : Manipulation de PDF
- **Pillow** : Traitement d'images
- **Uvicorn** : Serveur ASGI

## 🔄 Processus de traitement

1. **Upload** : Réception du PDF ADF
2. **Nettoyage** : Suppression des éléments indésirables
3. **Design** : Application du nouveau design
4. **Calculs** : Traitement automatique des acomptes
5. **Export** : Génération du PDF final

## 🎨 Personnalisation avancée

### Zones de nettoyage
Modifiez les coordonnées dans `_clean_pdf()` pour ajuster les zones à supprimer.

### Mise en page
Personnalisez la mise en page dans les méthodes `_add_*()` du processeur.

## 🐛 Dépannage

### Problèmes courants

- **Logo non affiché** : Vérifiez que `logo.png` existe
- **Calculs incorrects** : Vérifiez la détection de "ACOMPTE 30%" dans le PDF
- **Erreur de traitement** : Consultez les logs dans la console

### Logs
L'application affiche des logs détaillés pour diagnostiquer les problèmes.

## 📄 Licence

Ce projet est sous licence MIT.

## 👨‍💻 Auteur

Développé pour automatiser le traitement des devis ADF en menuiserie.

## 🔗 Liens utiles

- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [Repository GitHub](https://github.com/Haitham2122/Devis_menuiserie.git) 