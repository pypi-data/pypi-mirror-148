from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding = 'utf-8') as f:
    long_description = f.read()

setup(
    name = 'advancedmaths',
    version = '1.0.0b1',
    author = 'JamesJ',
    author_email = 'GGJamesQQ@yeah.net',
    description = 'A module to calculate math problems.',
    python_requires = '>=3.6.0',
    classifiers = [
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Topic :: Scientific/Engineering :: Mathematics'
    ],
    url = 'https://github.com/CokeStudios/AdvancedMath',
    packages = ['advancedmath'],
    long_description = long_description,
    long_description_content_type = 'text/markdown',
)