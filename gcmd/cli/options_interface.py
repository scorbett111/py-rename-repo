import os
import configargparse
import json
import pathlib
import sys
from .utils import (
    remove_argv
)


class OptionsInterface:

    def __init__(self, options=None):
        self.args = []
        self.options = options
        self.parser = configargparse.ArgumentParser()

    def add_arguments(self):
        for option in self.options:
            self.parser.add(
                option.get('short_flag'),
                option.get('long_flag'),
                required=option.get('required'),
                action=option.get('action'),
                help=option.get('help')
            )

    def parse_arguments(self):
        return vars(self.parser.parse_args())

    def clean_arguments(self):
        for option in self.options:
            short_flag = option.get('short_flag')
            long_flag = option.get('long_flag')

            if short_flag in sys.argv:
                short_flag_position = sys.argv.index(short_flag)
                remove_argv(index=short_flag_position, remove=2)

            if long_flag in sys.argv:
                long_flag_position = sys.argv.index(long_flag)
                remove_argv(index=long_flag_position, remove=2)
