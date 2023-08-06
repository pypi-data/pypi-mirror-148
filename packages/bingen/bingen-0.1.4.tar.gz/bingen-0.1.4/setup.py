# !/usr/bin/env python
from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='bingen',
      version='0.1.4',
      description='German to Ukrainian words translator',
      url='https://github.com/adyachok/bingen',
      author='Andras Gyacsok',
      author_email='atti.dyachok@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
            'dataclasses-json',
            'googletrans==4.0.0rc1',
      ],
      long_description_content_type='text/markdown',
      long_description=long_description,
      package_data = {'bingen': ['stardict/de_dict/*']},
      zip_safe=False)