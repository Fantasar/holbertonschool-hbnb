import pytest
from app.models.place import Place
from app.models.user import User
import random


@pytest.fixture
def valid_user():
    """Fixture qui retourne un utilisateur valide"""
    unique_email = f"user{random.randint(1, 100000)}@example.com"
    return User(
        first_name="Jean",
        last_name="Dupont",
        email=unique_email,
        password="motdepasse123"
    )


class TestPlaceValidation:
    """Tests de validation des attributs de Place"""

    def test_title_not_empty(self, valid_user):
        """Test que le titre ne peut pas être vide"""
        with pytest.raises(ValueError) as exc_info:
            Place(
                title="",
                description="Desc",
                price=100,
                latitude=0,
                longitude=0,
                owner_id=valid_user.id
            )
        assert str(exc_info.value) == "Le titre du lieu ne peut pas être vide."

    def test_title_whitespace_only(self, valid_user):
        """Test que le titre ne peut pas contenir uniquement des espaces"""
        with pytest.raises(ValueError) as exc_info:
            Place(
                title="   ",
                description="Desc",
                price=100,
                latitude=0,
                longitude=0,
                owner_id=valid_user.id
            )
        assert str(exc_info.value) == "Le titre du lieu ne peut pas être vide."

    def test_title_too_long(self, valid_user):
        """Test que le titre ne dépasse pas 100 caractères"""
        with pytest.raises(ValueError) as exc_info:
            Place(
                title="T" * 101,
                description="Desc",
                price=100,
                latitude=0,
                longitude=0,
                owner_id=valid_user.id
            )
        assert str(
            exc_info.value) == "Le titre ne doit pas dépasser 100 caractères."

    def test_price_positive(self, valid_user):
        """Test que le prix doit être positif"""
        with pytest.raises(ValueError) as exc_info:
            Place(
                title="Titre",
                description="Desc",
                price=0,
                latitude=0,
                longitude=0,
                owner_id=valid_user.id
            )
        assert str(exc_info.value) == "Le prix doit être une valeur positive."

    def test_price_negative(self, valid_user):
        """Test qu'un prix négatif est rejeté"""
        with pytest.raises(ValueError):
            Place(
                title="Titre",
                description="Desc",
                price=-50,
                latitude=0,
                longitude=0,
                owner_id=valid_user.id
            )

    def test_price_not_number(self, valid_user):
        """Test que le prix doit être un nombre"""
        with pytest.raises(TypeError) as exc_info:
            Place(
                title="Titre",
                description="Desc",
                price="cent",
                latitude=0,
                longitude=0,
                owner_id=valid_user.id
            )
        assert str(exc_info.value) == "Le prix doit être un nombre."

    def test_latitude_min_range(self, valid_user):
        """Test que la latitude doit être >= -90"""
        with pytest.raises(ValueError):
            Place(
                title="Titre",
                description="Desc",
                price=100,
                latitude=-91,
                longitude=0,
                owner_id=valid_user.id
            )

    def test_latitude_max_range(self, valid_user):
        """Test que la latitude doit être <= 90"""
        with pytest.raises(ValueError):
            Place(
                title="Titre",
                description="Desc",
                price=100,
                latitude=91,
                longitude=0,
                owner_id=valid_user.id
            )

    def test_latitude_not_number(self, valid_user):
        """Test que la latitude doit être un nombre"""
        with pytest.raises(TypeError):
            Place(
                title="Titre",
                description="Desc",
                price=100,
                latitude="north",
                longitude=0,
                owner_id=valid_user.id
            )

    def test_longitude_min_range(self, valid_user):
        """Test que la longitude doit être >= -180"""
        with pytest.raises(ValueError):
            Place(
                title="Titre",
                description="Desc",
                price=100,
                latitude=0,
                longitude=-181,
                owner_id=valid_user.id
            )

    def test_longitude_max_range(self, valid_user):
        """Test que la longitude doit être <= 180"""
        with pytest.raises(ValueError):
            Place(
                title="Titre",
                description="Desc",
                price=100,
                latitude=0,
                longitude=181,
                owner_id=valid_user.id
            )

    def test_longitude_not_number(self, valid_user):
        """Test que la longitude doit être un nombre"""
        with pytest.raises(TypeError):
            Place(
                title="Titre",
                description="Desc",
                price=100,
                latitude=0,
                longitude="east",
                owner_id=valid_user.id
            )
