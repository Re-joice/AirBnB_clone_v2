#!/usr/bin/python3

import unittest

from models.state import State


class TestState(unittest.TestCase):
    """Test State."""

    def test_create(self):
        """Test State creation."""
        state = State()
        self.assertIsNotNone(state.id)

    def test_name(self):
        """Test name."""
        state = State(name="California")
        self.assertEqual(state.name, "California")

    def test_table_name(self):
        """Test table name."""
        self.assertEqual(State.__tablename__, "states")

    def test_to_dict(self):
        """Test to_dict."""
        state = State(name="Texas")
        data = state.to_dict()

        self.assertEqual(data["__class__"], "State")
        self.assertEqual(data["name"], "Texas")

    def test_id(self):
        """Test ID."""
        state = State()
        self.assertIsInstance(state.id, str)


if __name__ == "__main__":
    unittest.main()
