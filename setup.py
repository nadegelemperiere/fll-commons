""" -----------------------------------------------------
# TECHNOGIX
# -------------------------------------------------------
# Copyright (c) [2022] Technogix SARL
# All rights reserved
# -------------------------------------------------------
# IT orchestrator module setup file
# -------------------------------------------------------
# Nadège LEMPERIERE, @17 october 2021
# Latest revision: 17 october 2021
# --------------------------------------------------- """

from os import path
from setuptools import setup, find_packages
from re import search

setup(
    name = "fll-commons",
    author = "Nadege LEMPERIERE",
    author_email='nadege.lemperiere@gmail.com',
    url='https://github.com/nadegelemperiere/fll-commons/',
    use_scm_version=True,
    packages=find_packages(),
    include_package_data=True,
    description = ("Common tools for all challenges"),
    license = "MIT",
    keywords = "python spike",
    install_requires=[],
    python_requires=">=3.11",
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Testers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License'
    ],
)