📘 **Description du projet Hbnb** :

Voici le README du projet Holberton School consistant à construire une plateforme de location : Hbnb.
  Cette deuxième partie du projet porte sur les API RESTful, avec notamment l’implémentation des modèles de classes, 
et le travail sur l’interaction entre le modèle Facade et les différentes API :

  - **Amenity** : contient les équipements présents dans les appartements.
  - **User** : contient les données personnelles des utilisateurs (nom, prénom, mot de passe, etc.).
  - **Place** : contient les logements disponibles sur la plateforme.
  - **Review** : contient les avis des utilisateurs.

**Auteurs et répartition du travail** :


  Afin de faciliter la compréhension du projet, le choix de la langue s’est porté sur le **français** pour les commentaires et 
les descriptions des différentes fonctions, classes ou modules.
  Cependant, une base de code étant fournie par l’école en **anglais**, 
nous ne l’avons pas traduite afin d’éviter d’éventuelles erreurs au lancement du serveur.

Le travail a été réalisé par deux étudiants dont les informations sont présentées ci-dessous :

👨‍💻 **Développeur 01** : Abdelrahman Azhar

  - **Lien GitHub** : (à compléter)

  - **Travaux réalisés** : Conception de l’architecture du projet et implémentation des différentes classes.

👨‍💻 **Développeur 02** : Lapique Philippe

  - **Lien GitHub** : (à compléter)

  - **Travaux réalisés** : Développement des différentes API, implémentation du modèle Facade et documentation du projet (README).

📂 **Architecture des dossiers** :

Afin de rendre la plateforme plus robuste et plus facile à comprendre, nous avons choisi d’organiser l’architecture du projet à travers plusieurs dossiers, présentés ci-dessous :

**Arborescence du projet** :

(Ajouter ici une capture d’écran ou un schéma de l’arborescence des dossiers)

Explication des dossiers :

  - **app/** : contient le code principal de l’application.
  - **api/** : héberge les points de terminaison de l’API, organisés par version (ex. v1/).
  - **models/** : contient les classes représentant la logique métier.
  - **services/** : contient l’implémentation du modèle Facade, gérant l’interaction entre les couches.
  - **persistence/** : contient le dépôt en mémoire.
→ Ce module sera ultérieurement remplacé par une solution basée sur une base de données SQLAlchemy.
  - **run.py** : point d’entrée pour l’exécution de l’application Flask.
  - **config.py** : contient les variables d’environnement et les paramètres de configuration.
  - **requirements.txt** : liste les dépendances Python nécessaires au projet.
  - **README.md** : contient toutes les informations utiles au fonctionnement de la plateforme.

**Configuration de l’environnement** :

  Afin que le serveur fonctionne correctement certaines données présente dans le fichier
requirements doivent être installer :

Installation des dépendances :

Photo de : pip install -r requirements.txt

Lancement du serveur Flask :

Photos de : flask run 

(Ajouter ici des captures d’écran ou des extraits de commandes)

🔒 **Sécurisation des données utilisateur** :

  Lors du développement de la plateforme, une réflexion a été menée sur la sécurisation 
des données sensibles des utilisateurs, notamment les mots de passe.
Pour cela, nous utilisons plusieurs outils intégrés à **Flask** :

  - **Werkzeug** : gère les interactions HTTP et le hachage sécurisé des mots de passe.
  
  - **Jinja2** : permet d’afficher dynamiquement les templates HTML.

  - **itsdangerous** : gère la génération et la vérification des 
signatures cryptographiques (tokens, cookies, etc.).

🧪 **Exemples de cas d’utilisation** : 

  Dans cette section, vous trouverez différents tests réalisés pour vérifier le fonctionnement des API.
Voici quelques codes de réponse HTTP actuellement pris en compte, ainsi que ceux à implémenter à l’avenir :

  - **200** : Requête réussie.

  - **301 / 302** : Redirection permanente ou temporaire.

  - **401** : Utilisateur non authentifié.

  - **403** : Accès refusé.

  - **404** : Ressource non trouvée.

  - **500 / 502 / 503** : Erreurs serveur.

  - **504** : Délai d’attente dépassé.

(Insérer ici des captures d’écran illustrant les réponses de l’API.)

