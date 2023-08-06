
# !/usr/bin/env python
import os
from os import path
from setuptools import setup


this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='sztaki',
      version='0.1.2',
      description='Hungarian to English words tranlator',
      url='https://github.com/adyachok/sztaki',
      author='Andras Gyacsok',
      author_email='atti.dyachok@gmail.com',
      license='MIT',
      packages=['sztaki'],
      install_requires=[
            'beautifulsoup4==4.11.1',
            'certifi==2021.10.8',
            'charset-normalizer==2.0.12',
            'dataclasses-json==0.5.7',
            'idna==3.3',
            'googletrans==3.1.0a0',
            'marshmallow==3.15.0',
            'marshmallow-enum==1.5.1',
            'mypy-extensions==0.4.3',
            'packaging==21.3',
            'pyparsing==3.0.8',
            'requests==2.27.1',
            'soupsieve==2.3.2.post1',
            'typing-inspect==0.7.1',
            'typing_extensions==4.2.0',
            'urllib3==1.26.9'
      ],
      long_description_content_type='text/markdown',
      long_description=long_description,
      zip_safe=False)