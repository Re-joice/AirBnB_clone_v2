#!/usr/bin/python3

import unittest

from models.review import Review


class TestReview(unittest.TestCase):
    """Test Review."""

    def test_create(self):
        """Test Review creation."""
        review = Review()
        self.assertIsNotNone(review.id)

    def test_place_id(self):
        """Test place ID."""
        review = Review(place_id="place-123")
        self.assertEqual(review.place_id, "place-123")

    def test_user_id(self):
        """Test user ID."""
        review = Review(user_id="user-123")
        self.assertEqual(review.user_id, "user-123")

    def test_text(self):
        """Test text."""
        review = Review(text="Great place!")
        self.assertEqual(review.text, "Great place!")

    def test_table_name(self):
        """Test table name."""
        self.assertEqual(Review.__tablename__, "reviews")

    def test_to_dict(self):
        """Test to_dict."""
        review = Review(
            place_id="place-1",
            user_id="user-1",
            text="Excellent"
        )

        data = review.to_dict()

        self.assertEqual(data["__class__"], "Review")
        self.assertEqual(data["text"], "Excellent")

    def test_id(self):
        """Test ID."""
        review = Review()
        self.assertIsInstance(review.id, str)


if __name__ == "__main__":
    unittest.main()
