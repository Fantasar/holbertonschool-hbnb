/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    
    /*------------------------------------------*/
    /*--------===> GESTION DU LOGIN <===------- */
    /*------------------------------------------*/
    
    // Vérifie si on est sur la page login
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        // Écoute la soumission du formulaire
        loginForm.addEventListener('submit', (e) => {
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
            
            // Simulation d'une connexion réussie
            // ICI : Tu ajouteras plus tard ton code pour envoyer les données au serveur
            alert('Connexion réussie ! Bienvenue ' + email);
            
            // Exemple : Redirection après login (à décommenter si besoin)
            // window.location.href = 'index.html';
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

            // Affiche le message
            showMessage();

            // Réinitialise le formulaire
            reviewForm.reset();
        });
    }

    /*------------------------------------------*/
    /*-----===> AUTRES FONCTIONNALITÉS <===----*/
    /*------------------------------------------*/
    // Tu pourras ajouter ici d'autres fonctionnalités :
    // - Chargement dynamique des places
    // - Animation des cartes
    // - Etc.


    console.log('🚀 Site HBNB chargé avec succès !');
});