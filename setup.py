from setuptools import setup, find_packages

import codecs
import os
import re
here = os.path.abspath(os.path.dirname(__file__))


def read_requirements(filename):

    try:
        with open(filename) as f:
            return f.read().splitlines()
    except IOError:
        import os
        raise IOError(os.getcwd())


def find_version(*file_paths):
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string')


def read_description(filename):
    with codecs.open(filename, encoding='utf-8') as f:
        return f.read()

setup(
    name='pydockerreg',
    version=find_version('pydockerreg', '__init__.py'),
    url='https://github.com/woosley/pydockerreg',
    description='A shell to talk with your private docker registry',
    long_description=read_description('README.md'),
    author='Woosley Xu',
    author_email='woosey.xu@gmail.com',
    license='MIT',
    packages=find_packages("."),
    entry_points="""
        [console_scripts]
        pydr=pydockerreg.cli:cli
    """,
    install_requires=read_requirements('requirements.txt'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Docker',
        'Topic :: Utilities',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ]
)
