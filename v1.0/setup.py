"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['p.py']
DATA_FILES = []
OPTIONS = {'argv_emulation': True}

setup(
	name="Text Analyzer",
    app=APP,
    setup_requires=['py2app']
)
