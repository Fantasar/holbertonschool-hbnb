/*============================================*/
/*======= Check autentification User =========*/
/*============================================*/

function checkAuthentication() {
    //Cherche le cookie contenant le token JWT
    const token = getCookie('token');
    //Récupération du formulaire d'ajout d'un avis
    const addReviewSection = document.getElementById('add-review');
    //Est ce que le token existe
    if (!token) {
        console.log('Utilisateur non authentifié - Redirection vers index.html');
        //Redirection d'un utilisateur non connecter vers l'index
        window.location.href = 'index.html';
        return null;
    
    } else {
        //token trouvé donc utilisateur connecté
        console.log('Utilisateur authentifié - Formulaire visible');
        return token;
    }
}

/*============================================*/
/*============= Get Cookies PLace ============*/
/*============================================*/

function getCookie(name) {
    // Utilise la même méthode que scripts.js pour éviter les conflits
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    
    if (parts.length === 2) {
        const cookieValue = parts.pop().split(';').shift();
        console.log(`Cookie "${name}" trouvé:`, cookieValue);
        return cookieValue;
    }

    // Message erreur si pas de cookie
    console.log(`Cookie "${name}" non trouvé`);
    return null;
}

/*=============================================*/
/*============== Get ID Place =================*/
/*=============================================*/

function getPlaceIdFromURL() {
    // window.location.search retourne tout ce qui est après le "?" dans l'URL
    // Exemple : si URL = "add-review.html?id=123", alors search = "?id=123"
    const params = new URLSearchParams(window.location.search);
    const placeID = params.get('id');
    console.log('Place ID récupéré:', placeID);
    return placeID;
}


/*============================================*/
/*=========== Submit a Review ================*/
/*============================================*/

async function submitReview(token, placeId, reviewText, rating) {
    try {
    // === PRÉPARATION DE LA REQUÊTE ===
    
    const headers = {
        'Content-Type': 'application/json', // On dit qu'on envoie/reçoit du JSON
        'Authorization': `Bearer ${token}`   //Token toujours présent
    };

    console.log('Token ajouté aux headers de la requête');
    // === CONSTRUCTION DE L'URL ===
    const apiUrl = `http://localhost:5000/api/v1/reviews/`;
    console.log('Envoi de la requête POST vers:', apiUrl);

    // === ENVOI DE LA REQUÊTE ===
    //fetch() envoi la requête HTTP
    //await = on attend la réponse avant de continuer
    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: headers,
        // JSON.stringify() convertit un objet JavaScript en texte JSON
        body: JSON.stringify({
            text: reviewText,    // Le contenu de l'avis
            place_id: placeId,    // L'ID du logement concerné
            rating: parseInt(rating) // Ajout de la note (convertie en nombre)
        })
    });

    // === VÉRIFICATION DE LA RÉPONSE ===

    // response.ok = true si le code HTTP est 200-299 (succès)
    if (!response.ok) {
        throw new Error(`Erreur HTTP ${response.status}: ${response.statusText}`);
    }
        
    console.log('Avis envoyé avec succès');
        
    // === TRAITEMENT DES DONNÉES ===
        
    // Conversition de la réponse Json en JavaScript
    const data = await response.json();
    console.log('Données recues:', data);

    // Appel du handleResponse pour gérer le succès
    handleResponse(response, data);

    return data;
        
    // === GESTION DES ERREURS ===
    
    } catch (error) {
        // Si une erreur survient (réseau, API down, etc.)
        console.error('Erreur lors de envoie des avis :', error);
        
        alert(`❌ Erreur : Impossible de poster votre avis. ${error.message}`);
        // On peut aussi retourner null pour indiquer l'échec
        return null;
    }

}

/*============================================*/
/*========= Gestion de la réponse  ===========*/
/*============================================*/

function handleResponse(response) {
    if (response.ok) {
        alert('Avis poster avec sucsès');
        
        // Efface le formulaire après un succès
        const reviewForm = document.getElementById('review-form');
        if (reviewForm) {
            reviewForm.reset(); // rest permet de vider tous les champs du formulaires
        }

    } else {
        alert('Echec : Impossible de déposer votre avis');
    }
}


/*============================================*/
/*============ Initialisation  ===============*/
/*============================================*/

// DOMContentLoaded = attend que toute la page HTML soit chargée avant d'exécuter le code
document.addEventListener('DOMContentLoaded', () => {
    console.log('Page chargée, initialisation du formulaire...');

    // Vérifie l'authentification (redirige si non connecté)
    const token = checkAuthentication();

    // Récupérer l'ID du logement depuis l'URL
    const placeId = getPlaceIdFromURL();

    // Verification si l'ID est bien présent sinon Stop !
    if (!placeId) {
        alert('Erreur: Aucun logement spécifié')
        window.location.href = 'index.html';
        return; // Stop l'éxécution
    }
    
    // Récupérer le formulaire d'avis
    const reviewForm = document.getElementById('review-form');

    // Si le formulaire existe sur la page
    if (reviewForm) {
        console.log('Formulaire trouvé, ajout de l\'event listener...');
        
        // 'submit' se déclanche lorseque l'utilisateur soumet le formulaire
        reviewForm.addEventListener('submit', async (event) => {
            // preventDefault() empêche le rechargement de la page (comportement par défaut)
            event.preventDefault();
            console.log('Formulaire soumis');

            // Récupére le texte de l'avis depuis le textarea
            // getElementById() trouve l'élément HTML avec l'id "review-text"
            const reviewTexarea = document.getElementById('review-text')
            const reviewText = reviewTexarea.value.trim() // trim() enlève les espaces inutiles

            // Récupération de la note
            const ratingSelect = document.getElementById('rating');
            const rating = ratingSelect.value;

            // Vérification : l'avis ne doit pas être vide
            if(!reviewText) {
                alert ('⚠️ Veuillez écrire un avis avant de soumettre');
                return; // On arrête si le champs est vide
            }

            if(!rating) {
                alert('⚠️ Veuillez choisir une note avant de soumettre');
                return;
            }

            console.log('Texte de l\'avis:', reviewText);
            console.log('Note:', rating);

            // Désactive le bouton pendant l'envoi ( évite les doubles clics)
            const submitButton = reviewForm.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Envoie en cours ...';
            }

            // Envoie l'avis avec la note
            const result = await submitReview(token, placeId, reviewText, rating);

            // Réactive le bouton
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = 'Envoyer';
            }
        });

    } else {
        // Si le formulaire n'existe pas sur la page
        console.error('Erreur : Formulaire #review-form non trouvé dans le HTML');
    }
});