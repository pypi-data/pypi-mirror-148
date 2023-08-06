from gettext import install
from setuptools import setup, find_packages





setup(
    name = 'spbasiccalculator',
    version = '0.0.1',
    description = 'a very basic addition function',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://github.com/saurabhpl/demo',
    author='Saurabh Pratap Singh',
    license='MIT',
    keywords='',
    packages=find_packages(),
)