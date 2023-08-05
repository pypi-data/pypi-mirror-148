from ensurepip import version
from setuptools import setup
from io import open

version = '0.9.10'

long_description = '''Python module for pasprot recognize'''

setup(
    name='rupasportread',
    version=version,
    author='grmnvv',
    author_email='russianfracture@gmail.com',
    url='https://github.com/grmnvv/paspread',
    license='Apache License, Version 2.0, see LICENSE file',
    packages=['rupasportread'],
    install_requires=['imutils', 'pytesseract', 'numpy', 'opencv-python']
)