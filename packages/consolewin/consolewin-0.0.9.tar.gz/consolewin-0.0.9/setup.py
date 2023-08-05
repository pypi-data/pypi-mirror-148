from os import read
from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]


setup(
    name='consolewin',
    version='0.0.9',
    description='A simple package for begginers!',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Adam Yasser',
    author_email='adam.y.h.20o1@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Console',
    packages=find_packages(),
    install_requires=['colorama']
)