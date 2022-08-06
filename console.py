#!/usr/bin/python3
""" Module for HBNB CLI class
"""
import cmd
import sys
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.engine.file_storage import FileStorage
from models.__init__ import storage


class HBNBCommand(cmd.Cmd):
    """ CLI for HBNB
    """

    " ----- CLI basic functionality ----- "

    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """ Handles EOF
        """
        return True

    def do_quit(self, arg):
        """ [quit + ENTER]: cmd exits the CLI
        """
        return True

    def emptyline(self):
        """ Handles [empty line + ENTER]
        """
        pass

    def default(self, arg):
        """ Overrides default unrecognized input line behaviour
            Acts as a custom parser
        """
        cmds = {"show": self.do_show,
                "destroy": self.do_destroy,
                "all": self.do_all}

        arg = (arg.replace("(", ".").replace(")", ".")
                  .replace('"', "").replace(",", "").split("."))
        try:
            new_cmd = arg[0] + " " + arg[2]
            new_func = cmds[arg[1]]
            new_func(new_cmd)
        except:
            print("*** Unknown syntax")

    " ----- class instance functionality ----- "

    def do_create(self, arg):
        """ Creates new instance of cls, saves to JSON file, prints id
            Command syntax: create + [cls name]
        """
        if len(arg) == 0:
            print("** class name missing **")
            return
        arg = arg.split()
        new_inst = eval(arg[0])()
        new_inst.save()
        print(new_inst.id)

    def do_show(self, arg):
        """ Prints string representation of instance based on cls name/id
            Command syntax: show + [cls name] + [id]
        """
        if len(arg) == 0:
            print("** class name missing **")
            return
        if len(arg) == 1:
            print("** instance id missing **")
            return

        arg = arg.split()
        inst_key = arg[0] + "." + arg[1]

        storage = FileStorage()
        storage.reload()
        all_objs = storage.all()

        try:
            str_rep = all_objs[inst_key]
            print(str_rep)
        except KeyError:
            print("** no instance found**")

    def do_destroy(self, arg):
        """ Deletes instance based on cls name & instance id, saves change
            Command syntax: destroy + [cls name] + [id]
        """
        if len(arg) == 0:
            print("** class name missing **")
            return
        if len(arg) == 1:
            print("** instance id missing **")
            return

        arg = arg.split()
        inst_key = arg[0] + "." + arg[1]

        storage = FileStorage()
        storage.reload()
        all_objs = storage.all()

        try:
            del all_objs[inst_key]
        except KeyError:
            print("** no instance found**")
        storage.save()

    def do_all(self, arg):
        """ Prints string representation of all instances based on cls name
            Command syntax: all + [ENTER]
        """
        new_list = []
        new_list2 = []
        storage = FileStorage()
        storage.reload()
        all_objs = storage.all()

        for key, value in all_objs.items():
            new_list.append(value.__str__())
        for i in new_list:
            new_list2.append(str(i))
        print(new_list2)

    def do_update(self, arg):
        """ Updates instance based on cls name/id by attribute, saves to JSON
            Command syntax: update + [cls nme] + [id] + [attr nme] + [attr val]
        """
        if len(arg) == 0:
            print("** class name missing **")
            return
        if len(arg) == 1:
            print("** instance id missing **")
            return
        if len(arg) == 2:
            print("** attribute name missing **")
            return
        if len(arg) == 3:
            print("** value missing **")
            return

        arg = arg.split()
        inst_key = arg[0] + "." + arg[1]

        storage = FileStorage()
        storage.reload()
        all_objs = storage.all()

        try:
            obj_value = all_objs[inst_key]
        except KeyError:
            print("** no instance found**")
            return

        setattr(obj_value, arg[2], arg[3])
        obj_value.save()

if __name__ == '__main__':
    """ Loops the CLI, prevents running on import
    """
    HBNBCommand().cmdloop()
