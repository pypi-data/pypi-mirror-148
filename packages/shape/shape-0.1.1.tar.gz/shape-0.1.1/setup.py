#!/usr/bin/env python
# coding=utf-8
import io
import re
from os.path import dirname, join

from setuptools import setup


def read(*names, **kwargs):
    with io.open(
            join(dirname(__file__), *names),
            encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name='shape',
    version='0.1.1',
    license='MIT',
    description='2D shapes abstraction',
    long_description=re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.md')),
    long_description_content_type='text/markdown',
    author='Matěj Šmíd',
    author_email='m@matejsmid.cz',
    url='https://github.com/smidm/shape',
    packages=['shape'],
    install_requires=[
        'opencv-python-headless',
#        'numpy <= 1.19; python_version <= "3.6"',
        'numpy; python_version > "3.6"',
        'matplotlib',
    ],
    python_requires='>=3.6',
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
    ],
    project_urls={
        # 'Changelog': 'https://github.com/smidm/shape/blob/master/CHANGELOG.md',
        'Issue Tracker': 'https://github.com/smidm/shape/issues',
    },
    zip_safe=True,
)
