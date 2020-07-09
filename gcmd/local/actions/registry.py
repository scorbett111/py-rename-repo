import pathlib
import os
import json
from .git_command import GitCommand

class LocalRegistry:

    def __init__(self, config_directory=None, recipies_file=None):

        if recipies_file is None:
            recipies_file = 'recipies.json'
            
        recipies = None

        if os.path.isdir(config_directory) and recipies_file in os.listdir(config_directory):
            recipies_file_path = "{config_directory}/{recipies_file}".format(
                config_directory=config_directory,
                recipies_file=recipies_file
            )
            with open(recipies_file_path) as recipies_file:
                recipies = json.load(recipies_file)
        else:
            raise Exception('Error: Config directory or file not found.')

        self.recipies = recipies
        self.registered_recipies = list(recipies.keys())

    def execute(self, commands=None):
        for command_config in commands:
            command = GitCommand(command=command_config.get('name'), options=command_config.get('options'))
            print("OPTS",command.repo.options)
            print("REPO NAME",command.repo.repo_name)
            print("REPO BRANCH",command.repo.repo_branch)
            print("REPO PATH",command.repo.repo_path)
            print("REPO URL", command.repo.repo_url)
            print("REMOTE NAME",command.repo.remote_name)
            print("REMOTE BRANCH",command.repo.remote_branch)
            command.execute()