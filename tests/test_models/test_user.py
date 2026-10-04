#!/usr/bin/python3

import unittest

from models.user import User


class TestUser(unittest.TestCase):
    """Test User."""

    def test_create(self):
        """Test User creation."""
        user = User()
        self.assertIsNotNone(user.id)

    def test_email(self):
        """Test email."""
        user = User(email="test@example.com")
        self.assertEqual(user.email, "test@example.com")

    def test_password(self):
        """Test password."""
        user = User(password="password")
        self.assertEqual(user.password, "password")

    def test_first_name(self):
        """Test first name."""
        user = User(first_name="John")
        self.assertEqual(user.first_name, "John")

    def test_last_name(self):
        """Test last name."""
        user = User(last_name="Doe")
        self.assertEqual(user.last_name, "Doe")

    def test_table_name(self):
        """Test table name."""
        self.assertEqual(User.__tablename__, "users")

    def test_to_dict(self):
        """Test to_dict."""
        user = User(email="test@example.com")
        data = user.to_dict()

        self.assertEqual(data["__class__"], "User")
        self.assertEqual(data["email"], "test@example.com")


if __name__ == "__main__":
    unittest.main()
