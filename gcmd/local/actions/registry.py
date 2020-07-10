import pathlib
import os
import json
from .git_command import GitCommand

class LocalRegistry:

    def __init__(self, config_directory=None, recipies_file=None):

        recipies_path = "{config_directory}/recipies".format(
            config_directory=config_directory
        )
            
        recipies = {}

        if os.path.isdir(recipies_path): 
            for recipies_file in os.listdir(recipies_path):
                recipies_file_path = "{recipies_path}/{recipies_file}".format(
                    recipies_path=recipies_path,
                    recipies_file=recipies_file
                )
                with open(recipies_file_path) as recipies_file:
                    recipie_config = json.load(recipies_file)
                    recipies[recipie_config.get('name')] = recipie_config
        else:
            raise Exception('Error: Config directory or file not found.')

        self.recipies = recipies
        self.registered_recipies = list(recipies.keys())

    def execute(self, commands=None):
        for command_config in commands:
            command = GitCommand(command=command_config.get('name'), options=command_config.get('options'))
            command.execute()