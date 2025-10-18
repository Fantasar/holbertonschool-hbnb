import unittest
from app.models.user import User


class TestUserCreation(unittest.TestCase):

    def setUp(self):
        """Réinitialiser les emails existants avant chaque test"""
        User._User__existing_emails = set()

    # -----------------------------
    # Test création valide
    def test_create_valid_user(self):
        user = User(
            last_name="Dupont",
            first_name="Jean",
            email="jean.dupont@example.com",
            password="motdepasse123"
        )
        self.assertEqual(user.first_name, "Jean")
        self.assertEqual(user.last_name, "Dupont")
        self.assertEqual(user.email, "jean.dupont@example.com")
        self.assertTrue(user.password)  # Vérifie que le mot de passe est hashé

    # -----------------------------
    # Test prénom vide
    def test_first_name_empty(self):
        with self.assertRaises(TypeError) as context:
            User(
                last_name="Dupont",
                first_name="",
                email="john@example.com",
                password="motdepasse123"
            )
        self.assertEqual(str(context.exception), "un prenom est obligatoire")

    # Test prénom > 50 caractères
    def test_first_name_too_long(self):
        with self.assertRaises(TypeError) as context:
            User(
                last_name="Dupont",
                first_name="J" * 51,
                email="john2@example.com",
                password="motdepasse123"
            )
        self.assertEqual(str(context.exception),
                         "le prenom doit contenir moins de 50 caractéres")

    # -----------------------------
    # Test nom vide
    def test_last_name_empty(self):
        with self.assertRaises(TypeError) as context:
            User(
                last_name="",
                first_name="John",
                email="john@example.com",
                password="motdepasse123"
            )
        self.assertEqual(str(context.exception), "un nom est obligatoire")

    # Test nom > 50 caractères
    def test_last_name_too_long(self):
        with self.assertRaises(TypeError) as context:
            User(
                last_name="D" * 51,
                first_name="John",
                email="john2@example.com",
                password="motdepasse123"
            )
        self.assertEqual(str(context.exception),
                         "le nom doit contenir moins de 50 caractères")

    # -----------------------------
    # Test email vide ou invalide
    def test_invalid_email_format(self):
        with self.assertRaises(ValueError):
            User(
                last_name="Dupont",
                first_name="John",
                email="",
                password="motdepasse123"
            )
        with self.assertRaises(ValueError):
            User(
                last_name="Dupont",
                first_name="John",
                email="invalid-email",
                password="motdepasse123"
            )

    # Test email unique
    def test_email_unique(self):
        User(last_name="Dupont", first_name="John",
             email="unique@example.com", password="motdepasse123")
        with self.assertRaises(ValueError) as context:
            User(last_name="Durand", first_name="Alice",
                 email="unique@example.com", password="motdepasse456")
        self.assertEqual(str(context.exception), "Cet email est déjà utilisé.")

    # -----------------------------
    # Test mot de passe trop court
    def test_password_too_short(self):
        with self.assertRaises(ValueError) as context:
            User(
                last_name="Dupont",
                first_name="John",
                email="john2@example.com",
                password="123"
            )
        self.assertEqual(str(context.exception),
                         "Le mot de passe doit contenir au moins 6 caractères.")


if __name__ == "__main__":
    unittest.main()
