from app.extensions import db

# Définition d'une table d'association Many-to-Many entre les tables "places" et "amenities"
# Cette table ne représente pas un modèle avec des données propres,
# mais simplement la liaison entre les identifiants de lieux et d'équipements.

place_amenity = db.Table( # Nom de la table d'association en base de données
    'place_amenity',

    # Colonne 'place_id' : clé étrangère vers la table 'places' (colonne 'id')
    # Ce champ est aussi une des clés primaires pour garantir l'unicité.
    db.Column(
        'place_id',
        db.String(36),
        db.ForeignKey('places.id'),
        primary_key=True
    ),

    # Colonne 'amenity_id' : clé étrangère vers la table 'amenities' (colonne 'id')
    # Clé primaire pour garantir l'unicité de la combinaison place-amenity.
    db.Column(
        'amenity_id',
        db.String(36),
        db.ForeignKey('amenities.id'),
        primary_key=True
    )
)