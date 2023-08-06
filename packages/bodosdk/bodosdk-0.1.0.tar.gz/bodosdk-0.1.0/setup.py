from setuptools import setup, find_packages

setup(
   name='bodosdk',
   version='0.1.0',
   author='Piotr Szajer',
   author_email='piotr@bodo.ai',
   packages=find_packages(include=['bodosdk', 'bodosdk.*']),
   scripts=[],
   url='http://pypi.python.org/pypi/PackageName/',
   license='LICENSE.txt',
   description='Bodo Platform SDK',
   long_description=open('README.md').read(),
   long_description_content_type="text/markdown",
   install_requires=open('requirements.txt').readlines()
)