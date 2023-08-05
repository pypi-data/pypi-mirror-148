from setuptools import setup,find_packages
from pkg.hello import __version__
setup(
    name = "UserManage",
    version = __version__,
    description = "Command line Demo",
    author = "mengqi",
    packages = find_packages(),
    platforms = "any",
    install_requires = [
        "requests", 
        "docopt>=0.6.2"
    ],
    entry_points = {
        "console_scripts": ['UserManage = pkg.hello:cmd'] 
    }
)