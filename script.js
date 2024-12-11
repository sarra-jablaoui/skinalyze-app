document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault(); // Empêche le rechargement de la page

    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0]; // Récupère le fichier sélectionné

    if (!file) {
        alert('Veuillez sélectionner une image.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file); // Ajoute l'image au formulaire

    try {
        // Envoi de la requête au serveur
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            // Affiche le résultat détaillé
            document.getElementById('result').innerText = 
                `Classe prédite : ${data.predicted_class} (Confiance : ${(data.confidence).toFixed(2)}%)`;
        } else {
            // Affiche l'erreur
            document.getElementById('result').innerText = `Erreur : ${data.error}`;
        }
    } catch (error) {
        console.error('Erreur:', error);
        document.getElementById('result').innerText = 'Une erreur est survenue.';
    }
});
