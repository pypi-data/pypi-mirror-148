# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name="QUnitSuite",
    version="0.4",
    packages=['qunitsuite', 'qunitsuite.tests'],
    package_data={'qunitsuite': ['grunt/*']},
    author="Xavier Morel",
    author_email="xavier.morel@masklinn.net",
    description="unittest TestSuite integrating a QUnit javascript suite into a "
                "unittest flow",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: JavaScript",
        "Topic :: Software Development :: Testing",
    ]
)
