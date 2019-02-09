from setuptools import *

README_FILE  = "./README.md"
VERSION_FILE = "./funky/_version.py"

# get the readme text
with open(README_FILE) as f:
    readme = f.read()

# get the version (loads into __version__)
with open(VERSION_FILE) as f:
    exec(f.read())

kwargs = {
    "author"           : "Joe Ellis",
    "author_email"     : "joechrisellis@gmail.com",
    "description"      : "BSc Computer Science final year project -- " \
                         "developing a functional programming compiler.",
    "long_description" : readme,
    "license"          : "GPL v2",
    "name"             : "funky",
    "packages"         : find_packages(),
    "version"          : __version__,
    "entry_points"     : {
        "console_scripts" : ["funky=funky.cli:start",  # compiler
                             "funkyi=funky.repl:start" # repl
        ],
    },
    "install_requires" : [
        "ply", # <-- for parsing
    ]
}

setup(**kwargs)
