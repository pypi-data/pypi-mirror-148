# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="django-tinystore",
    version="0.0.2",
    author="Jon Combe",
    author_email="jon@naremit.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    url="https://github.com/joncombe/django-tinystore",
    license="BSD licence, see LICENCE file",
    description="A tiny, persistent JSON store for Django",
    long_description="A tiny, persistent JSON store for Django",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
