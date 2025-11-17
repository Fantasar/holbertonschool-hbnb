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
    /*-----===> AUTRES FONCTIONNALITÉS <===---- */
    /*------------------------------------------*/
    
    // Tu pourras ajouter ici d'autres fonctionnalités :
    // - Gestion des reviews
    // - Chargement des places
    // - etc.
    
    console.log('🚀 Site HBNB chargé avec succès !');
});