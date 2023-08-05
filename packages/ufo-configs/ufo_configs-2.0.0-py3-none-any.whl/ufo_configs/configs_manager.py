"""
This code defines a class which holds some configurations used in the other
files in this directory.
"""

# Standard imports.
import json
from collections import namedtuple
from pathlib import Path

#####################
# SPECIAL FUNCTIONS #
#####################

def reroot_list(path_list, new_path, old_path):
    """ Change a path in a list of paths in a tree, and thereby change each
    path the derives from, recursively. """
    for index, path_string in enumerate(path_list):
        if Path(path_string) == Path(old_path):
            path_list[index] = new_path
        elif Path(path_string).parent == Path(old_path):
            new_path_dash = str(Path(new_path)/Path(path_string).name)
            old_path_dash = path_string
            path_list[index] = new_path_dash
            reroot_list(path_list, new_path_dash, old_path_dash)

def reroot(path_dict, new_path, old_path):
    """ As above, but for a dictionary. """
    key_storage = []
    value_storage = []
    for key, value in path_dict.items():
        key_storage.append(key)
        value_storage.append(value)
    reroot_list(value_storage, new_path, old_path)
    result = dict()
    for index, value in enumerate(value_storage):
        result[key_storage[index]] = value
    return result

def dictionary_to_named_tuple(dictionary, class_name="X"):
    """ Convert a dictionary to a named tuple, with a given class name. """
    if not isinstance(dictionary, dict):
        return None
    result = namedtuple(class_name, dictionary.keys())(**dictionary)
    return result

##############
# MAIN CLASS #
##############

class ConfigsManager:
    """ The class in question. """
    # Class attributes.
    PATHS_KEY = "paths"
    ENCODING = "utf-8"

    def __init__(self, defaults, path_to_overrides=None):
        self.defaults = defaults
        self.overrides = self.get_overrides(path_to_overrides)
        self.set_from_defaults()
        self.set_from_overrides()

    def get_overrides(self, path_to_overrides):
        """ Get the overrides dictionary, if possible. """
        if path_to_overrides and Path(path_to_overrides).exists():
            with open(
                path_to_overrides, "r", encoding=self.ENCODING
            ) as json_file:
                json_str = json_file.read()
                result = json.loads(json_str)
            return result
        return None

    def set_from_defaults(self):
        """ Set the user-facing fields of this class, from a dictionary of
        defaults. """
        for key, value in self.defaults.items():
            setattr(self, key, value)

    def set_from_overrides(self):
        """ Attempt to override some of the defaults from our JSON file. """
        if self.overrides:
            for key, value in self.overrides.items():
                if key == self.PATHS_KEY:
                    self.set_paths_from_overrides(value)
                else:
                    self.set_from_sub_dict(key, value)

    def set_from_sub_dict(self, key, source_dict):
        """ Set a field of this class from a sub-dictionary of the overrides
        dictionary. """
        target_dict = getattr(self, key, None)
        if target_dict:
            for key, value in source_dict.items():
                if (key in target_dict) and (value is not None):
                    target_dict[key] = value

    def set_paths_from_overrides(self, overrides_paths):
        """ Set the paths from the config file, which has to be done in a
        slightly more crafty way than with the others. """
        if overrides_paths and hasattr(self, self.PATHS_KEY):
            paths_field = getattr(self, self.PATHS_KEY)
            for key, new_path in overrides_paths.items():
                if new_path:
                    old_path = paths_field[key]
                    paths_field = reroot(paths_field, new_path, old_path)
            setattr(self, self.PATHS_KEY, paths_field)
            self.set_from_sub_dict(self.PATHS_KEY, overrides_paths)

    def export_as_immutable(self):
        """ Export the data in this class into an immutable form. """
        Config = namedtuple("Config", self.defaults.keys())
        configs_dict = dict()
        for key in self.defaults:
            configs_dict[key] = \
                dictionary_to_named_tuple(getattr(self, key), key)
        result = Config(**configs_dict)
        return result

###################
# HELPER FUNCTION #
###################

def get_configs_object(defaults, path_to_overrides=None):
    """ Get an immutable configs object, from a dictionary of defaults, and
    possibly a path to an overrides JSON file. """
    manager = ConfigsManager(defaults, path_to_overrides=path_to_overrides)
    result = manager.export_as_immutable()
    return result
