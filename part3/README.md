# 🏠 Projet Hbnb - Backend

📘 **Description du projet Hbnb**

Voici le README du projet **Holberton School** consistant à construire une plateforme de location : **Hbnb**.  
Cette troisième partie du projet porte sur le **backend** de l'application, en introduisant **l'authentification et l'autorisation des utilisateurs**,  
ainsi que **l'intégration d'une base de données** à l'aide de **SQLAlchemy** et **SQLite** pour le développement.

### 🎯 Objectifs du projet
1. **Authentification et autorisation** : implémenter une authentification basée sur **JWT** avec **Flask-JWT-Extended**,  
   ainsi qu’un contrôle d’accès par rôles grâce à l’attribut `is_admin` pour certains points de terminaison.
2. **Intégration de la base de données** : remplacer le stockage en mémoire par **SQLite** pour le développement, en utilisant **SQLAlchemy** comme ORM,  
   et préparer la configuration pour **MySQL**.
3. **Opérations CRUD avec persistance** : refactoriser toutes les opérations CRUD afin qu’elles interagissent avec une base de données persistante.
4. **Conception et visualisation de la base de données** : concevoir le schéma relationnel à l’aide de **Mermaid.js**.

---

## 🔒 Sécurisation des données utilisateur

Lors du développement de la plateforme, une réflexion a été menée sur la **sécurisation des données sensibles**.  
Pour cela, plusieurs outils ont été utilisés :

- **Flask-Bcrypt** : pour le hachage sécurisé des mots de passe avant leur enregistrement.  
- **Flask-JWT-Extended** : pour gérer l’authentification via des tokens JWT, garantissant que seules les requêtes autorisées peuvent accéder à certaines ressources.  
- **Contrôle des rôles (`is_admin`)** : pour différencier les actions accessibles aux utilisateurs standards et aux administrateurs.

---

## 📂 Architecture des dossiers

Afin de rendre la plateforme plus robuste et plus facile à comprendre, nous avons choisi d’organiser le projet à travers plusieurs dossiers, présentés ci-dessous :

<img width="318" height="563" alt="Architecture test" src="https://github.com/user-attachments/assets/4e97ee96-02c4-4c6e-b300-7f0133621a70" />

### 📁 Explication des dossiers

- **app/** : contient le code principal de l’application.  
- **api/** : héberge les points de terminaison de l’API, organisés par version (ex. `v1/`).  
- **models/** : contient les classes représentant la logique métier.  
- **services/** : implémente le modèle *Facade*, gérant l’interaction entre les couches.  
- **persistence/** : contient le dépôt en mémoire.  
- **run.py** : point d’entrée pour exécuter l’application Flask.  
- **config.py** : contient les variables d’environnement et les paramètres de configuration.  
- **requirements.txt** : liste les dépendances Python nécessaires au projet.  
- **README.md** : contient toutes les informations utiles au fonctionnement de la plateforme.  
- **Script_test/** : contient les fichiers de test permettant de contrôler la bonne implémentation de la base de données,  
  ainsi que les relations entre les différentes tables.

---

## 💾 Base de données et ORM

Le projet utilise **SQLAlchemy** comme ORM pour gérer la persistance des données.  
- En **développement**, nous utilisons **SQLite** pour sa simplicité.  
- En **production**, l’application sera configurée pour **MySQL**.

Cette intégration permet :
- Des opérations CRUD persistantes ;  
- Une gestion automatique des relations entre entités ;  
- Une compatibilité entre plusieurs systèmes de gestion de bases de données.

---

## ⚙️ Configuration de l’environnement

Afin que le serveur fonctionne correctement, certaines dépendances présentes dans le fichier `requirements.txt` doivent être installées.

### 🧩 Installation des dépendances

pip install -r requirements.txt

Lancement du serveur :

Commande à intégrer dans le terminal : python3 run.py

Nous recommandons pour d'installer un environnement virtuelle afin de pouvoir travailler dans de bonne condition.


## 📊 Diagramme de relations (Mermaid.js)

Afin de mieux comprendre la structure de la base de données, un **diagramme entité-relation (ERD)** a été réalisé à l’aide de **Mermaid.js**.  
Ce diagramme illustre les **relations entre les principales entités** du projet :

- Un **utilisateur (User)** peut posséder plusieurs **lieux (Place)**.
- Un **lieu** peut recevoir plusieurs **réservations (Reservation)** et **avis (Review)**.
- Une **amenity (Amenity)** peut appartenir à plusieurs lieux via la table de jointure **Place_Amenity**.

Ce schéma visuel garantit une compréhension claire des dépendances et des contraintes entre les différentes tables.


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

  # Exemple : Connexion utilisateur
curl -X POST http://127.0.0.1:5000/api/v1/login \
-H "Content-Type: application/json" \
-d '{"email": "user@example.com", "password": "password123"}'


🧪 **Cas d’utilisation des fichiers de contrôle**

Afin de garantir le bon fonctionnement du backend et la cohérence des données dans la base, plusieurs **fichiers de test** ont été mis à disposition.

### ⚙️ Avant d’exécuter les tests
Avant chaque utilisation, **il est impératif de réinitialiser la base de données** afin d’éviter la présence de **données résiduelles** ou de **fichiers fantômes** pouvant fausser les résultats des tests.

### Création automatique d’un utilisateur administrateur
Lors de l’exécution des tests, un **utilisateur administrateur (admin)** est automatiquement créé.  
Cet utilisateur dispose de droits étendus lui permettant d’effectuer différentes requêtes :
- `GET` : lecture des ressources,
- `POST` : création de nouvelles entrées,
- `PUT` : mise à jour des enregistrements,
- `DELETE` : suppression de ressources.

### 🔗 Vérification des relations entre entités
Un des fichiers de test se concentre sur la **validation des relations** entre les différentes tables du modèle de données :
- **One-to-Many** : par exemple, un utilisateur peut posséder plusieurs lieux.
- **Many-to-Many** : par exemple, les liens entre *Place* et *Amenity* via la table de jointure *Place_Amenity*.

Ces tests permettent de s’assurer que les contraintes, clés étrangères et relations SQLAlchemy sont correctement définies et fonctionnelles.

### 🧰 Exemple d’exécution
```bash
# Réinitialiser la base avant le test
python3 reset_db.py

<img width="507" height="485" alt="Test des fonctions" src="https://github.com/user-attachments/assets/bc824157-04c1-4520-9d60-df885f1ac924" />

<img width="559" height="436" alt="Test Relation" src="https://github.com/user-attachments/assets/f0481ecd-0173-445e-9de5-8800751de9a9" />

** 👤Auteurs et répartition du travail** :


  Afin de faciliter la compréhension du projet, le choix de la langue s’est porté sur le **français** pour les commentaires et 
les descriptions des différentes fonctions, classes ou modules.
  Cependant, une base de code étant fournie par l’école en **anglais**, 
nous ne l’avons pas traduite afin d’éviter d’éventuelles erreurs au lancement du serveur.
Nous avons pris la désicion de travailler ensemble sur une grandes parties des fichiers et des tâches afin d'avoir une bonne
compréhension globals du projet.

Le travail a été réalisé par deux étudiants dont les informations sont présentées ci-dessous :

👨‍💻 **Développeur 01** : Abdelrahman Azhar

  - **Lien GitHub** : https://github.com/NO6B

👨‍💻 **Développeur 02** : Lapique Philippe

  - **Lien GitHub** : https://github.com/Fantasar
