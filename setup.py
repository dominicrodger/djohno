import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import djohno


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='djohno',
    version=djohno.__version__,
    description="A tiny Django app for checking over your error pages.",
    long_description=open('README.rst').read(),
    author='Dominic Rodger',
    author_email='internet@dominicrodger.com',
    url='https://github.com/dominicrodger/djohno',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=1.4",
        "pkgtools==0.7.2",
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
    tests_require=(
        "pytest==2.6.4",
        "pytest-cov==1.7.0",
        "pytest-django==2.8.0",
        'mock==1.0.1',
        'httpretty==0.6.3',
    ),
    cmdclass = {'test': PyTest},
)
