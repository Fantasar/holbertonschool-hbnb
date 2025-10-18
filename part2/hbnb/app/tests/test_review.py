import pytest
from app.models.review import Review


class TestReviewValidation:
    """Tests de validation des attributs de Review - Sans dépendances Place"""

    def test_text_not_empty_simple(self):
        """Test que le texte ne peut pas être vide"""
        # Test sans créer de Place pour éviter le bug de place.py
        with pytest.raises(ValueError) as exc_info:
            Review(user=None, place=None, text="", rating=3)
        assert str(exc_info.value) == "Le texte de l'avis ne peut pas être vide."

    def test_text_whitespace_only(self):
        """Test que le texte ne peut pas contenir uniquement des espaces"""
        with pytest.raises(ValueError):
            Review(user=None, place=None, text="   ", rating=3)

    def test_rating_minimum(self):
        """Test que la note doit être >= 1"""
        with pytest.raises(ValueError):
            Review(user=None, place=None, text="Bien", rating=0)

    def test_rating_maximum(self):
        """Test que la note doit être <= 5"""
        with pytest.raises(ValueError):
            Review(user=None, place=None, text="Bien", rating=6)

    def test_rating_negative(self):
        """Test qu'une note négative est rejetée"""
        with pytest.raises(ValueError):
            Review(user=None, place=None, text="Bien", rating=-1)

    def test_rating_not_integer(self):
        """Test que la note doit être un entier"""
        with pytest.raises(TypeError):
            Review(user=None, place=None, text="Bien", rating="excellent")

    def test_rating_not_integer_float(self):
        """Test qu'un float n'est pas accepté pour rating"""
        with pytest.raises(TypeError):
            Review(user=None, place=None, text="Bien", rating=3.5)
