#!/usr/bin/env python3
"""
Script de test pour valider les relations SQLAlchemy et les contraintes du projet HBnB Part 3.
Exécuter avec : python3 test_relations.py
"""
import requests
import json
import sys
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000/api/v1"
HEADERS = {"Content-Type": "application/json"}

# Couleurs pour l'affichage
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

# Variables pour stocker les IDs des tests
test_data = {
    'user_id': None,
    'place_id': None,
    'amenity_id': None,
    'review_id': None,
    'user_token': None,
    'admin_token': None
}

def setup_test_data():
    """Créer les données nécessaires pour les tests."""
    print_section("PRÉPARATION DES DONNÉES DE TEST")

    # 1. Créer un utilisateur normal
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": f"testuser_{datetime.now().timestamp()}@test.com",
        "password": "test123"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data, headers=HEADERS)
    if response.status_code == 201:
        test_data['user_id'] = response.json()['id']
        print_success(f"Utilisateur créé (ID: {test_data['user_id']})")
    else:
        print_error("Échec création utilisateur")
        return False

    # 2. Se connecter pour obtenir un token
    login_data = {"email": user_data['email'], "password": user_data['password']}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data, headers=HEADERS)
    if response.status_code == 200:
        test_data['user_token'] = response.json()['access_token']
        print_success("Token JWT obtenu")
    else:
        print_error("Échec login utilisateur")
        return False

    # 3. Créer un Place
    auth_header = {"Authorization": f"Bearer {test_data['user_token']}", "Content-Type": "application/json"}
    place_data = {
        "title": "Test Place",
        "description": "Test description",
        "price": 100.0,
        "latitude": 48.8566,
        "longitude": 2.3522
    }
    response = requests.post(f"{BASE_URL}/places/", json=place_data, headers=auth_header)
    if response.status_code == 201:
        test_data['place_id'] = response.json()['id']
        print_success(f"Place créé (ID: {test_data['place_id']})")
    else:
        print_error("Échec création Place")
        return False

    # 4. Créer un Amenity (en tant qu'admin)
    admin_data = {
        "first_name": "Admin",
        "last_name": "Test",
        "email": f"admin_{datetime.now().timestamp()}@test.com",
        "password": "admin123",
        "is_admin": True
    }
    response = requests.post(f"{BASE_URL}/users/", json=admin_data, headers=HEADERS)
    if response.status_code != 201:
        print_error("Échec création admin")
        return False

    admin_login = {"email": admin_data['email'], "password": admin_data['password']}
    response = requests.post(f"{BASE_URL}/auth/login", json=admin_login, headers=HEADERS)
    if response.status_code != 200:
        print_error("Échec login admin")
        return False
    test_data['admin_token'] = response.json()['access_token']

    admin_header = {"Authorization": f"Bearer {test_data['admin_token']}", "Content-Type": "application/json"}
    amenity_data = {"name": "Test Amenity"}
    response = requests.post(f"{BASE_URL}/admin/amenities/", json=amenity_data, headers=admin_header)
    if response.status_code == 201:
        test_data['amenity_id'] = response.json()['id']
        print_success(f"Amenity créé (ID: {test_data['amenity_id']})")
    else:
        print_error("Échec création Amenity")
        return False

    # 5. Créer une Review
    review_data = {
        "text": "Test review",
        "rating": 5,
        "place_id": test_data['place_id']
    }
    response = requests.post(f"{BASE_URL}/reviews/", json=review_data, headers=admin_header)
    if response.status_code == 201:
        test_data['review_id'] = response.json()['id']
        print_success(f"Review créée (ID: {test_data['review_id']})")
    else:
        print_error("Échec création Review")
        return False

    return True

def test_user_places_relation():
    """Test: Vérifier la relation User ↔ Places (1-N)"""
    print_test("Relation User ↔ Places (un-à-plusieurs)")
    response = requests.get(f"{BASE_URL}/users/{test_data['user_id']}")
    if response.status_code == 200:
        user_data = response.json()
        if 'places' in user_data and isinstance(user_data['places'], list):
            print_success("Relation User ↔ Places validée (1 utilisateur → N places)")
            return True
    print_error("Échec validation relation User ↔ Places")
    return False

def test_place_amenities_relation():
    """Test: Vérifier la relation Place ↔ Amenities (N-N)"""
    print_test("Relation Place ↔ Amenities (plusieurs-à-plusieurs)")

    # 1. Associer un Amenity à un Place
    auth_header = {"Authorization": f"Bearer {test_data['user_token']}", "Content-Type": "application/json"}
    response = requests.post(
        f"{BASE_URL}/places/{test_data['place_id']}/amenities",
        json=[test_data['amenity_id']],
        headers=auth_header
    )
    if response.status_code != 200:
        print_error("Échec association Amenity → Place")
        return False

    # 2. Vérifier que l'Amenity est bien associé au Place
    response = requests.get(f"{BASE_URL}/places/{test_data['place_id']}")
    if response.status_code == 200:
        place_data = response.json()
        if 'amenities' in place_data and isinstance(place_data['amenities'], list):
            if any(amenity['id'] == test_data['amenity_id'] for amenity in place_data['amenities']):
                print_success("Relation Place ↔ Amenities validée (N-N)")
                return True

    print_error("Échec validation relation Place ↔ Amenities")
    return False

def test_place_reviews_relation():
    """Test: Vérifier la relation Place ↔ Reviews (1-N)"""
    print_test("Relation Place ↔ Reviews (un-à-plusieurs)")
    response = requests.get(f"{BASE_URL}/places/{test_data['place_id']}/reviews/")
    if response.status_code == 200:
        reviews = response.json()
        if isinstance(reviews, list) and len(reviews) >= 1:
            print_success("Relation Place ↔ Reviews validée (1 place → N reviews)")
            return True
    print_error("Échec validation relation Place ↔ Reviews")
    return False

def test_cascade_delete():
    """Test: Vérifier la cascade delete (suppression d'un Place supprime ses Reviews)"""
    print_test("Cascade delete (Place → Reviews)")

    # 1. Créer un nouveau Place et une Review associée
    auth_header = {"Authorization": f"Bearer {test_data['user_token']}", "Content-Type": "application/json"}
    new_place_data = {
        "title": "Temp Place",
        "description": "Temp",
        "price": 50.0,
        "latitude": 0.0,
        "longitude": 0.0
    }
    place_response = requests.post(f"{BASE_URL}/places/", json=new_place_data, headers=auth_header)
    if place_response.status_code != 201:
        print_error("Échec création Place temporaire")
        return False
    temp_place_id = place_response.json()['id']

    # 2. Créer une Review pour ce Place
    review_data = {"text": "Temp review", "rating": 3, "place_id": temp_place_id}
    review_response = requests.post(f"{BASE_URL}/reviews/", json=review_data, headers=auth_header)
    if review_response.status_code != 201:
        print_error("Échec création Review temporaire")
        return False
    temp_review_id = review_response.json()['id']

    # 3. Supprimer le Place
    delete_response = requests.delete(f"{BASE_URL}/places/{temp_place_id}", headers=auth_header)
    if delete_response.status_code != 200:
        print_error("Échec suppression Place temporaire")
        return False

    # 4. Vérifier que la Review a été supprimée
    review_check = requests.get(f"{BASE_URL}/reviews/")
    if review_check.status_code == 200:
        reviews = review_check.json()
        if not any(review['id'] == temp_review_id for review in reviews):
            print_success("Cascade delete validée (Place → Reviews)")
            return True

    print_error("Échec validation cascade delete")
    return False

def test_required_fields():
    """Test: Vérifier que les champs requis sont validés"""
    print_test("Validation des champs requis (nullable=False)")
    auth_header = {"Authorization": f"Bearer {test_data['user_token']}", "Content-Type": "application/json"}

    # Essayer de créer un Place sans title (nullable=False)
    invalid_place_data = {
        "description": "No title",
        "price": 50.0,
        "latitude": 0.0,
        "longitude": 0.0
    }
    response = requests.post(f"{BASE_URL}/places/", json=invalid_place_data, headers=auth_header)
    if response.status_code == 400:
        print_success("Validation des champs requis fonctionnelle (title est obligatoire)")
        return True

    print_error("Échec validation des champs requis")
    return False

def test_unique_constraints():
    """Test: Vérifier les contraintes d'unicité (ex: email)"""
    print_test("Contraintes d'unicité (ex: email)")
    duplicate_user_data = {
        "first_name": "Duplicate",
        "last_name": "User",
        "email": f"testuser_{datetime.now().timestamp()}@test.com",  # Même email que test_data['user_id']
        "password": "test123"
    }
    response = requests.post(f"{BASE_URL}/users/", json=duplicate_user_data, headers=HEADERS)
    if response.status_code == 400:  # Doit échouer car email déjà utilisé
        print_success("Contrainte d'unicité validée (email)")
        return True

    print_error("Échec validation contrainte d'unicité")
    return False

def test_performance():
    """Test: Mesurer le temps de réponse pour les requêtes complexes"""
    print_test("Performance des requêtes")
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/places/")
    end_time = time.time()

    if response.status_code == 200:
        elapsed = end_time - start_time
        print_success(f"Requête GET /places/ exécutée en {elapsed:.3f} secondes")
        if elapsed < 1.0:
            return True

    print_error("Requête trop lente ou échouée")
    return False

def main():
    """Fonction principale"""
    print(f"\n{Colors.BOLD}{'='*70}")
    print(f"  TEST DES RELATIONS SQLALCHEMY - HBNB PART 3")
    print(f"{'='*70}{Colors.END}\n")

    # 1. Préparer les données de test
    if not setup_test_data():
        print_error("\n❌ Échec de la préparation des données. Arrêt des tests.")
        return 1

    # 2. Exécuter les tests
    results = []
    results.append(("User ↔ Places", test_user_places_relation()))
    results.append(("Place ↔ Amenities", test_place_amenities_relation()))
    results.append(("Place ↔ Reviews", test_place_reviews_relation()))
    results.append(("Cascade delete", test_cascade_delete()))
    results.append(("Champs requis", test_required_fields()))
    results.append(("Contraintes uniques", test_unique_constraints()))
    results.append(("Performance", test_performance()))

    # 3. Résumé
    print_section("RÉSUMÉ DES TESTS")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = f"{Colors.GREEN}✓{Colors.END}" if result else f"{Colors.RED}✗{Colors.END}"
        print(f"{status} {name}")

    print(f"\n{Colors.BOLD}Résultat: {passed}/{total} tests réussis{Colors.END}")

    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 TOUS LES TESTS DE RELATIONS SONT PASSÉS !{Colors.END}\n")
        print_warning("Votre implémentation SQLAlchemy est validée !")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ {total - passed} test(s) en échec.{Colors.END}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
