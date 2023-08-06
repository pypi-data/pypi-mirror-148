import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="pyutmodel",
    version="1.0.1",
    author_email='Humberto.A.Sanchez.II@gmail.com',
    description='External Pyut Data Model',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/pyutmodel",
    packages=[
        'pyutmodel',
    ],
    install_requires=['Deprecated'],
)
