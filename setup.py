# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


def get_version():
    version = "0.0.0"
    return version


setup(
    name='oftools_compile',
    version=get_version(),
    description='compiler frontend for Openframe compilers',
    long_description=readme,
    author='Tmaxsoft Inc.',
    author_email='tfsadmin@tmaxsoft.com',
    url='https://tmaxsoft.com',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    scripts=['bin/oftools_compile'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Tmaxsoft Copyright",
        "Operating System :: Linux",
    ],
    python_requires='>=3.5',
)
