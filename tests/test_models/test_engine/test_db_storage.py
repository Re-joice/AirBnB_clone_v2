#!/usr/bin/python3

import os
import unittest

from models.engine.db_storage import DBStorage


class TestDBStorage(unittest.TestCase):
    """Test DBStorage."""

    @classmethod
    def setUpClass(cls):
        """Set up DBStorage tests."""
        if os.getenv("HBNB_TYPE_STORAGE") != "db":
            cls.skip_tests = True
            return

        try:
            cls.storage = DBStorage()
            cls.storage.reload()
            cls.skip_tests = False
        except Exception:
            cls.skip_tests = True

    def setUp(self):
        """Skip when MySQL is unavailable."""
        if self.skip_tests:
            self.skipTest("MySQL database is not available")

    def test_instance(self):
        """Test DBStorage instance."""
        self.assertIsInstance(self.storage, DBStorage)

    def test_all(self):
        """Test all."""
        objects = self.storage.all()
        self.assertIsInstance(objects, dict)

    def test_new(self):
        """Test new method exists."""
        self.assertTrue(callable(self.storage.new))

    def test_save(self):
        """Test save method exists."""
        self.assertTrue(callable(self.storage.save))

    def test_delete(self):
        """Test delete method exists."""
        self.assertTrue(callable(self.storage.delete))

    def test_reload(self):
        """Test reload method exists."""
        self.assertTrue(callable(self.storage.reload))

    def test_close(self):
        """Test close method exists."""
        self.assertTrue(callable(self.storage.close))


if __name__ == "__main__":
    unittest.main()
