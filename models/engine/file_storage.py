#!/usr/bin/python3

import json


class FileStorage:
    """Serialize instances to a JSON file and deserialize them."""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return all objects, optionally filtered by class."""
        if cls is None:
            return FileStorage.__objects

        return {
            key: obj
            for key, obj in FileStorage.__objects.items()
            if isinstance(obj, cls)
        }

    def new(self, obj):
        """Add an object to storage."""
        key = "{}.{}".format(
            obj.__class__.__name__,
            obj.id
        )
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize objects to the JSON file."""
        objects_dict = {}

        for key, obj in FileStorage.__objects.items():
            objects_dict[key] = obj.to_dict()

        with open(FileStorage.__file_path, "w") as file:
            json.dump(objects_dict, file)

    def delete(self, obj=None):
        """Delete an object from storage."""
        if obj is None:
            return

        key = "{}.{}".format(
            obj.__class__.__name__,
            obj.id
        )

        if key in FileStorage.__objects:
            del FileStorage.__objects[key]

    def reload(self):
        """Deserialize the JSON file."""
        try:
            with open(FileStorage.__file_path, "r") as file:
                objects = json.load(file)

            from models.base_model import BaseModel
            from models.state import State
            from models.place import Place

            classes = {
                "BaseModel": BaseModel,
                "State": State,
                "Place": Place
            }

            for key, value in objects.items():
                class_name = value["__class__"]
                if class_name in classes:
                    FileStorage.__objects[key] = classes[class_name](**value)
        except FileNotFoundError:
            pass
