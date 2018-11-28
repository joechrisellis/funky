from setuptools import *

kwargs = {
    "author" : "Joe Ellis",
    "author_email" : "joechrisellis@gmail.com",
    "description" : "BSc Computer Science final year project -- developing a " \
                    "functional programming compiler.",
    "license" : "GPL v2",
    "name" : "funky",
    "packages" : find_packages(),
    "version" : "V0.1",
    "entry_points" : {"console_scripts" : ["funky=funky.cli:start"]},
}

setup(**kwargs)
