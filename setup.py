from setuptools import setup, find_packages

import djohno

setup(
    name='djohno',
    version=djohno.__version__,
    description="I'll fill this in later.",
    long_description=open('README.md').read(),
    author='Dominic Rodger',
    author_email='internet@dominicrodger.com',
    url='http://github.com/dominicrodger/djohno',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django==1.5.1",
    ],
)
