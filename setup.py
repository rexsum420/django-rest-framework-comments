#!/usr/bin/env python3
import os
import re
import shutil
import sys
from io import open

from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 8)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================

<<<<<<< HEAD
This version of Django REST Framework w/ Comments requires Python {}.{}, but you're trying
=======
This version of Django REST Framework requires Python {}.{}, but you're trying
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9
to install it on Python {}.{}.

This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:

    $ python -m pip install --upgrade pip setuptools
<<<<<<< HEAD
    $ python -m pip install drf-comments
=======
    $ python -m pip install djangorestframework
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9

This will install the latest version of Django REST Framework which works on
your version of Python. If you can't upgrade your pip (or Python), request
an older version of Django REST Framework:

<<<<<<< HEAD
    $ python -m pip install "drf-comments<1.01"
=======
    $ python -m pip install "djangorestframework<3.10"
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)


def read(f):
    with open(f, 'r', encoding='utf-8') as file:
        return file.read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


<<<<<<< HEAD
version = get_version('drf_comments')
=======
version = get_version('rest_framework')
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9


if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    if os.system("twine check dist/*"):
        print("twine check failed. Packages might be outdated.")
        print("Try using `pip install -U twine wheel`.\nExiting.")
        sys.exit()
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('djangorestframework.egg-info')
    sys.exit()


setup(
<<<<<<< HEAD
    name='drf-comments',
    version='0.3',
    url='https://github.com/rexsum420/django-rest-framework-comments.git',
    license='BSD',
    description='Web APIs for Django with comments, made easy.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Jeffery Springs',
    author_email='rexsum420@gmail.com',
=======
    name='djangorestframework',
    version=version,
    url='https://www.django-rest-framework.org/',
    license='BSD',
    description='Web APIs for Django, made easy.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Tom Christie',
    author_email='tom@tomchristie.com',  # SEE NOTE BELOW (*)
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=["django>=4.2", 'backports.zoneinfo;python_version<"3.9"'],
    python_requires=">=3.8",
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
    ],
    project_urls={
<<<<<<< HEAD
        'Source': 'https://github.com/rexsum420/django-rest-framework-comments.git',
    },
)
=======
        'Funding': 'https://fund.django-rest-framework.org/topics/funding/',
        'Source': 'https://github.com/encode/django-rest-framework',
        'Changelog': 'https://www.django-rest-framework.org/community/release-notes/',
    },
)

# (*) Please direct queries to the discussion group, rather than to me directly
#     Doing so helps ensure your question is helpful to other users.
#     Queries directly to my email are likely to receive a canned response.
#
#     Many thanks for your understanding.
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9
