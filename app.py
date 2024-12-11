import os
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

# Initialisation de l'application Flask
app = Flask(__name__)

# Chargement du modèle pré-entraîné
MODEL_PATH = 'skin_model.h5'  # Remplacez par le chemin vers votre modèle
model = load_model(MODEL_PATH)

# Taille des images utilisées pour l'entrée du modèle
IMG_SIZE = 224

# Dossier pour stocker les images téléchargées temporairement
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dictionnaire des classes pour un modèle avec 7 classes
class_names = {
    0: "Melanocytic nevi",
    1: "Melanoma",
    2: "Benign keratosis-like lesions",
    3: "Basal cell carcinoma",
    4: "Actinic keratoses",
    5: "Vascular lesions",
    6: "Dermatofibroma" 
}

@app.route('/')
def index():
    return render_template('index.html')  # Remplacez par votre fichier HTML principal

@app.route('/analyze', methods=['POST'])
def analyze():
    # Vérification si un fichier a été envoyé
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier téléchargé'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nom de fichier invalide'}), 400

    # Sauvegarder le fichier
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Préparation de l'image pour le modèle
    img = load_img(file_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = img_to_array(img) / 255.0  # Normalisation
    img_array = np.expand_dims(img_array, axis=0)

    # Prédiction
    prediction = model.predict(img_array)
    
    # Trouver l'indice de la classe prédite
    predicted_class_index = np.argmax(prediction, axis=1)[0]
    
    # Récupérer le nom de la classe en utilisant l'indice
    predicted_class_name = class_names.get(predicted_class_index, "Classe inconnue")
    
    # Probabilité de la classe prédite
    predicted_prob = float(prediction[0][predicted_class_index].item()) * 100  # Convertir en float natif

    # Renvoyer les informations sur la classe prédite et la probabilité
    return jsonify({
        'predicted_class': predicted_class_name,
        'confidence': predicted_prob
    })

if __name__ == '__main__':
    app.run(debug=True)
