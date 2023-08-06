#!/usr/bin/env python

import pathlib
import setuptools.command.test
import sys
from setuptools import setup, find_packages
from typing import Dict

requirements = [
]

test_requirements = [
    'aioresponses~=0.0',
    'docstring_parser~=0.0',
    'flask~=2.0',
    'jsonschema~=3.0',
    'pytest~=6.0',
    'pytest-aiohttp~=0.0',
    'pytest-mock~=3.0',
    'responses~=0.0',
    'respx~=0.0',
    'pydantic~=1.8.0',
    'werkzeug~=2.0',
    'openapi_ui_bundles~=0.0',
]

with open('README.rst', 'r') as file:
    readme = file.read()


def parse_about() -> Dict[str, str]:
    about_globals = {}
    this_path = pathlib.Path(__file__).parent
    about_module_text = pathlib.Path(this_path, 'xjsonrpc', '__about__.py').read_text()
    exec(about_module_text, about_globals)

    return about_globals


about = parse_about()


class PyTest(setuptools.command.test.test):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        setuptools.command.test.test.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.pytest_args))


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    author=about['__author__'],
    author_email=about['__email__'],
    url=about['__url__'],
    license=about['__license__'],
    keywords=[
        'json-rpc', 'rpc', 'jsonrpc-client', 'jsonrpc-server',
        'requests', 'aiohttp', 'flask', 'httpx', 'aio-pika', 'kombu',
        'openapi', 'openrpc', 'starlette', 'django',
    ],
    python_requires=">=3.6",
    packages=find_packages(),
    install_requires=requirements,
    tests_require=test_requirements,
    extras_require={
        'aiohttp': ['aiohttp~=3.0'],
        'aio-pika': ['aio-pika~=7.0'],
        'flask': ['flask~=2.0'],
        'jsonschema': ['jsonschema~=3.0'],
        'kombu': ['kombu~=5.0'],
        'pydantic': ['pydantic~=1.8.0'],
        'requests': ['requests~=2.0'],
        'httpx': ['requests~=0.0'],
        'docstring-parser': ['docstring-parser~=0.0'],
        'openapi-ui-bundles': ['openapi-ui-bundles~=0.0'],
        'starlette': ['starlette~=0.12.0', 'aiofiles~=0.7'],
        'django': ['django~=3.0'],
        'test': [test_requirements],
    },
    entry_points={"pytest11": ["xjsonrpc = xjsonrpc.client.integrations.pytest"]},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    project_urls={
        "Documentation": "https://xjsonrpc.readthedocs.io/en/latest/",
        'Source': 'https://github.com/bernhardkaindl/xjsonrpc',
    },
    cmdclass={'test': PyTest},
)
