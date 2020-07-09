import pathlib
import sys
from gcmd.cli import CommandLineInterface
from gcmd.local import LocalRegistry


def run():

    config_directory = "{package_path}/config".format(
        package_path=pathlib.Path(__file__).resolve().parents[1]
    )

    registry = LocalRegistry(config_directory=config_directory)
    cli = CommandLineInterface(registry=registry)
    action = cli.parse_action().parse_targets().parse_options().map_to_commands()
    registry.execute(
        commands=action.get('commands')
    )
    # auth = Auth(config=options)
    # service = Service(
    #     service_name=options.get('service')
    # )

    # service.login(auth=auth)


    # for repo in service.get_repositories():
    #     print(repo.name)

if __name__ == '__main__':
    run()