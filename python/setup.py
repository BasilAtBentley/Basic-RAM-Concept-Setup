#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

from setuptools import setup, find_packages

# this will fail if not run from an installation as the version_constant.py file will not exist
from ram_concept.version_constant import API_VERSION

setup(
    name="ram_concept",
    version=API_VERSION,
    packages=["ram_concept"],
    install_requires=["requests>=2.23"],
    python_requires='>=3.8',
    author="Bentley Systems, Inc.",
    description="This package provides an interop API for RAM Concept."
    )