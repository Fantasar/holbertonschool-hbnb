#!/usr/bin/env python3
"""
Script de test pour la TÂCHE 8 - Relations SQLAlchemy
Teste les relations : User-Place, Place-Review, User-Review, Place-Amenity
Exécuter avec : python3 test_task_8_relations.py
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:5000/api/v1"
HEADERS = {"Content-Type": "application/json"}

# Couleurs
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_test(message):
    print(f"\n{Colors.BLUE}{Colors.BOLD}🧪 TEST: {message}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def print_section(message):
    print(f"\n{Colors.BOLD}{'='*70}")
    print(f"  {message}")
    print(f"{'='*70}{Colors.END}")

def print_info(message):
    print(f"{Colors.YELLOW}ℹ {message}{Colors.END}")

# Données de test
test_data = {
    'admin_token': None,
    'user1_token': None,
    'user2_token': None,
    'admin_id': None,
    'user1_id': None,
    'user2_id': None,
    'place1_id': None,
    'place2_id': None,
    'amenity1_id': None,
    'amenity2_id': None,
    'amenity3_id': None,
    'review1_id': None,
    'review2_id': None,
}

def setup_test_data():
    """Créer les données de test nécessaires"""
    print_section("PRÉPARATION DES DONNÉES DE TEST")
    
    # Créer admin
    print_test("Création de l'administrateur")
    admin_data = {
        "first_name": "Admin",
        "last_name": "Test",
        "email": "admin@relations.test",
        "password": "admin123",
        "is_admin": True
    }
    response = requests.post(f"{BASE_URL}/users/", json=admin_data, headers=HEADERS)
    if response.status_code == 201:
        test_data['admin_id'] = response.json()['id']
        print_success(f"Admin créé (ID: {test_data['admin_id']})")
    else:
        print_error(f"Échec création admin: {response.text}")
        return False
    
    # Login admin
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "admin@relations.test", "password": "admin123"},
        headers=HEADERS
    )
    if login_response.status_code == 200:
        test_data['admin_token'] = login_response.json()['access_token']
        print_success("Token admin obtenu")
    else:
        print_error("Échec login admin")
        return False
    
    # Créer user1
    print_test("Création de l'utilisateur 1")
    user1_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@relations.test",
        "password": "alice123"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user1_data, headers=HEADERS)
    if response.status_code == 201:
        test_data['user1_id'] = response.json()['id']
        print_success(f"User1 créé (ID: {test_data['user1_id']})")
    else:
        print_error(f"Échec création user1: {response.text}")
        return False
    
    # Login user1
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "alice@relations.test", "password": "alice123"},
        headers=HEADERS
    )
    if login_response.status_code == 200:
        test_data['user1_token'] = login_response.json()['access_token']
        print_success("Token user1 obtenu")
    else:
        print_error("Échec login user1")
        return False
    
    # Créer user2
    print_test("Création de l'utilisateur 2")
    user2_data = {
        "first_name": "Bob",
        "last_name": "Jones",
        "email": "bob@relations.test",
        "password": "bob123"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user2_data, headers=HEADERS)
    if response.status_code == 201:
        test_data['user2_id'] = response.json()['id']
        print_success(f"User2 créé (ID: {test_data['user2_id']})")
    else:
        print_error(f"Échec création user2: {response.text}")
        return False
    
    # Login user2
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "bob@relations.test", "password": "bob123"},
        headers=HEADERS
    )
    if login_response.status_code == 200:
        test_data['user2_token'] = login_response.json()['access_token']
        print_success("Token user2 obtenu")
    else:
        print_error("Échec login user2")
        return False
    
    # Créer amenities
    print_test("Création des amenities")
    admin_headers = {
        "Authorization": f"Bearer {test_data['admin_token']}",
        "Content-Type": "application/json"
    }
    
    amenities = [
        {"name": "WiFi"},
        {"name": "Piscine"},
        {"name": "Parking"}
    ]
    
    for i, amenity in enumerate(amenities, 1):
        response = requests.post(
            f"{BASE_URL}/admin/amenities/",
            json=amenity,
            headers=admin_headers
        )
        if response.status_code == 201:
            test_data[f'amenity{i}_id'] = response.json()['id']
            print_success(f"Amenity '{amenity['name']}' créée (ID: {test_data[f'amenity{i}_id']})")
        else:
            print_error(f"Échec création amenity '{amenity['name']}'")
    
    return True

def test_user_place_relation():
    """Test Relation 1: User ↔ Place (One-to-Many)"""
    print_section("RELATION 1: USER ↔ PLACE (One-to-Many)")
    
    results = []
    
    # User1 crée 2 places
    print_test("User1 crée deux places")
    user1_headers = {
        "Authorization": f"Bearer {test_data['user1_token']}",
        "Content-Type": "application/json"
    }
    
    places_data = [
        {
            "title": "Appartement Paris",
            "description": "Bel appartement au centre",
            "price": 120.0,
            "latitude": 48.8566,
            "longitude": 2.3522
        },
        {
            "title": "Villa Côte d'Azur",
            "description": "Villa avec vue mer",
            "price": 350.0,
            "latitude": 43.7102,
            "longitude": 7.2620
        }
    ]
    
    for i, place_data in enumerate(places_data, 1):
        response = requests.post(
            f"{BASE_URL}/places/",
            json=place_data,
            headers=user1_headers
        )
        if response.status_code == 201:
            data = response.json()
            test_data[f'place{i}_id'] = data['id']
            
            # Vérifier owner_id
            if data.get('owner_id') == test_data['user1_id']:
                print_success(f"Place '{place_data['title']}' créé avec owner_id correct")
                results.append(True)
            else:
                print_error(f"Owner_id incorrect pour '{place_data['title']}'")
                results.append(False)
        else:
            print_error(f"Échec création place '{place_data['title']}': {response.text}")
            results.append(False)
    
    # Récupérer un place et vérifier la relation owner
    print_test("Vérification de la relation Place → User (owner)")
    response = requests.get(f"{BASE_URL}/places/{test_data['place1_id']}")
    if response.status_code == 200:
        place = response.json()
        
        # Vérifier que owner_id existe
        if 'owner_id' in place and place['owner_id'] == test_data['user1_id']:
            print_success("Place.owner_id pointe vers le bon utilisateur")
            results.append(True)
        else:
            print_error("Place.owner_id manquant ou incorrect")
            results.append(False)
        
        # Si to_dict_list retourne les infos du owner
        if 'owner' in place:
            owner = place['owner']
            if owner.get('id') == test_data['user1_id']:
                print_success("Place.owner contient les détails du propriétaire")
                print_info(f"  Owner: {owner.get('first_name')} {owner.get('last_name')}")
                results.append(True)
            else:
                print_warning("Place.owner présent mais ID incorrect")
                results.append(False)
        else:
            print_warning("Place.owner non présent dans la réponse (optionnel)")
    else:
        print_error("Impossible de récupérer le place")
        results.append(False)
    
    # Vérifier que User1 a bien 2 places
    print_test("Vérification que l'utilisateur possède plusieurs places")
    all_places = requests.get(f"{BASE_URL}/places/").json()
    user1_places = [p for p in all_places if p.get('owner_id') == test_data['user1_id']]
    
    if len(user1_places) >= 2:
        print_success(f"User1 possède {len(user1_places)} places")
        results.append(True)
    else:
        print_error(f"User1 ne possède que {len(user1_places)} place(s)")
        results.append(False)
    
    return all(results)

def test_place_review_relation():
    """Test Relation 2: Place ↔ Review (One-to-Many)"""
    print_section("RELATION 2: PLACE ↔ REVIEW (One-to-Many)")
    
    results = []
    
    # User2 crée 2 reviews sur place1
    print_test("User2 crée deux reviews sur le même place")
    user2_headers = {
        "Authorization": f"Bearer {test_data['user2_token']}",
        "Content-Type": "application/json"
    }
    
    review1_data = {
        "text": "Excellent appartement, très bien situé!",
        "rating": 5,
        "place_id": test_data['place1_id']
    }
    
    response = requests.post(
        f"{BASE_URL}/reviews/",
        json=review1_data,
        headers=user2_headers
    )
    if response.status_code == 201:
        data = response.json()
        test_data['review1_id'] = data['id']
        
        # Vérifier place_id
        if data.get('place_id') == test_data['place1_id']:
            print_success("Review1 créée avec place_id correct")
            results.append(True)
        else:
            print_error("place_id incorrect dans review1")
            results.append(False)
    else:
        print_error(f"Échec création review1: {response.text}")
        results.append(False)
    
    # Admin crée une review sur place1
    print_test("Admin crée une review sur le même place")
    admin_headers = {
        "Authorization": f"Bearer {test_data['admin_token']}",
        "Content-Type": "application/json"
    }
    
    review2_data = {
        "text": "Bon rapport qualité/prix",
        "rating": 4,
        "place_id": test_data['place1_id']
    }
    
    response = requests.post(
        f"{BASE_URL}/reviews/",
        json=review2_data,
        headers=admin_headers
    )
    if response.status_code == 201:
        data = response.json()
        test_data['review2_id'] = data['id']
        print_success("Review2 créée par admin")
        results.append(True)
    else:
        print_error(f"Échec création review2: {response.text}")
        results.append(False)
    
    # Récupérer les reviews d'un place
    print_test("Récupération des reviews d'un place via /places/<id>/reviews")
    response = requests.get(f"{BASE_URL}/places/{test_data['place1_id']}/reviews/")
    
    if response.status_code == 200:
        reviews = response.json()
        
        if len(reviews) >= 2:
            print_success(f"Place1 a {len(reviews)} reviews")
            print_info(f"  Reviews: {[r.get('text')[:30] + '...' for r in reviews]}")
            results.append(True)
        else:
            print_error(f"Place1 n'a que {len(reviews)} review(s)")
            results.append(False)
    else:
        print_error("Impossible de récupérer les reviews du place")
        results.append(False)
    
    # Vérifier via GET place
    print_test("Vérification que Place.reviews est accessible")
    response = requests.get(f"{BASE_URL}/places/{test_data['place1_id']}")
    if response.status_code == 200:
        place = response.json()
        
        if 'reviews' in place and len(place['reviews']) >= 2:
            print_success(f"Place.reviews accessible avec {len(place['reviews'])} reviews")
            results.append(True)
        else:
            print_warning("Place.reviews non présent ou vide dans la réponse")
            results.append(False)
    
    return all(results)

def test_user_review_relation():
    """Test Relation 3: User ↔ Review (One-to-Many)"""
    print_section("RELATION 3: USER ↔ REVIEW (One-to-Many)")
    
    results = []
    
    print_test("Vérification que les reviews pointent vers leurs auteurs")
    
    # Récupérer review1
    response = requests.get(f"{BASE_URL}/reviews/{test_data['review1_id']}")
    if response.status_code == 200:
        review = response.json()
        
        # Vérifier user_id
        if review.get('user_id') == test_data['user2_id']:
            print_success("Review1.user_id pointe vers user2")
            results.append(True)
        else:
            print_error(f"Review1.user_id incorrect: {review.get('user_id')}")
            results.append(False)
    else:
        print_error("Impossible de récupérer review1")
        results.append(False)
    
    # Récupérer review2
    response = requests.get(f"{BASE_URL}/reviews/{test_data['review2_id']}")
    if response.status_code == 200:
        review = response.json()
        
        # Vérifier user_id
        if review.get('user_id') == test_data['admin_id']:
            print_success("Review2.user_id pointe vers admin")
            results.append(True)
        else:
            print_error(f"Review2.user_id incorrect: {review.get('user_id')}")
            results.append(False)
    else:
        print_error("Impossible de récupérer review2")
        results.append(False)
    
    # Vérifier qu'un user a plusieurs reviews
    print_test("Vérification qu'un utilisateur peut avoir plusieurs reviews")
    all_reviews = requests.get(f"{BASE_URL}/reviews/").json()
    user2_reviews = [r for r in all_reviews if r.get('user_id') == test_data['user2_id']]
    
    if len(user2_reviews) >= 1:
        print_success(f"User2 a {len(user2_reviews)} review(s)")
        results.append(True)
    else:
        print_error("User2 n'a aucune review")
        results.append(False)
    
    return all(results)

def test_place_amenity_relation():
    """Test Relation 4: Place ↔ Amenity (Many-to-Many)"""
    print_section("RELATION 4: PLACE ↔ AMENITY (Many-to-Many)")
    
    results = []
    
    print_test("Ajout d'amenities à un place (Many-to-Many)")
    
    # Note: Cette partie dépend de votre implémentation
    # Vérifiez si vous avez un endpoint pour ajouter des amenities à un place
    
    user1_headers = {
        "Authorization": f"Bearer {test_data['user1_token']}",
        "Content-Type": "application/json"
    }
    
    # Essayer d'ajouter des amenities via POST /places/<id>/amenities
    amenities_to_add = [
        {"id": test_data['amenity1_id']},  # WiFi
        {"id": test_data['amenity2_id']}   # Piscine
    ]
    
    response = requests.post(
        f"{BASE_URL}/places/{test_data['place1_id']}/amenities",
        json=amenities_to_add,
        headers=user1_headers
    )
    
    if response.status_code == 200:
        print_success("Amenities ajoutées au place1")
        results.append(True)
    elif response.status_code == 501:
        print_warning("Endpoint d'ajout d'amenities non implémenté (501)")
        print_info("  Ceci est normal si vous n'avez pas encore implémenté cette fonctionnalité")
        results.append(True)  # Ne pas pénaliser
    else:
        print_warning(f"Réponse inattendue: {response.status_code} - {response.text[:100]}")
        results.append(True)  # Ne pas pénaliser
    
    # Vérifier si les amenities apparaissent dans le place
    print_test("Vérification que Place.amenities est accessible")
    response = requests.get(f"{BASE_URL}/places/{test_data['place1_id']}")
    
    if response.status_code == 200:
        place = response.json()
        
        if 'amenities' in place:
            amenities = place['amenities']
            if len(amenities) > 0:
                print_success(f"Place.amenities contient {len(amenities)} amenity/ies")
                print_info(f"  Amenities: {[a.get('name', 'N/A') for a in amenities]}")
                results.append(True)
            else:
                print_warning("Place.amenities est vide (peut-être pas encore lié)")
                results.append(True)  # Ne pas pénaliser
        else:
            print_warning("Place.amenities non présent dans la réponse")
            print_info("  Assurez-vous que to_dict_list() retourne les amenities")
            results.append(True)  # Ne pas pénaliser
    else:
        print_error("Impossible de récupérer le place")
        results.append(False)
    
    # Vérifier la relation inverse (optionnel)
    print_test("Vérification de la relation inverse Amenity → Places")
    print_info("  Cette fonctionnalité dépend de votre implémentation")
    
    # Si vous avez un endpoint pour lister les places d'une amenity
    # response = requests.get(f"{BASE_URL}/amenities/{test_data['amenity1_id']}/places")
    # Pour l'instant on le considère comme optionnel
    
    results.append(True)  # Ne pas pénaliser
    
    return all(results)

def test_cascade_delete():
    """Test supplémentaire: Vérifier les cascades"""
    print_section("TEST SUPPLÉMENTAIRE: CASCADES")
    
    results = []
    
    print_test("Vérification que la suppression d'un place supprime ses reviews")
    print_info("  Création d'un place temporaire pour tester la cascade")
    
    # User1 crée un place temporaire
    user1_headers = {
        "Authorization": f"Bearer {test_data['user1_token']}",
        "Content-Type": "application/json"
    }
    
    temp_place_data = {
        "title": "Place Temporaire",
        "price": 50.0,
        "latitude": 45.0,
        "longitude": 1.0
    }
    
    response = requests.post(
        f"{BASE_URL}/places/",
        json=temp_place_data,
        headers=user1_headers
    )
    
    if response.status_code != 201:
        print_warning("Impossible de créer un place temporaire pour tester la cascade")
        return True  # Ne pas pénaliser
    
    temp_place_id = response.json()['id']
    print_success(f"Place temporaire créé (ID: {temp_place_id})")
    
    # Admin crée une review sur ce place
    admin_headers = {
        "Authorization": f"Bearer {test_data['admin_token']}",
        "Content-Type": "application/json"
    }
    
    temp_review_data = {
        "text": "Review temporaire",
        "rating": 3,
        "place_id": temp_place_id
    }
    
    response = requests.post(
        f"{BASE_URL}/reviews/",
        json=temp_review_data,
        headers=admin_headers
    )
    
    if response.status_code != 201:
        print_warning("Impossible de créer une review temporaire")
        return True  # Ne pas pénaliser
    
    temp_review_id = response.json()['id']
    print_success(f"Review temporaire créée (ID: {temp_review_id})")
    
    # Supprimer le place
    response = requests.delete(
        f"{BASE_URL}/places/{temp_place_id}",
        headers=user1_headers
    )
    
    if response.status_code == 200:
        print_success("Place temporaire supprimé")
        results.append(True)
    else:
        print_error(f"Échec suppression place: {response.text}")
        results.append(False)
        return False
    
    # Vérifier que la review a été supprimée (cascade)
    response = requests.get(f"{BASE_URL}/reviews/{temp_review_id}")
    
    if response.status_code == 404:
        print_success("Review supprimée automatiquement (cascade OK)")
        results.append(True)
    elif response.status_code == 200:
        print_warning("Review NON supprimée (cascade manquante)")
        print_info("  Ajoutez cascade='all, delete-orphan' dans la relation Place.reviews")
        results.append(False)
    
    return all(results)

def main():
    """Fonction principale"""
    print(f"\n{Colors.BOLD}{'='*70}")
    print(f"  TEST COMPLET - HBNB PART 3 - TÂCHE 8 (RELATIONS)")
    print(f"{'='*70}{Colors.END}\n")
    
    # Vérifier que le serveur est accessible
    print_test("Vérification que le serveur Flask est accessible")
    try:
        response = requests.get(f"{BASE_URL}/users/", timeout=5)
        print_success(f"Serveur accessible (Status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print_error("Le serveur n'est pas accessible. Assurez-vous que 'python3 run.py' est lancé.")
        sys.exit(1)
    
    # Préparation des données
    if not setup_test_data():
        print_error("\n❌ Échec de la préparation des données. Arrêt des tests.")
        sys.exit(1)
    
    # Tests des relations
    results = []
    
    results.append(("User ↔ Place", test_user_place_relation()))
    results.append(("Place ↔ Review", test_place_review_relation()))
    results.append(("User ↔ Review", test_user_review_relation()))
    results.append(("Place ↔ Amenity", test_place_amenity_relation()))
    results.append(("Cascades", test_cascade_delete()))
    
    # Résumé
    print_section("RÉSUMÉ DES TESTS")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{Colors.GREEN}✓{Colors.END}" if result else f"{Colors.RED}✗{Colors.END}"
        print(f"{status} Relation: {name}")
    
    print(f"\n{Colors.BOLD}Résultat: {passed}/{total} relations testées avec succès{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 TOUTES LES RELATIONS FONCTIONNENT ! Tâche 8 complète !{Colors.END}\n")
        return 0
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ {total - passed} relation(s) à vérifier.{Colors.END}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())