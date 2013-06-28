from setuptools import setup, find_packages

import djohno

setup(
    name='djohno',
    version=djohno.__version__,
    description="A tiny Django app for checking over your error pages.",
    long_description=open('README.rst').read(),
    author='Dominic Rodger',
    author_email='internet@dominicrodger.com',
    url='http://github.com/dominicrodger/djohno',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=1.4",
    ],
    tests_require=(
        'django-setuptest==0.1.3',
        'mock==1.0.1',
    ),
    test_suite='setuptest.setuptest.SetupTestSuite',
)
