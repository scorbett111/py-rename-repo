import os
from setuptools import (
    setup,
    find_packages
)

current_directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(current_directory, 'README.md'), "r") as readme:
    package_description = readme.read()

setup(
    name="py-gcmd",
    version="0.0.3",
    author="Sean C.",
    author_email="randomaccess403@gmail.com",
    description="py-rename-repo renames the provided branch for all repositories under a user's Github/Gitlab/Bitbucket account.",
    long_description=package_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scorbett111/py-rename-repo",
    data_files=[
        ('config', ['config/recipies.json'])
    ],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'ConfigArgParse',
        'cryptography',
        'PyGitHub',
        'python-gitlab',
        'bitbucket-python',
        'python-dotenv',
        'gitpython'

    ],
    entry_points = {
        'console_scripts': [
            'gcmd=gcmd:run'
        ],
    },
    python_requires='>=3.7'
)
