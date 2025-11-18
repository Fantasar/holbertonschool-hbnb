#!/usr/bin/env python3
"""
Script pour réinitialiser complètement la base de données
⚠️ ATTENTION : Supprime TOUTES les données !
"""

from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

def reset_database():
    """
    Supprime toutes les tables et les recrée à vide
    """
    print("=" * 70)
    print("⚠️  RESET DE LA BASE DE DONNÉES")
    print("=" * 70)
    print()
    
    # Demande de confirmation
    confirm = input("⚠️  Êtes-vous sûr de vouloir SUPPRIMER toutes les données ? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("❌ Opération annulée")
        return
    
    print()
    print("🗑️  Suppression de toutes les données en cours...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Compte les données avant suppression
            users_count = User.query.count()
            places_count = Place.query.count()
            amenities_count = Amenity.query.count()
            reviews_count = Review.query.count()
            
            print(f"   📊 Données actuelles:")
            print(f"      - {users_count} utilisateurs")
            print(f"      - {places_count} places")
            print(f"      - {amenities_count} équipements")
            print(f"      - {reviews_count} avis")
            print()
            
            # Supprime toutes les tables
            print("🔨 Suppression des tables...")
            db.drop_all()
            
            # Recrée les tables vides
            print("🏗️  Recréation des tables...")
            db.create_all()
            
            print()
            print("=" * 70)
            print("✅ Base de données réinitialisée avec succès !")
            print("=" * 70)
            print()
            print("💡 Vous pouvez maintenant lancer: python3 setup_test_data.py")
            
        except Exception as e:
            print(f"❌ Erreur lors du reset: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    reset_database()