#!/usr/bin/env python3
"""
Script pour peupler la base de données avec les 5 places initiales
Utilise les données du HTML original avec les images correspondantes
"""

import requests
import json

# Configuration
API_BASE_URL = "http://localhost:5000/api/v1"
LOGIN_ENDPOINT = f"{API_BASE_URL}/auth/login"
PLACES_ENDPOINT = f"{API_BASE_URL}/places/"

# Identifiants de connexion (à adapter selon ton utilisateur)
USER_EMAIL = "test@hbnb.com"
USER_PASSWORD = "Test1234!"

# Données des 5 places à créer (extraites de ton HTML)
PLACES_DATA = [
    {
        "title": "Appartement à Arcachon",
        "description": "Charmant appartement près du port, pour ballade et moment de détente.",
        "price": 90.0,
        "latitude": 44.6534,
        "longitude": -1.1659,
        "image_url": "images/arcachon.jpg"
    },
    {
        "title": "Maison à Bordeaux",
        "description": "Maison située dans quartier calme près des commerces, place de parking privée",
        "price": 105.0,
        "latitude": 44.8378,
        "longitude": -0.5792,
        "image_url": "images/bordeaux.avif"
    },
    {
        "title": "Maison à Agen",
        "description": "Maison près du centre et de l'église, ballade et randonnées et barbecue",
        "price": 60.0,
        "latitude": 44.2034,
        "longitude": 0.6164,
        "image_url": "images/agen.jpg"
    },
    {
        "title": "Appartement à La Rochelle",
        "description": "Charmant appartement près du vieux port, possédant un balcon, proche de tous les commerces.",
        "price": 75.0,
        "latitude": 46.1591,
        "longitude": -1.1520,
        "image_url": "images/la_rochelle.jpg"
    },
    {
        "title": "Appartement à Limoges",
        "description": "Appartement calme, situé en centre ville, avec la ligne de bus à proximité.",
        "price": 65.0,
        "latitude": 45.8336,
        "longitude": 1.2611,
        "image_url": "images/limoges.jpg"
    }
]


def login():
    """
    Se connecter à l'API et récupérer le token JWT
    """
    print("🔐 Connexion à l'API...")
    
    response = requests.post(
        LOGIN_ENDPOINT,
        json={
            "email": USER_EMAIL,
            "password": USER_PASSWORD
        },
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        print(f"✅ Connexion réussie ! Token obtenu.")
        return token
    else:
        print(f"❌ Échec de connexion: {response.status_code}")
        print(f"   Réponse: {response.text}")
        return None


def create_place(token, place_data):
    """
    Créer une place dans l'API
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.post(
        PLACES_ENDPOINT,
        json=place_data,
        headers=headers
    )
    
    if response.status_code == 201:
        created_place = response.json()
        print(f"✅ Place créée: {place_data['title']} (ID: {created_place.get('id', 'N/A')})")
        return True
    else:
        print(f"❌ Échec création de '{place_data['title']}'")
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.text}")
        return False


def get_existing_places(token):
    """
    Récupérer la liste des places existantes
    """
    headers = {
        "Authorization": f"Bearer {token}"
    } if token else {}
    
    response = requests.get(PLACES_ENDPOINT, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    return []


def main():
    """
    Fonction principale
    """
    print("=" * 60)
    print("🏠 Script de peuplement de la base de données HBNB")
    print("=" * 60)
    print()
    
    # Étape 1 : Connexion
    token = login()
    if not token:
        print("\n❌ Impossible de continuer sans token.")
        print("💡 Vérifiez vos identifiants dans le script :")
        print(f"   USER_EMAIL = '{USER_EMAIL}'")
        print(f"   USER_PASSWORD = '{USER_PASSWORD}'")
        return
    
    print()
    
    # Étape 2 : Vérifier les places existantes
    print("📋 Vérification des places existantes...")
    existing_places = get_existing_places(token)
    print(f"   {len(existing_places)} place(s) déjà en base")
    print()
    
    # Étape 3 : Créer les places
    print("🏗️  Création des 5 places...")
    print()
    
    success_count = 0
    for i, place_data in enumerate(PLACES_DATA, 1):
        print(f"[{i}/5] Création de: {place_data['title']}")
        if create_place(token, place_data):
            success_count += 1
        print()
    
    # Résumé
    print("=" * 60)
    print(f"✨ Résultat: {success_count}/{len(PLACES_DATA)} places créées avec succès")
    print("=" * 60)
    print()
    
    # Vérification finale
    print("🔍 Vérification finale...")
    final_places = get_existing_places(token)
    print(f"   Total de places en base: {len(final_places)}")
    print()
    
    # Afficher les places créées
    if final_places:
        print("📍 Places disponibles:")
        for place in final_places:
            print(f"   • {place.get('title', 'N/A')} - {place.get('price', 0)}€/nuit")
    
    print()
    print("✅ Script terminé !")
    print("💡 Tu peux maintenant recharger ton site web pour voir les places.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Script interrompu par l'utilisateur")
    except requests.exceptions.ConnectionError:
        print("\n\n❌ Erreur: Impossible de se connecter à l'API")
        print("💡 Vérifie que ton serveur Flask est bien démarré sur le port 5000")
    except Exception as e:
        print(f"\n\n❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
