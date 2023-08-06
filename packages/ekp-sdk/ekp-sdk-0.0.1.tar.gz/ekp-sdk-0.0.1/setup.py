from setuptools import setup, find_packages
import codecs
import os

# here = os.path.abspath(os.path.dirname(__file__))
#
with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Python SDK for frontend components usage'
LONG_DESCRIPTION = 'A package that allows to use front-end components to simplify ' \
                   'building of web pages for ekp plugins'

# Setting up
setup(
    name="ekp-sdk",
    version=VERSION,
    url="https://github.com/hiki0505/python-ekp-sdk",
    author="Earn Keeper (Gavin Shaw)",
    author_email="gavin@earnkeeper.io",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=["components", "currency_utils", "socket_methods"],
    package_dir={'': 'sdk'},
    packages=find_packages(),
    install_requires=['eventlet==0.33.0', 'pycoingecko==2.2.0', 'python-socketio==5.6.0'],
    keywords=['python', 'earnkeeper', 'sdk', 'components'],
    classifiers=[
        # "Development Status :: 1 - Planning",
        # "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        # "Operating System :: Unix",
        # "Operating System :: MacOS :: MacOS X",
        # "Operating System :: Microsoft :: Windows",
    ]
)