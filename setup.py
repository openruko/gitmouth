# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

with open('README.md') as readme:
    long_description = readme.read()

with open('requirements.txt') as reqs:
    install_requires = [
        line for line in reqs.read().split('\n') if (line and not
                                                     line.startswith('--'))
    ]

tests_require = [
    'Flask==0.9',  # Used for mock server
]

setup(
    name='openruko-gitmouth',
    version=__import__('gitmouth').__version__,
    author='Matt Freeman',
    author_email='matt@nonuby.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/openruko/gitmouth',
    license='MIT',
    description="SSH to Git Server for Openruko - Similar to heroku's SSH server",
    long_description=long_description,
    scripts = ['gitmouth/bin/gitmouth'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Twisted',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
)
