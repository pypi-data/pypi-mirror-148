from setuptools import setup

with open('README.md', 'r', encoding="utf-8") as file:
    long_description = file.read()

VERSION = '0.0.3'
AUTHOR = 'Manuel Cabral'
EMAIL = 'cabral.manuel@yandex.com'
DESCRIPTION = 'Algebra and Analytic Geometry in Python'
LICENSE = 'GPLv3'

setup(
  name = 'algepy',
  packages = ['algepy'],
  version = VERSION,
  license = LICENSE,
  description = DESCRIPTION,
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  author = AUTHOR,
  author_email = EMAIL,
  url = 'https://github.com/manucabral/algepy',
  keywords = ['python', 'algebra', 'math', 'geometry', 'vector', 'algepy'],
  install_requires = ['matplotlib'],
  python_requires = '>= 3.9',
  classifiers=[
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.9',
    'Operating System :: Unix',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
  ],
)