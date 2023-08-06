from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = "\n" + f.read()

VERSION = '0.1.0'
DESCRIPTION = 'A Python package for finding the best decision tree parameters.'
LONG_DESCRIPTION = long_description

setup(
    name="bestree",
    version=VERSION,
    author="CodingLive",
    author_email="<rootcode@duck.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=["numpy", "scikit-learn", "pandas"],
    keywords=["decision tree", "decision tree parameters", "best tree parameters"],
)