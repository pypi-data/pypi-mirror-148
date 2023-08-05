import os
import sys
from typing import List
import importlib.util

import GoldyBot
from GoldyBot.errors import ModuleFailedToLoad, ModuleNotFound

MODULE_NAME = "MODULES"

sys.path.insert(1, GoldyBot.paths.MODULES)
sys.path.append(GoldyBot.paths.INTERNAL_MODULES_V4)

class Module(object):
    """Goldy Bot class to easily interface with modules."""
    def __init__(self, path_to_module:str=None, module_file_name:str=None):
        self.path_to_module = path_to_module
        self.module_file_name = module_file_name

        self.is_internal_module_ = False
        self.is_external_module_ = False
        self.is_package_module_ = False

        self.ignored_modules_list = GoldyBot.config.Config(GoldyBot.files.File(GoldyBot.paths.GOLDY_CONFIG_JSON)).read("ignored_modules")

        if self.path_to_module == None:
            if self.module_file_name == None:
                GoldyBot.logging.log("error", "Module() must have either arguments 'path_to_module' or 'module_file_name' passed in.")
            else:
                # Find where module is located.
                #----------------------------------
                if self.module_file_name in os.listdir(GoldyBot.paths.INTERNAL_COGS_V4):
                    self.path_to_module = f"{GoldyBot.paths.INTERNAL_COGS_V4}/{self.module_file_name}"
                    self.is_internal_module_ = True

                if self.module_file_name in os.listdir(GoldyBot.paths.MODULES):
                    self.path_to_module = f"{GoldyBot.paths.MODULES}/{self.module_file_name}"
                    self.is_external_module_ = True

                if not self.path_to_module == None:
                    GoldyBot.logging.log(f"[{MODULE_NAME}] The module '{self.module_file_name}' was found in '{self.path_to_module}'.")
                    
                    if os.path.isdir(self.path_to_module): # Checks if the module is a package module.
                        GoldyBot.logging.log("info", f"[{MODULE_NAME}] The module '{self.module_file_name}' was dectected as a package module.")
                        self.is_package_module_ = True

                else:
                    #GoldyBot.logging.log("warn", f"[{MODULE_NAME}] The module '{self.module_file_name}' was not found!")
                    raise ModuleNotFound(f"[{MODULE_NAME}] The module '{self.module_file_name}' was not found!")
        else:
            # Assume 'path_to_module' was used.
            self.module_file_name = path_to_module.split("/")[-1]

        # Cache module.
        #----------------
        if self.is_external_module_:
            if not self.name in GoldyBot.cache.main_cache_dict["modules"]:
                GoldyBot.cache.main_cache_dict["modules"][f"{self.name}"] = {}
                GoldyBot.cache.main_cache_dict["modules"][f"{self.name}"]["extenstions"] = {}
                GoldyBot.cache.main_cache_dict["modules"][f"{self.name}"]["object"] = self
        else:
            if not self.name in GoldyBot.cache.main_cache_dict["internal_modules"]:
                GoldyBot.cache.main_cache_dict["internal_modules"][f"{self.name}"] = {}
                GoldyBot.cache.main_cache_dict["internal_modules"][f"{self.name}"]["extenstions"] = {}
                GoldyBot.cache.main_cache_dict["internal_modules"][f"{self.name}"]["object"] = self


    def load(self):
        """Commands Goldy Bot to load this module."""
        
        if not self.module_file_name[:-3] in self.ignored_modules_list:
            if self.is_package_module_:
                # Specify Package Module
                sys.path.append(self.path_to_module)

                spec_module = importlib.util.spec_from_file_location(self.module_file_name, self.path_to_module + "/__init__.py")
            else:
                # Specify Module
                spec_module = importlib.util.spec_from_file_location(self.module_file_name[:-3], self.path_to_module)

            # Get Module
            module_py = importlib.util.module_from_spec(spec_module)
            
            # Run Module
            spec_module.loader.exec_module(module_py)

            # Get load function from module.
            try:
                load_function = getattr(module_py, "load")
                load_function()

                GoldyBot.logging.log("info_4", f"[{MODULE_NAME}] Loaded the internal module '{self.module_file_name}'!")
            except AttributeError:
                #TODO: #21 Raise a Goldy Bot error here.
                #GoldyBot.logging.log("error", f"[{MODULE_NAME}] The internal module '{self.module_file_name[:-3]}' failed to load because it did not contain the 'load()' function.")
                raise ModuleFailedToLoad(f"[{MODULE_NAME}] The internal module '{self.name}' failed to load because it did not contain the 'load()' function.")

        else:
            GoldyBot.logging.log("info", f"[{MODULE_NAME}] The internal module '{self.name}' is not being loaded as it was ignored.")

    def reload(self):
        """Commands Goldy Bot to reload this module."""

        # Unload the module.
        #--------------------------
        self.unload()

        # Load the module again.
        #--------------------------
        GoldyBot.logging.log(f"[{MODULE_NAME}] Reloading module...")
        self.load()

    def unload(self):
        """Commands Goldy Bot to unload this module with it's commands."""

        # Remove all commands in module.
        #---------------------------------
        GoldyBot.logging.log(f"[{MODULE_NAME}] Getting all module's commands...")
        commands_list = self.commands

        for command in commands_list:
            command.remove()
        
        GoldyBot.logging.log(f"[{MODULE_NAME}] Removed all commands!")

        GoldyBot.logging.log("info_5", f"[{MODULE_NAME}] Unloaded the module '{self.module_file_name}'!")

    @property
    def name(self):
        """Returns the name of the module."""
        if self.is_package_module_:
            return self.module_file_name
        else:
            return self.module_file_name[:-3]


    @property
    def commands(self):
        """List of commands in the module."""
        if self.is_internal_module: modules_list_name = "internal_modules"
        else: modules_list_name = "modules"

        commands:List[GoldyBot.objects.command.Command] = []

        # Finding all commands in this.
        #-----------------------
        GoldyBot.logging.log(f"[{MODULE_NAME}] Finding all commands in the module '{self.name}'...")
        for extenstion in GoldyBot.cache.main_cache_dict[modules_list_name][self.name]["extenstions"]:
            for command in GoldyBot.cache.main_cache_dict[modules_list_name][self.name]["extenstions"][extenstion]["commands"]:
                command:GoldyBot.objects.command.Command

                commands.append(command)

        return commands

    @property
    def is_internal_module(self):
        """Commands Goldy Bot to check whether this module is an internal module or an external one."""
        if self.is_internal_module_:
            return True
        else:
            return False