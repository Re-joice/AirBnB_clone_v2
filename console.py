#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    # All valid classes supported by the console
    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }

    def do_quit(self, command):
        """ Exit the application """
        return True

    def help_quit(self):
        """ Documentation for the quit command """
        print("Exits the application")

    def do_EOF(self, command):
        """ Exit the application on EOF """
        print()
        return True

    def emptyline(self):
        """ Overrides the emptyline method to do nothing """
        pass

    def do_create(self, args):
        """ Create an object of any class with parameters """
        if not args:
            print("** class name missing **")
            return
        
        args_list = args.split()
        class_name = args_list[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        new_instance = self.classes[class_name]()

        # Handle key=value parameters for DBStorage/FileStorage creation
        for param in args_list[1:]:
            if '=' in param:
                key, value = param.split('=', 1)
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1].replace('_', ' ').replace('\\"', '"')
                elif '.' in value:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        pass
                
                setattr(new_instance, key, value)

        new_instance.save()
        print(new_instance.id)

    def do_show(self, args):
        """ Print an instance based on the class name and id """
        new = args.split()
        if not new:
            print("** class name missing **")
            return
        if new[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(new) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(new[0], new[1])
        if key not in storage.all():
            print("** no instance found **")
        else:
            print(storage.all()[key])

    def do_destroy(self, args):
        """ Deletes an instance based on the class name and id """
        new = args.split()
        if not new:
            print("** class name missing **")
            return
        if new[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(new) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(new[0], new[1])
        if key not in storage.all():
            print("** no instance found **")
        else:
            del storage.all()[key]
            storage.save()

    def do_all(self, args):
        """ Prints all string representation of all instances """
        new = args.split()
        obj_list = []
        if len(new) > 0 and new[0] not in self.classes:
            print("** class doesn't exist **")
            return
        
        for k, v in storage.all().items():
            if len(new) > 0 and new[0] == k.split('.')[0]:
                obj_list.append(str(v))
            elif len(new) == 0:
                obj_list.append(str(v))
        print(obj_list)

    def do_update(self, args):
        """ Updates an instance by adding or updating attribute """
        args_list = args.split()
        if not args_list:
            print("** class name missing **")
            return
        if args_list[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args_list) < 2:
            print("** instance id missing **")
            return
        
        key = "{}.{}".format(args_list[0], args_list[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        
        if len(args_list) < 3:
            print("** attribute name missing **")
            return
        if len(args_list) < 4:
            print("** value missing **")
            return

        obj = storage.all()[key]
        attr_name = args_list[2]
        attr_value = args_list[3].strip('"')

        if hasattr(obj, attr_name):
            attr_type = type(getattr(obj, attr_name))
            try:
                attr_value = attr_type(attr_value)
            except ValueError:
                pass

        setattr(obj, attr_name, attr_value)
        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
