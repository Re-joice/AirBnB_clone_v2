#!/usr/bin/python3

import cmd
import shlex

from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place


class HBNBCommand(cmd.Cmd):
    """Command interpreter for the AirBnB project."""

    prompt = "(hbnb) "

    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Place": Place
    }

    def do_quit(self, arg):
        """Quit the command interpreter."""
        return True

    def do_EOF(self, arg):
        """Handle EOF."""
        print()
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered."""
        pass

    def do_create(self, arg):
        """Create a new instance with optional parameters."""
        if not arg:
            print("** class name missing **")
            return

        try:
            tokens = shlex.split(arg, posix=False)
        except ValueError:
            return

        if not tokens:
            print("** class name missing **")
            return

        class_name = tokens[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        params = {}

        for token in tokens[1:]:
            if "=" not in token:
                continue

            key, value = token.split("=", 1)

            if not key or not value:
                continue

            if value.startswith('"'):
                if not value.endswith('"') or len(value) < 2:
                    continue

                value = value[1:-1]
                value = value.replace('\\"', '"')
                value = value.replace("_", " ")
                params[key] = value

            elif "." in value:
                try:
                    params[key] = float(value)
                except ValueError:
                    continue

            else:
                try:
                    params[key] = int(value)
                except ValueError:
                    continue

        instance = self.classes[class_name](**params)
        instance.save()
        print(instance.id)

    def do_show(self, arg):
        """Show an object."""
        args = arg.split()

        if not args:
            print("** class name missing **")
            return

        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        key = "{}.{}".format(args[0], args[1])
        obj = storage.all().get(key)

        if obj is None:
            print("** no instance found **")
            return

        print(obj)

    def do_all(self, arg):
        """Show all objects or all objects of a class."""
        if arg and arg not in self.classes:
            print("** class doesn't exist **")
            return

        if arg:
            objects = storage.all(self.classes[arg])
        else:
            objects = storage.all()

        print([str(obj) for obj in objects.values()])


if __name__ == "__main__":
    storage.reload()
    HBNBCommand().cmdloop()
