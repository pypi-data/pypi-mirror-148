from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '2.2.3'
DESCRIPTION = 'Seperate the song and artist name from a song title'
LONG_DESCRIPTION = 'The SongNameSplit library can attempt to take a song title and identify the song name and artist name. This is still under development.'

setup(
    name="SongNameSplit",
    version=VERSION,
    author="Archit Tandon",
    author_email="archittandon26@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['google', 'bs4', 'requests', 'beautifulsoup4', 'tqdm'],
    keywords=['python', 'song', 'song name', 'artist', 'artist name'],
    classifiers=[]
)
