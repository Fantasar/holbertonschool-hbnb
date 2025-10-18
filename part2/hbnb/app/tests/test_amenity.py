import pytest
from app.models.amenity import Amenity


class TestAmenityCreation:
    """Tests pour la création et validation des amenities"""

    def test_create_valid_amenity(self):
        """Test de création d'une amenity valide"""
        amenity = Amenity(name="WiFi")
        assert amenity.name == "WiFi"
        assert amenity.id is not None
        assert amenity.created_at is not None
        assert amenity.updated_at is not None

    def test_name_empty(self):
        """Test que le nom ne peut pas être vide"""
        with pytest.raises(TypeError) as exc_info:
            Amenity(name="")
        assert str(exc_info.value) == "il faut indiquer le nom de l'équipement"

    def test_name_too_long(self):
        """Test que le nom ne dépasse pas 50 caractères"""
        with pytest.raises(TypeError) as exc_info:
            Amenity(name="N" * 51)
        assert str(
            exc_info.value) == "Le nom de l'équipement ne peut pas dépasser 50 caractères."

    def test_name_not_string(self):
        """Test que le nom doit être une chaîne de caractères"""
        with pytest.raises(TypeError) as exc_info:
            Amenity(name=123)
        assert str(
            exc_info.value) == "L'équipement doit être une chaine de caractères"

    def test_name_whitespace_only(self):
        """Test qu'un nom avec uniquement des espaces est
            accepté (comportement actuel)
        """
        # Le modèle actuel accepte les espaces
        amenity = Amenity(name="   ")
        assert amenity.name == "   "


class TestAmenityEdgeCases:
    """Tests des cas limites pour Amenity"""

    def test_name_exactly_50_chars(self):
        """Test qu'un nom de 50 caractères est accepté"""
        name = "N" * 50
        amenity = Amenity(name=name)
        assert amenity.name == name

    def test_name_with_spaces(self):
        """Test qu'un nom avec espaces est accepté sans être trimé"""
        amenity = Amenity(name="  WiFi Gratuit  ")
        # Le modèle actuel ne trim pas les espaces
        assert amenity.name == "  WiFi Gratuit  "

    def test_name_special_characters(self):
        """Test qu'un nom avec caractères spéciaux est accepté"""
        amenity = Amenity(name="Télévision 4K")
        assert amenity.name == "Télévision 4K"


# Fixtures
@pytest.fixture
def valid_amenity():
    """Fixture qui retourne une amenity valide"""
    return Amenity(name="Piscine")


@pytest.fixture
def multiple_amenities():
    """Fixture qui retourne plusieurs amenities"""
    return [
        Amenity(name="WiFi"),
        Amenity(name="Parking"),
        Amenity(name="Climatisation")
    ]


class TestAmenityWithFixtures:
    """Tests utilisant les fixtures"""

    def test_amenity_fixture(self, valid_amenity):
        """Test utilisant la fixture valid_amenity"""
        assert valid_amenity.name == "Piscine"
        assert hasattr(valid_amenity, 'id')

    def test_multiple_amenities_fixture(self, multiple_amenities):
        """Test utilisant la fixture multiple_amenities"""
        assert len(multiple_amenities) == 3
        assert multiple_amenities[0].name == "WiFi"
        assert all(hasattr(a, 'id') for a in multiple_amenities)


# Tests paramétrés pour noms valides
@pytest.mark.parametrize("name", [
    "WiFi",
    "  Piscine  ",  # Les espaces ne sont pas trimés
    "Télévision",
    "A" * 50,
])
def test_valid_names(name):
    """Test de plusieurs noms valides avec paramétrage"""
    amenity = Amenity(name=name)
    assert amenity.name == name


# Tests paramétrés pour noms invalides (chaîne vide et trop long)
@pytest.mark.parametrize("invalid_name,expected_error", [
    ("", "il faut indiquer le nom de l'équipement"),
    ("N" * 51, "Le nom de l'équipement ne peut pas dépasser 50 caractères."),
])
def test_invalid_names(invalid_name, expected_error):
    """Test de plusieurs noms invalides avec paramétrage"""
    with pytest.raises(TypeError) as exc_info:
        Amenity(name=invalid_name)
    assert str(exc_info.value) == expected_error


# Tests paramétrés pour types invalides
@pytest.mark.parametrize("invalid_type", [
    123,
    12.5,
    None,
    [],
    {},
])
def test_invalid_types(invalid_type):
    """Test de plusieurs types invalides avec paramétrage"""
    with pytest.raises(TypeError):
        Amenity(name=invalid_type)
