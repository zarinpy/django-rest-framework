#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os  # pragma nocover
import re  # pragma nocover
import shutil  # pragma nocover
import sys  # pragma nocover
from io import open  # pragma nocover

from setuptools import setup, find_packages  # pragma nocover

try:  # pragma nocover
    from pypandoc import convert_file

    def read_md(f):
        return convert_file(f, 'rst')
except ImportError:  # pragma nocover
    print("warning: pypandoc module not found, could not convert Markdown to RST")

    def read_md(f):  # pragma nocover
        return open(f, 'r', encoding='utf-8').read()


def get_version(package):  # pragma nocover
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('rest_framework')  # pragma nocover


if sys.argv[-1] == 'publish':  # pragma nocover
    try:
        import pypandoc
    except ImportError:
        print("pypandoc not installed.\nUse `pip install pypandoc`.\nExiting.")
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('djangorestframework.egg-info')
    sys.exit()


setup(  # pragma nocover
    name='djangorestframework',
    version=version,
    url='http://www.django-rest-framework.org',
    license='BSD',
    description='Web APIs for Django, made easy.',
    long_description=read_md('README.md'),
    author='Tom Christie',
    author_email='tom@tomchristie.com',  # SEE NOTE BELOW (*)
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ]
)

# (*) Please direct queries to the discussion group, rather than to me directly
#     Doing so helps ensure your question is helpful to other users.
#     Queries directly to my email are likely to receive a canned response.
#
#     Many thanks for your understanding.
