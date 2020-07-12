import pathlib
import sys
from gcmd.cli import CommandLineInterface
from gcmd.local import LocalRegistry
from gcmd.components import Action
from gcmd.remote.auth import Auth
from gcmd.remote.services import (
    Service
)

def run():

    # config_directory = "{package_path}/config".format(
    #     package_path=pathlib.Path(__file__).resolve().parents[1]
    # )

    # registry = LocalRegistry(config_directory=config_directory)
    # cli = CommandLineInterface(registry=registry)
    # cli.parse_action().parse_targets().parse_options()
    # action = Action(
    #     cli=cli
    # )

    # action.setup()
    # registry.execute(
    #     commands=action.commands
    # )
    auth = Auth(config=options)
    service = Service(
        service_name=options.get('service')
    )

    service.login(auth=auth)


    for repo in service.get_repositories():
        print(repo.name)

if __name__ == '__main__':
    run()