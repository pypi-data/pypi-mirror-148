# coding: utf-8
# python setup.py sdist register upload
from setuptools import setup

setup(
    name='sw-python-utils',
    version='0.0.18',
    description='Soft Way company python utils.',
    author='Telminov Sergey',
    url='https://github.com/telminov/sw-python-utils',
    packages=[
        'swutils',
        'swutils.tests',
    ],
    include_package_data=True,
    license='The MIT License',
    test_suite='nose.collector',
    install_requires=[
        'pycryptodome', 'requests', 'beautifulsoup4', 'phonenumbers'
    ],
)
