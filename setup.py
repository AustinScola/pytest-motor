"""A build script using setuptools for the pytest motor package."""
from setuptools import setup, find_packages

_PACKAGE_REQUIREMENTS = ['pytest>=5.0', 'motor>=2.0', 'aiohttp[speedups]', 'distro']
_TEST_REQUIREMENTS = ["tox>=3.24.0", "pytest-cov", "pytest-asyncio", "pytest-lazy-fixture"]
_DEV_REQUIREMENTS = ["pre-commit", "pylint", "yapf", "isort", "mypy"]

setup(name='pytest-motor',
      version=open("VERSION.txt", encoding="utf-8").read(),
      author='Austin Scola',
      author_email='austinscola@gmail.com',
      description='A pytest plugin for motor, the non-blocking MongoDB driver.',
      long_description=open("README.md", encoding="utf-8").read(),
      long_description_content_type='text/markdown',
      url='https://github.com/AustinScola/pytest-motor',
      packages=find_packages(where="pytest_motor"),
      package_data={'pytest_motor': ['py.typed']},
      entry_points={'pytest11': ['pytest_motor = pytest_motor.plugin']},
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Framework :: Pytest',
          'Topic :: Software Development :: Testing',
          'Typing :: Typed',
      ],
      python_requires='>=3.6',
      install_requires=_PACKAGE_REQUIREMENTS,
      extras_require={
          "dev": _DEV_REQUIREMENTS + _TEST_REQUIREMENTS,
          "test": _TEST_REQUIREMENTS,
      })
