# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 10:32:24 2022

@author: BMU085
"""

from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='dame_sexo',
  version='0.0.1',
  description='Name sex classifier',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Luis Vivas',
  author_email='luisvivas@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages(),
  install_requires=['nltk'] 
)