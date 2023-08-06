#!/usr/bin/env python3
"""Setup file for the midas package."""
import setuptools


with open("VERSION") as freader:
    VERSION = freader.readline().strip()


with open("README.md") as freader:
    README = freader.read()

install_requirements = [
    "click",
    "mosaik",
    "midas-util",
    "midas-analysis",
    "midas-store",
    "midas-powergrid",
    "midas-sndata",
    "midas-sbdata>=1.0.0rc3",
    "midas-comdata",
    "midas-dlpdata",
    "midas-pwdata",
    "midas-goa",
    "midas-weather",
    "midas-timesim",
    "pysimmods>=0.7.2",
    "ruamel.yaml",
    "simbench",
    "setproctitle",
    "wget",
    "xlrd",
]

development_requirements = [
    "numba",
    "flake8",
    "pytest",
    "tox",
    "coverage",
    "black==22.3.0",
    "setuptools",
    "twine",
    "wheel",
    "sphinx",
]

extras = {"dev": development_requirements}

setuptools.setup(
    name="midas-mosaik",
    version=VERSION,
    author="Stephan Balduin",
    author_email="stephan.balduin@offis.de",
    description="MultI-DomAin test Scenario for smart grid co-simulation.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/midas-mosaik/midas",
    packages=["midas.api", "midas.scenario"],
    include_package_data=True,
    install_requires=install_requirements,
    extras_require=extras,
    entry_points="""
        [console_scripts]
        midasctl=midas.api.cli:cli
    """,
    license="LGPL",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v2 (LGPLv2)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
)
