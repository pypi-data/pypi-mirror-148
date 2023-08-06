from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.2'
DESCRIPTION = 'A plugin for creating Space Time Cube'
LONG_DESCRIPTION = "spacetimecube is a Python module that allows users to create Space Time Cube and calculate Getis Ord and Local Moran's I analysis on the cube."

# Setting up
setup(
    name="spacetimecube",
    version=1.2,
    author="Murat Çalışkan, Berk Anbaroğlu",
    author_email="caliskan.murat.20@gmail.com,banbar@hacettepe.edu.tr",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['gdal', 'numpy', 'pandas', 'matplotlib'],
    keywords=['python', 'space time cube', 'getis', 'ord', 'local', 'moran', 'spatial', 'data science', 'gis'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
