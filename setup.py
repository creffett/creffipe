#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="reffipe",
    description="A recipe storage program",
    author="Chris & Caroline Reffett",
    author_email="",
    url="https://github.com/creffett/reffipe",
    version="0.1.0",
    license="GPLv3+"
    zip_safe=False,
    packages=find_packages(),
    install_requires=[
        'SQLAlchemy>=1.1.0b1',
        'alembic',
        'pint',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ]
)
