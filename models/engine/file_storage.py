#!/usr/bin/python3

import json


class FileStorage:
    """Serialize instances to a JSON file and deserialize them."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return all objects."""
        return FileStorage.__objects

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
