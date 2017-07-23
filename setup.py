import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


# ref: https://tox.readthedocs.org/en/latest/example/basic.html#integration-with-setuptools-distribute-test-commands
class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = ''

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)


class ToxWithRecreate(Tox):
    description = ('Run tests, but recreate the testing environments first. '
                   '(Useful if the test dependencies change.)')

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = '-r'


setup(
    name='datacheck',
    version='0.2.0',
    packages=['datacheck'],
    url='https://github.com/csdev/datacheck',
    license='MIT',
    author='Christopher Sang',
    description='data validation library',
    long_description='data validation library',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
    ],

    install_requires=[
        'future >= 0.14.3, < 0.17',
    ],

    # tox is responsible for setting up the test runner and its dependencies
    # (e.g., code coverage tools) -- see the tox.ini file
    tests_require=[
        'tox >= 1.9, < 3',
    ],

    cmdclass={
        'test': Tox,
        'clean_test': ToxWithRecreate,
    },
)
