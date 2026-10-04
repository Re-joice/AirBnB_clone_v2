#!/usr/bin/python3

import os
import unittest

from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """Test FileStorage."""

    def setUp(self):
        """Set up tests."""
        self.storage = FileStorage()
        self.file_path = self.storage._FileStorage__file_path

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def tearDown(self):
        """Clean up."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_instance(self):
        """Test FileStorage instance."""
        self.assertIsInstance(self.storage, FileStorage)

    def test_all(self):
        """Test all."""
        obj = BaseModel()
        self.storage.new(obj)
        objects = self.storage.all()

        key = "BaseModel.{}".format(obj.id)
        self.assertIn(key, objects)

    def test_new(self):
        """Test new."""
        obj = BaseModel()
        self.storage.new(obj)

        key = "BaseModel.{}".format(obj.id)
        self.assertIn(key, self.storage.all())

    def test_save(self):
        """Test save."""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()

        self.assertTrue(os.path.exists(self.file_path))

    def test_reload(self):
        """Test reload."""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()

        new_storage = FileStorage()
        new_storage.reload()

        key = "BaseModel.{}".format(obj.id)
        self.assertIn(key, new_storage.all())

    def test_delete(self):
        """Test delete."""
        obj = BaseModel()
        self.storage.new(obj)

        key = "BaseModel.{}".format(obj.id)
        self.assertIn(key, self.storage.all())

        self.storage.delete(obj)

        self.assertNotIn(key, self.storage.all())


if __name__ == "__main__":
    unittest.main()
