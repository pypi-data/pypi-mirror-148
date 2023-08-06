# !/usr/bin/env python
from os import path
from setuptools import setup


this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='bingen',
      version='0.1.0',
      description='German to Ukrainian words translator',
      url='https://github.com/adyachok/bingen',
      author='Andras Gyacsok',
      author_email='atti.dyachok@gmail.com',
      license='MIT',
      packages=['bingen'],
      install_requires=[
            'build==0.7.0',
            'certifi==2021.10.8',
            'chardet==3.0.4',
            'charset-normalizer==2.0.12',
            'dataclasses-json==0.5.7',
            'googletrans==3.1.0a0',
            'h11==0.9.0',
            'h2==3.2.0',
            'hpack==3.0.0',
            'hstspreload==2021.12.1',
            'httpcore==0.9.1',
            'httpx==0.13.3',
            'hyperframe==5.2.0',
            'idna==2.10',
            'marshmallow==3.15.0',
            'marshmallow-enum==1.5.1',
            'mypy-extensions==0.4.3',
            'packaging==21.3',
            'pep517==0.12.0',
            'pyparsing==3.0.8',
            'rfc3986==1.5.0',
            'sniffio==1.2.0',
            'tomli==2.0.1',
            'typing-inspect==0.7.1',
            'typing_extensions==4.2.0',
            'urllib3==1.26.9'
      ],
      long_description_content_type='text/markdown',
      long_description=long_description,
      zip_safe=False)