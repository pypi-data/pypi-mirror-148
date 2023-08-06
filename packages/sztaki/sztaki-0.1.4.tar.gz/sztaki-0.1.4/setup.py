
# !/usr/bin/env python
import os
from os import path
from setuptools import setup


this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='sztaki',
      version='0.1.4',
      description='Hungarian to English words tranlator',
      url='https://github.com/adyachok/sztaki',
      author='Andras Gyacsok',
      author_email='atti.dyachok@gmail.com',
      license='MIT',
      packages=['sztaki'],
      install_requires=[
            'beautifulsoup4',
            'dataclasses-json',
            'googletrans==4.0.0rc1',
      ],
      long_description_content_type='text/markdown',
      long_description=long_description,
      zip_safe=False)