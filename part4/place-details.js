/*============================================*/
/*============== Get ID PLace ================*/
/*============================================*/

function getPlaceIdFromURL() {
    //Récupère les id du logement, stocker après ? dans l'url
    const params = new URLSearchParams(window.location.search);
    const placeId = params.get('id');
    console.log('Place ID récupéré:', placeId);
    return placeId;
}

/*============================================*/
/*============= Get Cookies PLace ============*/
/*============================================*/

function getCookie(name) {
    //Permet de séparer tout les cookies présent en tableaux
    const cookies = document.cookie.split('; ');
    //Parcour les cookies pour trouver le bon
    for (let cookie of cookies) {
        //Les clés cookie sont "nom=valeur"
        const [cookieName, cookieValue] = cookie.split('=');
        if (cookieName === name) {
            console.log(`Cookie "${name}" trouvé:`, cookieValue);
            return cookieValue;
        } 
    }

    // Message erreur si pas de cookie
    console.log(`Cookie "${name}" non trouvé`);
    return null;
}

/*============================================*/
/*======= Check autentification User =========*/
/*============================================*/

function checkAuthentication() {
    //Cherche le cookie
    const token = getCookie('token');
    //Récupération du formulaire d'ajout d'un avis
    const addReviewSection = document.getElementById('add-review');

    //Est ce que le token existe
    if (!token) {
        console.log('Utilisateur non authentifié - Formulaire masqué');
        //Permet de cacher le formulaire si non connecter
        if (addReviewSection) {
            addReviewSection.style.display = 'none';
        }
        return null;
    
    } else {
        //token trouvé donc utilisateur connecté
        console.log('Utilisateur authentifié - Formulaire visible');
        if (addReviewSection) {
            addReviewSection.style.display = 'block';
        }
        return token;
    }
}

/*============================================*/
/*========= Get details Place API ============*/
/*============================================*/

async function fetchPlaceDetails(token, placeId) {
    try {
        // === PRÉPARATION DE LA REQUÊTE ===

        const headers = {
            'Content-Type': 'application/json' // On dit qu'on envoie/reçoit du JSON
        };

        //Si utilisateur connecter ajoute son token dans la requête
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
            console.log('Token ajouté aux headers de la requête');
        }

        // === ENVOI DE LA REQUÊTE ===
        const apiUrl = `http://localhost:5000/api/v1/places/${placeId}`;
        console.log('Envoi de la requête GET vers:', apiUrl);

        //fetch() envoi la requête HTTP
        //await = on attend la réponse avant de continuer
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: headers
        });

        // === VÉRIFICATION DE LA RÉPONSE ===

        // response.ok = true si le code HTTP est 200-299 (succès)
        if (!response.ok) {
            throw new Error(`Erreur HTTP ${response.status}: ${response.statusText}`);
        }
        
        console.log('Réponse reçue avec succès');
        
        // === TRAITEMENT DES DONNÉES ===
        
        // Conversition de la réponse Json en JavaScript
        const place = await response.json();
        console.log('Données du logement:', place);

        //Appelle de la fonction pour afficher les données
        return place;
        
    // === GESTION DES ERREURS ===
    
    } catch (error) {
        // Si une erreur survient (réseau, API down, etc.)
        console.error('Erreur lors de la récupération des détails:', error);
        
        // On affiche un message d'erreur à l'utilisateur
        const detailsSection = document.getElementById('place-details');
        detailsSection.innerHTML = `
            <div style="padding: 20px; background-color: #ffebee; border-radius: 10px; color: #c62828;">
                <h3>❌ Erreur</h3>
                <p>Impossible de charger les détails du logement.</p>
                <p>Détails : ${error.message}</p>
            </div>
        `;
        return null;
    }
}

/*============================================*/
/*======== Affiche les infos de PLACE ========*/
/*============================================*/

function displayPlaceDetails(place) {
    console.log('Affichage des détails du logement');
    // Récupération de la section ou afficher les détails
    const detailsSection = document.getElementById('place-details');
    // Permet de vider le contenue sécuriter pour les fichier HTML fantome
    detailsSection.innerHTML = '';

    const imageMapping = {
        'arcachon': 'images/arcachon.jpg',
        'bordeaux': 'images/bordeaux.avif',
        'agen': 'images/agen.jpg',
        'la rochelle': 'images/la_rochelle.jpg',
        'rochelle': 'images/la_rochelle.jpg',
        'limoges': 'images/limoges.jpg'
    };
    
    // Trouve l'image correspondante
    let imageUrl = place.image_url || 'images/default-place.jpg';
    
    // Si pas d'image_url dans l'API, cherche dans le mapping
    if (!place.image_url) {
        const titleLower = (place.title || place.name || '').toLowerCase();
        
        for (const [city, img] of Object.entries(imageMapping)) {
            if (titleLower.includes(city)) {
                imageUrl = img;
                break;
            }
        }
    }

    // === CRÉATION DU HTML POUR LE LOGEMENT ===
    const placeDiv = document.createElement('div');
    placeDiv.className = 'place-details'; // Classe CSS

    // On construit le HTML avec les données de l'API
    // Les ${variable} sont remplacées par les vraies valeurs
    placeDiv.innerHTML = `
        <div class="place-info">
            <img src="${imageUrl}" alt="${place.title || place.name}" class="place-img" onerror="this.src='images/default-place.jpg'" style="max-width: 100%; border-radius: 10px; margin-bottom: 20px;">
            <h1>${place.name || place.title || 'Nom non disponible'}</h1>
            <p><strong>Hôte :</strong> ${place.host ? `${place.host.first_name} ${place.host.last_name}` : 'Inconnu'}</p>
            <p><strong>Prix :</strong> ${place.price || '0'}€ / nuit</p>
            <p><strong>Description:</strong> ${place.description || 'Pas de description'}</p>
            
            <h3>Équipements :</h3>
            <ul>
                ${generateAmenitiesList(place.amenities)}
            </ul>
        </div>
    `;

    // On ajoute le div au DOM de la page
    detailsSection.appendChild(placeDiv);

    // === AFFICHAGE DES AVIS ===
    // Si des avis existent, on les affiche
    if (place.reviews && place.reviews.length > 0) {
        displayReviews(place.reviews);
    } else {
        // Sinon, on affiche un message
        const reviewsSection = document.getElementById('reviews');
        reviewsSection.innerHTML = '<p>Aucun avis pour le moment. Soyez le premier à donner votre avis !</p>';
    }

    addReviewButton(place.id)
}

/*============================================*/
/*===== Affiche les équipement de PLACE ======*/
/*============================================*/

function generateAmenitiesList(amenities) {
    //Si aucun équipeent présent retour message
    if (!amenities || amenities.length === 0) {
        return '<li>Aucun équipement spécifié</li>';
    }

    // On transforme le tableau en HTML
    // .map() = pour chaque équipement, on crée un <li>
    // .join('') = on colle tous les <li> ensemble en une seule chaîne
    return amenities.map(amenity => `<li>${amenity}</li>`).join('');    
}

/*============================================*/
/*======= Affiche les avis de PLACE ==========*/
/*============================================*/

function displayReviews(reviews) {
    console.log(`Affichage de ${reviews.length} avis`);

    // Récupère la section des avis
    const reviewsSection = document.getElementById('reviews');
    // On vide et on ajoute le titre
    reviewsSection.innerHTML = '<h2>Avis des clients</h2>';

    //On créer le conteneur pour stocker les cartes d'avis pour le CSS
    const container = document.createElement('div');
    container.id = 'reviews-container';

    //Pour chaque avis dans le tableau
    reviews.forEach(review => {
        // On crée une carte d'avis
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';
        
        // On génère les étoiles en fonction de la note
        const stars = generateStars(review.rating);
        
        // On construit le HTML de la carte
        reviewCard.innerHTML = `
            <p class="comment">"${review.comment || 'Pas de commentaire'}"</p>
            <p class="user">Par : ${review.user || 'Anonyme'}</p>
            <p class="rating">${stars} (${review.rating}/5)</p>
        `;
        
        // On ajoute la carte au conteneur
        container.appendChild(reviewCard);
    });

    // On ajoute le container à la section
    reviewsSection.appendChild(container);
}

/*============================================*/
/*====== Permet de gérer les étoiles  ========*/
/*============================================*/

function generateStars(rating) {
    // On crée une chaîne avec le bon nombre d'étoiles pleines et vides
    let stars = '';
    
    // Étoiles pleines (de 1 à rating)
    for (let i = 1; i <= 5; i++) {
        if (i <= rating) {
            stars += '⭐'; // Étoile pleine
        } else {
            stars += '☆'; // Étoile vide
        }
    }
    
    return stars;
}


/*============================================*/
/*====== Bouton pour ajouter un avis  ========*/
/*============================================*/

function addReviewButton(placeId) {
    const detailsSection = document.getElementById('place-details');

    const buttonHTML = `
        <div style="margin-top: 30px; text-align: center;">
            <a href="add_review.html?id=${placeId}" 
               class="add-review-button"
               style="background-color: #34967C; 
                      color: white; 
                      padding: 15px 30px; 
                      text-decoration: none; 
                      border-radius: 8px;
                      display: inline-block;
                      font-weight: bold;
                      transition: all 0.3s ease;">
                ✍️ Ajouter un avis sur ce logement
            </a>
        </div>
    `;

    if (detailsSection) {
        detailsSection.insertAdjacentHTML('beforeend', buttonHTML);
        console.log('Bouton "Ajouter un avis" créé avec ID:', placeId);
    }
}


/*============================================*/
/*============ Initialisation  ===============*/
/*============================================*/

document.addEventListener('DOMContentLoaded', async () => {
    console.log('=== Chargement de la page place.html ===');
    
    // ÉTAPE 1 : On récupère l'ID du logement depuis l'URL
    const placeId = getPlaceIdFromURL();
    
    // Vérification : est-ce qu'on a bien un ID ?
    if (!placeId) {
        console.error('Aucun ID de logement trouvé dans l\'URL');
        alert('Erreur : Aucun logement sélectionné. Retour à la page d\'accueil.');
        window.location.href = 'index.html'; // Redirection vers l'accueil
        return; // On arrête l'exécution
    }
    
    // ÉTAPE 2 : On vérifie si l'utilisateur est connecté
    const token = checkAuthentication();
    
    // ÉTAPE 3 : On récupère et affiche les détails du logement
    const place = await fetchPlaceDetails(token, placeId);
    
    // ÉTAPE 4 : Si on a bien récupéré les données, les afficher
    if (place) {
        displayPlaceDetails(place);
    }

    console.log('=== Initialisation terminée ===');
});
