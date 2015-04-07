from setuptools import setup, find_packages

import djohno

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
        'django-setuptest==0.1.6',
        'mock==1.0.1',
        'httpretty==0.6.3',
    ),
    test_suite='setuptest.setuptest.SetupTestSuite',
)
