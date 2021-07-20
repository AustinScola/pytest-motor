"""A build script using setuptools for the pytest motor package."""
import pathlib
from typing import List

import setuptools

_HERE = pathlib.Path(__file__).parent

_README = _HERE / 'README.md'
_LONG_DESCRIPTION = _README.read_text()

_VERSION_FILE = _HERE / 'VERSION.txt'
_VERSION = _VERSION_FILE.read_text()

_PACKAGES: List[str] = setuptools.find_packages(where=_HERE, include=['pytest_motor*'])

setuptools.setup(
    name='pytest-motor',
    version=_VERSION,
    author='Austin Scola',
    author_email='austinscola@gmail.com',
    description='A pytest plugin for motor, the non-blocking MongoDB driver.',
    long_description=_LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/AustinScola/pytest-motor',
    packages=_PACKAGES,
    package_data={'pytest_motor': ['py.typed']},
    entry_points={'pytest11': ['pytest_motor = pytest_motor.plugin']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Pytest',
        'Topic :: Software Development :: Testing',
        'Typing :: Typed',
    ],
    python_requires='>=3.6',
    install_requires=['pytest', 'motor', 'aiohttp[speedups]', 'distro'],
)
