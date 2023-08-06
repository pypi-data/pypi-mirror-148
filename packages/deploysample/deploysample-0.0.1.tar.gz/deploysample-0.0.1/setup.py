from setuptools import setup, find_packages
from distutils.core import setup






setup(
    name = 'deploysample',
    version= '0.0.1',
    description = 'adding numbers',
    long_description= open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Saurabh',
    author_email='saurabhp@leewayhertz.com',
    license='MIT',
    keywords = '',
    packages=find_packages(),
    install_requires=['']
)