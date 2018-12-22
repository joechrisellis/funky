from setuptools import *

with open("README.md") as f:
    readme = f.read()

kwargs = {
    "author"           : "Joe Ellis",
    "author_email"     : "joechrisellis@gmail.com",
    "description"      : "BSc Computer Science final year project -- " \
                         "developing a functional programming compiler.",
    "long_description" : readme,
    "license"          : "GPL v2",
    "name"             : "funky",
    "packages"         : find_packages(),
    "version"          : "V0.1",
    "entry_points"     : {
        "console_scripts" : ["funky=funky.cli:start"],
    },
    "install_requires" : [
        "ply", # <-- for parsing
    ]
}

setup(**kwargs)
