import pathlib
import sys
from gcmd.cli import CommandLineInterface
from gcmd.local import LocalRegistry
from gcmd.cli.components import (
    Action
)


def run():

    config_directory = "{package_path}/config".format(
        package_path=pathlib.Path(__file__).resolve().parents[1]
    )

    registry = LocalRegistry(config_directory=config_directory)
    cli = CommandLineInterface(registry=registry)
    cli.parse_action().parse_targets().parse_options()
    action = Action(
        cli=cli
    )

    action.setup()

    for command in action.commands:
        for event in command.hooks:
            for hook in event:
                for target in hook.targets:
                    print(target.map, target.value)
                for option in hook.options:
                    print(option.map, option.value)
    # registry.execute(
    #     commands=action.commands
    # )
    # auth = Auth(config=options)
    # service = Service(
    #     service_name=options.get('service')
    # )

    # service.login(auth=auth)


    # for repo in service.get_repositories():
    #     print(repo.name)

if __name__ == '__main__':
    run()