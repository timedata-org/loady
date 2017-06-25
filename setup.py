from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

VERSION = 1.1


# From here: http://pytest.org/2.2.4/goodpractises.html
class RunTests(TestCommand):
    DIRECTORY = 'test'

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [self.DIRECTORY]
        self.test_suite = True

    def run_tests(self):
        # Import here, because outside the eggs aren't loaded.
        import pytest
        errno = pytest.main(self.test_args)
        if errno:
            raise SystemExit(errno)


setup(
    name='Gitty',
    version=VERSION,
    description=('Gitty lets you load Python libraries, JSON and raw text ' +
                 'dynamically from git'),
    author='Tom Ritchford',
    author_email='tom@swirly.com',
    url='http://github.com/timedata-org/gitty/',
    download_url='http://github.com/timedata-org/gitty/archive/1.1.tar.gz',
    license='MIT',
    packages=find_packages(exclude=['test']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
    ],
    tests_require=['pytest'],
    cmdclass={'test': RunTests},
    keywords=['git', 'import'],
    include_package_data=True,
    install_requires=['GitPython', 'requests'],
)
