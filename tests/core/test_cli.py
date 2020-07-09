import subprocess
import pytest


def test_git_rename_linux():
    try:
        process = subprocess.Popen(['git-rename'],
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

    except FileNotFoundError as command_not_found:
        raise command_not_found
