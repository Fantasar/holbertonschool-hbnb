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

  - **Lien GitHub** : https://github.com/NO6B

  - **Travaux réalisés** : Conception de l’architecture du projet et implémentation des différentes classes.

👨‍💻 **Développeur 02** : Lapique Philippe

  - **Lien GitHub** : https://github.com/Fantasar

  - **Travaux réalisés** : Développement des différentes API, implémentation du modèle Facade et documentation du projet (README).

📂 **Architecture des dossiers** :

Afin de rendre la plateforme plus robuste et plus facile à comprendre, nous avons choisi d’organiser l’architecture du projet à travers plusieurs dossiers, présentés ci-dessous :

**Arborescence du projet** :

<img width="346" height="546" alt="Architecture des dossiers" src="https://github.com/user-attachments/assets/005c9a99-90bc-4acb-8c82-9477a77c420f" />


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

Commande à intégrer dans le terminal : pip install -r requirements.txt

Lancement du serveur Flask :

Commande à intégrer dans le terminal : flask run 

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

**Création d'un nouvelle Utilisateur :** 

<img width="1396" height="566" alt="Création d'un comptre Réussite" src="https://github.com/user-attachments/assets/d3084fbb-3506-4ca6-a104-2619e4cbb679" />

<img width="1398" height="562" alt="Création d'un compte Code erreur " src="https://github.com/user-attachments/assets/4351fda4-b778-4ef6-bf51-538e25c12782" />

**Récupération de la liste des utilisateur :**

<img width="1391" height="666" alt="Récupération d'une liste d'utilisateur" src="https://github.com/user-attachments/assets/a28fdba4-9e8a-45b2-b34f-0eda0d0b1171" />

**Création d'une annonce pour un logement :**

<img width="1387" height="830" alt="Création d'une annonce de logement Réussite" src="https://github.com/user-attachments/assets/fadce76a-06b9-4e0b-93da-9a740e789dc2" />


<img width="1394" height="874" alt="Création d'une annonce de logement erreur" src="https://github.com/user-attachments/assets/6f631784-e3c8-4519-b106-35dadb12a2c4" />

**Récupération des détails d'un logment par son ID :**

<img width="1393" height="674" alt="Récupération des détails d'un logement avec l'ID" src="https://github.com/user-attachments/assets/cbd014ad-5584-4872-86fb-55dca29d0306" />


**Création d'un avis sur un logement :**

<img width="1393" height="587" alt="Création d'un avis sur un logement" src="https://github.com/user-attachments/assets/836e2a16-cd3e-49b0-a3b4-1d2c46b377e3" />


<img width="1397" height="491" alt="Récupérer un avis avec son ID" src="https://github.com/user-attachments/assets/8834d0dc-1bbf-4cf8-851f-3caa2e76af9f" />

**Récupération de la liste des équipeent :**

<img width="1399" height="643" alt="Récupération de la liste des équipements" src="https://github.com/user-attachments/assets/93b0a722-7490-43ed-85d5-671d67db67df" />






