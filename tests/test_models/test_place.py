#!/usr/bin/python3

import unittest

from models.place import Place


class TestPlace(unittest.TestCase):
    """Test Place."""

    def test_create(self):
        """Test Place creation."""
        place = Place()
        self.assertIsNotNone(place.id)

    def test_name(self):
        """Test name."""
        place = Place(name="My Place")
        self.assertEqual(place.name, "My Place")

    def test_city_id(self):
        """Test city ID."""
        place = Place(city_id="city-123")
        self.assertEqual(place.city_id, "city-123")

    def test_user_id(self):
        """Test user ID."""
        place = Place(user_id="user-123")
        self.assertEqual(place.user_id, "user-123")

    def test_price(self):
        """Test price."""
        place = Place(price_by_night=100)
        self.assertEqual(place.price_by_night, 100)

    def test_rooms(self):
        """Test rooms."""
        place = Place(number_rooms=3)
        self.assertEqual(place.number_rooms, 3)

    def test_bathrooms(self):
        """Test bathrooms."""
        place = Place(number_bathrooms=2)
        self.assertEqual(place.number_bathrooms, 2)

    def test_guests(self):
        """Test guests."""
        place = Place(max_guest=5)
        self.assertEqual(place.max_guest, 5)

    def test_table_name(self):
        """Test table name."""
        self.assertEqual(Place.__tablename__, "places")

    def test_to_dict(self):
        """Test to_dict."""
        place = Place(name="House")
        data = place.to_dict()

        self.assertEqual(data["__class__"], "Place")
        self.assertEqual(data["name"], "House")


if __name__ == "__main__":
    unittest.main()
