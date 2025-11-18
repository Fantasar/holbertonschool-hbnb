/*------------------------------------------*/
/*--------===> GESTION DU L'API <===------- */
/*------------------------------------------*/

const API_BASE_URL = 'http://localhost:5000/api/v1';
const API_LOGIN_ENDPOINT = `${API_BASE_URL}/auth/login`;

/*------------------------------------------*/
/*----===> Chargement de la page <===------ */
/*------------------------------------------*/

document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Site HBNB chargé avec succès !');

    /*------------------------------------------*/
    /*--------===> GESTION DU LOGIN <===------- */
    /*------------------------------------------*/
    
    // Vérifie si on est sur la page login
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        // Écoute la soumission du formulaire
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault(); // Empêche le rechargement de la page
            
            // Récupère les valeurs des champs
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            // Validation simple
            if (!email || !password) {
                alert('Merci de remplir tous les champs !');
                return;
            }
            
            // Validation du format email
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert('Merci d\'entrer une adresse email valide !');
                return;
            }
            
            // Affiche dans la console (pour le développement)
            console.log('=== TENTATIVE DE CONNEXION ===');
            console.log('Email:', email);
            console.log('Password:', password);
            console.log('===========================');
            
            // Désactiver le bouton pendant la requête
            const submitButton = loginForm.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            submitButton.textContent = '⏳ Connexion en cours...';
            submitButton.disabled = true;

            try {
                //Appel à l'API pour test la connexion
                const success = await loginUser(email, password);

                if (success) {
                    //Connexion réussie
                    console.log('✅ Connexion réussie !');
                    showSuccess('Connexion réussie ! Redirection...');

                    //Redirection vers index.html
                    setTimeout(() => {
                        window.location.href = 'index.html';
                    }, 1000);
                }
            } catch (error) {
                console.error('❌ Erreur lors de la connexion:', error);
                showError('Une erreur est survenue. Veuillez réessayer.');
            } finally {
                // Permet de réactiver le bouton
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            }
            
        });
        
        /*------------------------------------------*/
        /*-----===> ANIMATION DES INPUTS <===------ */
        /*------------------------------------------*/
        
        // Récupère tous les inputs du formulaire
        const inputs = loginForm.querySelectorAll('input');
        
        // Ajoute des effets visuels au focus/blur
        inputs.forEach(input => {
            // Quand on clique dans l'input
            input.addEventListener('focus', () => {
                input.style.transform = 'scale(1.02)';
                input.style.transition = 'transform 0.3s';
            });
            
            // Quand on quitte l'input
            input.addEventListener('blur', () => {
                input.style.transform = 'scale(1)';
            });
        });
    }


    /*------------------------------------------*/
    /*-----===> FORMULAIRE ADD REVIEW <===-----*/
    /*------------------------------------------*/

    const reviewForm = document.getElementById('review-form');

    if (reviewForm) {
        // Crée dynamiquement un message flottant de confirmation
        const floating = document.createElement('div');
        floating.id = 'floating-confirmation';
        floating.textContent = "✅ Merci ! Votre avis a été ajouté.";
        floating.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            opacity: 0;
            transform: translateY(-20px);
            transition: opacity 0.4s, transform 0.4s;
            z-index: 9999;
        `;
        document.body.appendChild(floating);

        // Fonction pour afficher le message
        const showMessage = () => {
            floating.style.opacity = '1';
            floating.style.transform = 'translateY(0)';
            setTimeout(() => {
                floating.style.opacity = '0';
                floating.style.transform = 'translateY(-20px)';
            }, 3000);
        };

        reviewForm.addEventListener('submit', (e) => {
            e.preventDefault(); // Empêche le rechargement

            // Ici tu pourrais envoyer les données au serveur via fetch/ajax
            console.log('📝 Avis soumis (simulation)');
            // Affiche le message
            showMessage();

            // Réinitialise le formulaire
            reviewForm.reset();
        });
    }
});

/*-------------------------------------------*/
/*-===> Fonction de la connexion à l'Api <==-*/
/*-------------------------------------------*/

/**
 * Envoie les identifiants à l'API backend
 * @param {string} email - Email de l'utilisateur
 * @param {string} password - Mot de passe de l'utilisateur
 * @returns {Promise<boolean>} - true si connexion réussie, false sinon
 */
async function loginUser(email, password) {
    try {
        console.log('📤 Envoi de la requête à l\'API:', API_LOGIN_ENDPOINT);
        
        // Envoyer la requête POST à l'API
        const response = await fetch(API_LOGIN_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });
        
        console.log('📥 Réponse reçue:', response.status, response.statusText);
        
        // Vérifier si la requête a réussi
        if (response.ok) {
            // Récupérer les données JSON
            const data = await response.json();
            console.log('📦 Données reçues:', data);
            
            // Vérifier que le token existe
            if (data.access_token) {
                // Sauvegarder le token dans un cookie
                saveTokenToCookie(data.access_token);
                console.log('🍪 Token sauvegardé dans un cookie');
                return true;
            } else {
                console.error('❌ Token manquant dans la réponse');
                showError('Erreur serveur : token manquant');
                return false;
            }
        } else {
            // Connexion échouée - essayer de récupérer le message d'erreur
            let errorMessage = 'Email ou mot de passe incorrect';
            
            try {
                const errorData = await response.json();
                if (errorData.message) {
                    errorMessage = errorData.message;
                } else if (errorData.error) {
                    errorMessage = errorData.error;
                }
            } catch (e) {
                // Pas de message d'erreur JSON disponible
            }
            
            console.error('❌ Connexion échouée:', errorMessage);
            showError(errorMessage);
            return false;
        }
    } catch (error) {
        // Erreur réseau ou autre erreur technique
        console.error('❌ Erreur réseau:', error);
        
        // Message d'erreur plus détaillé selon le type d'erreur
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            showError('Impossible de contacter le serveur. Vérifiez que votre API est bien démarrée.');
        } else {
            showError('Une erreur réseau est survenue. Vérifiez votre connexion internet.');
        }
        
        return false;
    }
}

/*============================================*/
/*===== GESTION DES COOKIES ==================*/
/*============================================*/

/**
 * Sauvegarde le JWT token dans un cookie
 * @param {string} token - Le JWT token à sauvegarder
 */
function saveTokenToCookie(token) {
    // Créer un cookie qui expire dans 7 jours
    const expirationDays = 7;
    const date = new Date();
    date.setTime(date.getTime() + (expirationDays * 24 * 60 * 60 * 1000));
    const expires = `expires=${date.toUTCString()}`;
    
    // Sauvegarder le cookie
    // SameSite=Lax pour la sécurité
    document.cookie = `token=${token}; ${expires}; path=/; SameSite=Lax`;
}

/**
 * Récupère un cookie par son nom
 * @param {string} name - Le nom du cookie
 * @returns {string|null} - La valeur du cookie ou null
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
    return null;
}

/**
 * Vérifie si l'utilisateur est connecté
 * @returns {boolean} - true si connecté, false sinon
 */
function isUserLoggedIn() {
    return getCookie('token') !== null;
}

/**
 * Déconnecte l'utilisateur (supprime le cookie)
 */
function logoutUser() {
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    console.log('👋 Utilisateur déconnecté');
    window.location.href = 'login.html';
}

/*============================================*/
/*===== AFFICHAGE DES MESSAGES ===============*/
/*============================================*/

/**
 * Affiche un message d'erreur
 * @param {string} message - Le message à afficher
 */
function showError(message) {
    // Utilise alert pour l'instant (simple)
    alert('❌ ' + message);
    
    // Alternative : afficher dans un élément HTML
    // Si tu as un <div id="error-message"></div> dans ton HTML
    const errorElement = document.getElementById('error-message');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        errorElement.style.color = 'red';
        errorElement.style.padding = '10px';
        errorElement.style.marginTop = '10px';
        errorElement.style.backgroundColor = '#ffe0e0';
        errorElement.style.borderRadius = '5px';
        
        // Cacher après 5 secondes
        setTimeout(() => {
            errorElement.style.display = 'none';
        }, 5000);
    }
}

/**
 * Affiche un message de succès
 * @param {string} message - Le message à afficher
 */
function showSuccess(message) {
    // Utilise alert pour l'instant
    alert('✅ ' + message);
    
    // Alternative : afficher dans un élément HTML
    const successElement = document.getElementById('success-message');
    if (successElement) {
        successElement.textContent = message;
        successElement.style.display = 'block';
        successElement.style.color = 'green';
        successElement.style.padding = '10px';
        successElement.style.marginTop = '10px';
        successElement.style.backgroundColor = '#e0ffe0';
        successElement.style.borderRadius = '5px';
        
        // Cacher après 3 secondes
        setTimeout(() => {
            successElement.style.display = 'none';
        }, 3000);
    }
}

/*============================================*/
/*===== FONCTIONS UTILITAIRES ================*/
/*============================================*/

/**
 * Fonction de test pour vérifier si l'API est accessible
 * Appelle cette fonction dans la console pour tester
 */
async function testAPIConnection() {
    console.log('🧪 Test de connexion à l\'API...');
    console.log('URL:', API_LOGIN_ENDPOINT);
    
    try {
        const response = await fetch(API_LOGIN_ENDPOINT, {
            method: 'OPTIONS' // Requête OPTIONS pour tester CORS
        });
        
        if (response.ok) {
            console.log('✅ L\'API est accessible !');
        } else {
            console.log('⚠️ L\'API répond mais avec une erreur:', response.status);
        }
    } catch (error) {
        console.error('❌ Impossible de contacter l\'API:', error);
        console.log('💡 Vérifie que ton backend est bien démarré et que l\'URL est correcte.');
    }
}

// Pour débugger : affiche le token actuel dans la console
function debugShowToken() {
    const token = getCookie('token');
    if (token) {
        console.log('🍪 Token actuel:', token);
    } else {
        console.log('❌ Aucun token trouvé');
    }
}
