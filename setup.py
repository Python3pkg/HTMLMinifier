"""
HTMLMinifier
------------

A simple HTML5 minifier written in Python.

:copyright: (c) 2014-2015, Chi-En Wu.
:license: BSD 3-Clause License.
"""

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import HTMLMinifier


class Tox(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['-v', '-epy']
        self.test_suite = True

    def run_tests(self):
        import tox
        tox.cmdline(self.test_args)


setup(
    name='HTMLMinifier',
    version=HTMLMinifier.__version__,
    author=HTMLMinifier.__author__,
    author_email='',
    description='A simple HTML5 minifier written in Python.',
    long_description=__doc__,
    url='https://github.com/jason2506/HTMLMinifier',
    license=HTMLMinifier.__license__,
    packages=find_packages(),
    zip_safe=False,
    platforms='any',
    install_requires=[],
    tests_require=['tox'],
    cmdclass={'test': Tox},
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        "Topic :: Text Processing :: Markup :: HTML",
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
