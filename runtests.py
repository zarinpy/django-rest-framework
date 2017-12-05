#! /usr/bin/env python
from __future__ import print_function  # pragma nocover

import os  # pragma nocover
import subprocess  # pragma nocover
import sys  # pragma nocover

import pytest  # pragma nocover

PYTEST_ARGS = {  # pragma nocover
    'default': ['tests', '--tb=short', '-s', '-rw'],
    'fast': ['tests', '--tb=short', '-q', '-s', '-rw'],
}

FLAKE8_ARGS = ['rest_framework', 'tests']  # pragma nocover

ISORT_ARGS = ['--recursive', '--check-only', '-o' 'uritemplate', '-p', 'tests', 'rest_framework', 'tests']  # pragma nocover

sys.path.append(os.path.dirname(__file__))  # pragma nocover


def exit_on_failure(ret, message=None):  # pragma nocover
    if ret:
        sys.exit(ret)


def flake8_main(args):  # pragma nocover
    print('Running flake8 code linting')
    ret = subprocess.call(['flake8'] + args)
    print('flake8 failed' if ret else 'flake8 passed')
    return ret


def isort_main(args):  # pragma nocover
    print('Running isort code checking')
    ret = subprocess.call(['isort'] + args)

    if ret:
        print('isort failed: Some modules have incorrectly ordered imports. Fix by running `isort --recursive .`')
    else:
        print('isort passed')

    return ret


def split_class_and_function(string):  # pragma nocover
    class_string, function_string = string.split('.', 1)
    return "%s and %s" % (class_string, function_string)


def is_function(string):  # pragma nocover
    # `True` if it looks like a test function is included in the string.
    return string.startswith('test_') or '.test_' in string


def is_class(string):  # pragma nocover
    # `True` if first character is uppercase - assume it's a class name.
    return string[0] == string[0].upper()


if __name__ == "__main__":  # pragma nocover
    try:
        sys.argv.remove('--nolint')
    except ValueError:
        run_flake8 = True
        run_isort = True
    else:
        run_flake8 = False
        run_isort = False

    try:
        sys.argv.remove('--lintonly')
    except ValueError:
        run_tests = True
    else:
        run_tests = False

    try:
        sys.argv.remove('--fast')
    except ValueError:
        style = 'default'
    else:
        style = 'fast'
        run_flake8 = False
        run_isort = False

    if len(sys.argv) > 1:
        pytest_args = sys.argv[1:]
        first_arg = pytest_args[0]

        try:
            pytest_args.remove('--coverage')
        except ValueError:
            pass
        else:
            pytest_args = [
                '--cov-report',
                'xml',
                '--cov',
                'rest_framework'] + pytest_args

        if first_arg.startswith('-'):
            # `runtests.py [flags]`
            pytest_args = ['tests'] + pytest_args
        elif is_class(first_arg) and is_function(first_arg):
            # `runtests.py TestCase.test_function [flags]`
            expression = split_class_and_function(first_arg)
            pytest_args = ['tests', '-k', expression] + pytest_args[1:]
        elif is_class(first_arg) or is_function(first_arg):
            # `runtests.py TestCase [flags]`
            # `runtests.py test_function [flags]`
            pytest_args = ['tests', '-k', pytest_args[0]] + pytest_args[1:]
    else:
        pytest_args = PYTEST_ARGS[style]

    if run_tests:
        exit_on_failure(pytest.main(pytest_args))

    if run_flake8:
        exit_on_failure(flake8_main(FLAKE8_ARGS))

    if run_isort:
        exit_on_failure(isort_main(ISORT_ARGS))
