from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
import os
import shutil
from pathlib import Path
import uuid
from pdf_processor_complete import PDFProcessorComplete  # Nouveau module complet

app = FastAPI(title="PDF Devis Modifier", description="Application pour modifier automatiquement les devis PDF")

# Créer les répertoires s'ils n'existent pas
os.makedirs("uploads", exist_ok=True)
os.makedirs("output", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Monter les répertoires statiques seulement s'ils existent
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")
if os.path.exists("output"):
    app.mount("/output", StaticFiles(directory="output"), name="output")

def cleanup_old_files():
    """Nettoie les anciens fichiers temporaires"""
    import time
    current_time = time.time()
    
    # Nettoyer les fichiers de plus de 1 heure dans uploads et output
    for directory in ["uploads", "output"]:
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                if filename.startswith(("modified_", "temp_")) or "_" in filename:
                    file_path = os.path.join(directory, filename)
                    try:
                        # Supprimer les fichiers de plus d'1 heure
                        if os.path.isfile(file_path) and (current_time - os.path.getmtime(file_path)) > 3600:
                            os.remove(file_path)
                            print(f"Fichier temporaire supprimé: {filename}")
                    except Exception as e:
                        print(f"Erreur lors de la suppression de {filename}: {e}")

# Nettoyer les anciens fichiers au démarrage
cleanup_old_files()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Page d'accueil avec interface de téléchargement"""
    html_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Processeur de Devis ADF</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: #f8fafc;
                color: #334155;
                line-height: 1.6;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                max-width: 600px;
                width: 100%;
                padding: 40px;
                border: 1px solid #e2e8f0;
            }
            
            .header {
                text-align: center;
                margin-bottom: 40px;
            }
            
            .header h1 {
                font-size: 28px;
                font-weight: 700;
                color: #1e293b;
                margin-bottom: 8px;
                letter-spacing: -0.025em;
            }
            
            .header p {
                color: #64748b;
                font-size: 16px;
                font-weight: 400;
            }
            
            .upload-section {
                margin-bottom: 32px;
            }
            
            .upload-area {
                border: 2px dashed #cbd5e1;
                border-radius: 8px;
                padding: 32px;
                text-align: center;
                transition: all 0.2s ease;
                background: #f8fafc;
                position: relative;
            }
            
            .upload-area:hover {
                border-color: #3b82f6;
                background: #f1f5f9;
            }
            
            .upload-area.dragover {
                border-color: #3b82f6;
                background: #eff6ff;
            }
            
            .upload-icon {
                width: 48px;
                height: 48px;
                margin: 0 auto 16px;
                background: #e2e8f0;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
                color: #64748b;
            }
            
            .upload-text {
                margin-bottom: 16px;
            }
            
            .upload-text h3 {
                font-size: 18px;
                font-weight: 600;
                color: #1e293b;
                margin-bottom: 4px;
            }
            
            .upload-text p {
                color: #64748b;
                font-size: 14px;
            }
            
            input[type="file"] {
                display: none;
            }
            
            .file-input-label {
                display: inline-block;
                background: #3b82f6;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 500;
                font-size: 14px;
                transition: background 0.2s ease;
                border: none;
            }
            
            .file-input-label:hover {
                background: #2563eb;
            }
            
            .selected-file {
                margin-top: 16px;
                padding: 12px;
                background: #f0f9ff;
                border: 1px solid #bae6fd;
                border-radius: 6px;
                color: #0369a1;
                font-size: 14px;
                display: none;
            }
            
            .process-button {
                width: 100%;
                background: #059669;
                color: white;
                border: none;
                padding: 14px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
                margin-top: 24px;
                opacity: 0.5;
                pointer-events: none;
            }
            
            .process-button:enabled {
                opacity: 1;
                pointer-events: auto;
            }
            
            .process-button:enabled:hover {
                background: #047857;
                transform: translateY(-1px);
            }
            
            .result {
                margin-top: 24px;
                padding: 16px;
                border-radius: 8px;
                display: none;
                font-size: 14px;
            }
            
            .result.success {
                background: #f0fdf4;
                border: 1px solid #bbf7d0;
                color: #166534;
            }
            
            .result.error {
                background: #fef2f2;
                border: 1px solid #fecaca;
                color: #dc2626;
            }
            
            .download-link {
                display: inline-block;
                margin-top: 12px;
                padding: 8px 16px;
                background: #3b82f6;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
                transition: background 0.2s ease;
            }
            
            .download-link:hover {
                background: #2563eb;
            }
            
            .loading {
                display: none;
                text-align: center;
                padding: 20px;
            }
            
            .spinner {
                width: 32px;
                height: 32px;
                border: 3px solid #e2e8f0;
                border-top: 3px solid #3b82f6;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 0 auto 12px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            @media (max-width: 640px) {
                .container {
                    padding: 24px;
                    margin: 16px;
                }
                
                .header h1 {
                    font-size: 24px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Processeur de Devis ADF</h1>
                <p>Transformation automatique de vos devis en quelques secondes</p>
            </div>
            
            <div class="upload-section">
                <form id="uploadForm" enctype="multipart/form-data">
                    <div class="upload-area">
                        <div class="upload-icon">📄</div>
                        <div class="upload-text">
                            <h3>Sélectionner un devis PDF</h3>
                            <p>Glissez-déposez votre fichier ici ou cliquez pour parcourir</p>
                        </div>
                        <label for="pdfFile" class="file-input-label">Choisir un fichier</label>
                        <input type="file" id="pdfFile" name="file" accept=".pdf" required>
                    </div>
                    <div id="selectedFile" class="selected-file"></div>
                    <button type="submit" id="processButton" class="process-button" disabled>
                        Traiter le document
                    </button>
                </form>
            </div>
            
            <div id="loading" class="loading">
                <div class="spinner"></div>
                <p>Traitement en cours...</p>
            </div>
            
            <div id="result" class="result"></div>
        </div>

        <script>
            const uploadArea = document.querySelector('.upload-area');
            const fileInput = document.getElementById('pdfFile');
            const selectedFileDiv = document.getElementById('selectedFile');
            const processButton = document.getElementById('processButton');
            const form = document.getElementById('uploadForm');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');

            let isProcessing = false; // Protection contre les soumissions multiples

            // Gestion du drag & drop
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });

            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragover');
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                
                const files = e.dataTransfer.files;
                if (files.length > 0 && files[0].type === 'application/pdf') {
                    fileInput.files = files;
                    handleFileSelect();
                }
            });

            // Gestion de la sélection de fichier
            fileInput.addEventListener('change', handleFileSelect);

            function handleFileSelect() {
                const file = fileInput.files[0];
                if (file) {
                    selectedFileDiv.textContent = `Fichier sélectionné: ${file.name}`;
                    selectedFileDiv.style.display = 'block';
                    processButton.disabled = false;
                } else {
                    selectedFileDiv.style.display = 'none';
                    processButton.disabled = true;
                }
            }

            // Gestion du formulaire
            form.addEventListener('submit', async function(e) {
                e.preventDefault();
                
                // Protection contre les soumissions multiples
                if (isProcessing) {
                    console.log('Traitement déjà en cours, ignoré');
                    return;
                }
                
                const file = fileInput.files[0];
                if (!file) {
                    showResult('Veuillez sélectionner un fichier PDF', 'error');
                    return;
                }
                
                isProcessing = true;
                const formData = new FormData();
                formData.append('file', file);
                
                // Afficher le loading
                loading.style.display = 'block';
                result.style.display = 'none';
                processButton.disabled = true;
                
                try {
                    const response = await fetch('/upload-pdf/', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (response.ok) {
                        // Le serveur retourne directement le fichier PDF
                        const blob = await response.blob();
                        
                        // Créer un nom de fichier propre
                        const cleanFilename = file.name.replace('.pdf', '_traité.pdf');
                        
                        // Méthode plus robuste pour le téléchargement
                        if (window.navigator && window.navigator.msSaveOrOpenBlob) {
                            // Pour Internet Explorer
                            window.navigator.msSaveOrOpenBlob(blob, cleanFilename);
                        } else {
                            // Pour les autres navigateurs
                            const url = window.URL.createObjectURL(blob);
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = cleanFilename;
                            a.style.display = 'none';
                            
                            // Ajouter au DOM, cliquer, puis supprimer
                            document.body.appendChild(a);
                            
                            // Forcer le téléchargement avec un délai
                            setTimeout(() => {
                                a.click();
                                
                                // Nettoyer après un délai
                                setTimeout(() => {
                                    document.body.removeChild(a);
                                    window.URL.revokeObjectURL(url);
                                }, 100);
                            }, 100);
                        }
                        
                        showResult('✅ Document traité et téléchargé avec succès !', 'success');
                        
                        // Réinitialiser le formulaire après succès
                        fileInput.value = '';
                        selectedFileDiv.style.display = 'none';
                        processButton.disabled = true;
                    } else {
                        const errorData = await response.json();
                        showResult(`❌ Erreur: ${errorData.detail}`, 'error');
                    }
                } catch (error) {
                    showResult(`❌ Erreur de connexion: ${error.message}`, 'error');
                } finally {
                    loading.style.display = 'none';
                    processButton.disabled = false;
                    isProcessing = false; // Réinitialiser la protection
                }
            });
            
            function showResult(message, type) {
                result.innerHTML = message;
                result.className = `result ${type}`;
                result.style.display = 'block';
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """Endpoint pour télécharger et modifier un PDF"""
    
    print(f"🔧 Début du traitement: {file.filename}")
    
    # Vérifier que c'est un fichier PDF
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Le fichier doit être un PDF")
    
    # Générer un nom unique pour le fichier
    file_id = str(uuid.uuid4())
    input_filename = f"{file_id}_{file.filename}"
    output_filename = f"temp_{file_id}.pdf"  # Nom temporaire plus simple
    
    input_path = os.path.join("uploads", input_filename)
    output_path = os.path.join("output", output_filename)
    
    print(f"📁 Fichiers: {input_path} -> {output_path}")
    
    try:
        # Sauvegarder le fichier téléchargé
        with open(input_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        print(f"💾 Fichier sauvegardé: {len(content)} bytes")
        
        # Modifier le PDF
        modifier = PDFProcessorComplete()
        print("🔧 Début du traitement PDF...")
        success = modifier.process_pdf(input_path, output_path)
        
        if not success:
            print("❌ Échec du traitement PDF")
            raise HTTPException(status_code=500, detail="Erreur lors de la modification du PDF")
        
        print("✅ Traitement PDF terminé")
        
        # Vérifier que le fichier de sortie existe bien
        import time
        time.sleep(0.2)  # Réduire le délai à 200ms
        
        if not os.path.exists(output_path):
            print(f"❌ Fichier de sortie non trouvé: {output_path}")
            raise HTTPException(status_code=500, detail="Le fichier traité n'a pas été créé")
        
        # Lire le fichier traité en mémoire
        with open(output_path, "rb") as f:
            pdf_content = f.read()
        
        print(f"📖 Fichier lu en mémoire: {len(pdf_content)} bytes")
        
        # Nettoyer immédiatement les fichiers temporaires
        if os.path.exists(input_path):
            os.remove(input_path)
            print(f"🗑️ Fichier d'entrée supprimé: {input_path}")
        if os.path.exists(output_path):
            os.remove(output_path)
            print(f"🗑️ Fichier de sortie supprimé: {output_path}")
        
        # Nom de fichier propre pour le téléchargement
        clean_filename = file.filename.replace('.pdf', '_traité.pdf')
        print(f"📤 Envoi du fichier: {clean_filename}")
        
        # Retourner le contenu depuis la mémoire
        return Response(
            content=pdf_content,
            media_type='application/pdf',
            headers={
                "Content-Disposition": f"attachment; filename={clean_filename}",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
        
    except Exception as e:
        print(f"❌ Erreur lors du traitement: {str(e)}")
        # Nettoyer en cas d'erreur
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement: {str(e)}")

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Endpoint pour télécharger un fichier modifié"""
    file_path = os.path.join("output", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    # Nom de fichier plus propre pour le téléchargement
    clean_filename = filename
    if filename.startswith("modified_"):
        # Enlever le préfixe "modified_" et l'UUID
        parts = filename.split("_", 2)  # Split en 3 parties max
        if len(parts) >= 3:
            clean_filename = f"traité_{parts[2]}"
        else:
            clean_filename = f"traité_{filename.replace('modified_', '')}"
    
    return FileResponse(
        path=file_path,
        filename=clean_filename,
        media_type='application/pdf',
        headers={
            "Content-Disposition": f"attachment; filename={clean_filename}",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 