"""
This module provides fixtures for mocking requests in the PyPI Package Info module tests.

Fixtures:
    - mock_get_user_packages_success: Mocks requests.get for a successful user packages fetch.
    - mock_get_user_packages_error: Mocks requests.get for an error during user packages fetch.
    - mock_get_package_details_success: Mocks requests.get for a successful package details fetch.
    - mock_get_package_details_error: Mocks requests.get for an error during package details fetch.
    - mock_get_all_packages_details_success: Mocks requests.get for a successful fetch of all package details.
"""

from typing import Any, Generator, Union
from unittest.mock import AsyncMock, MagicMock, patch, Mock

import pytest
import requests


@pytest.fixture
def mock_get_user_packages_success() -> Generator[Union[MagicMock, AsyncMock], Any, None]:
    """Fixture to mock requests.get for get_user_packages success case."""
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = '''
        <a class="package-snippet">
            <h3 class="package-snippet__title">Package1</h3>
            <p class="package-snippet__description">Description1</p>
        </a>
        <a class="package-snippet">
            <h3 class="package-snippet__title">Package2</h3>
            <p class="package-snippet__description">Description2</p>
        </a>
        '''
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def mock_get_user_packages_error() -> Generator[Union[MagicMock, AsyncMock], Any, None]:
    """Fixture to mock requests.get for get_user_packages error case."""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.RequestException("Request error")
        yield mock_get


@pytest.fixture
def mock_get_package_details_success() -> Generator[Union[MagicMock, AsyncMock], Any, None]:
    """Fixture to mock requests.get for get_package_details success case."""
    with patch('requests.get') as mock_get:
        mock_response1 = Mock()
        mock_response1.raise_for_status.return_value = None
        mock_response1.json.return_value = {
            'info': {
                'name': 'Package1',
                'version': '1.0.0',
                'summary': 'Description1',
                'author': 'Author1',
                'author_email': 'author1@example.com',
                'license': 'MIT',
                'home_page': 'https://example.com',
                'keywords': 'example, package',
                'classifiers': ['Development Status :: 4 - Beta'],
                'requires_python': '>=3.6',
            },
            'releases': {
                '0.9.0': [
                    {
                        'upload_time': '2021-01-01T00:00:00',
                        'upload_time_iso_8601': '2021-01-01T00:00:00Z',
                        'python_version': 'py3',
                        'url': 'https://example.com',
                        'filename': 'package-0.9.0.tar.gz',
                        'packagetype': 'sdist',
                        'md5_digest': 'abc123',
                        'digests': {'sha256': 'def456'},
                        'size': 12345
                    }
                ],
                '1.0.0': [
                    {
                        'upload_time': '2021-06-01T00:00:00',
                        'upload_time_iso_8601': '2021-06-01T00:00:00Z',
                        'python_version': 'py3',
                        'url': 'https://example.com',
                        'filename': 'package-1.0.0.tar.gz',
                        'packagetype': 'sdist',
                        'md5_digest': 'ghi789',
                        'digests': {'sha256': 'jkl012'},
                        'size': 23456
                    }
                ],
            },
            'requires_dist': ['requests', 'beautifulsoup4'],
            'urls': [{'url': 'https://example.com/package-1.0.0.tar.gz'}],
        }

        mock_response2 = Mock()
        mock_response2.raise_for_status.return_value = None
        mock_response2.json.return_value = {
            'info': {
                'name': 'Package2',
                'version': '2.0.0',
                'summary': 'Description2',
                'author': 'Author2',
                'author_email': 'author2@example.com',
                'license': 'MIT',
                'home_page': 'https://example.com',
                'keywords': 'example, package',
                'classifiers': ['Development Status :: 5 - Production/Stable'],
                'requires_python': '>=3.6',
            },
            'releases': {
                '1.0.0': [
                    {
                        'upload_time': '2021-01-01T00:00:00',
                        'upload_time_iso_8601': '2021-01-01T00:00:00Z',
                        'python_version': 'py3',
                        'url': 'https://example.com',
                        'filename': 'package-1.0.0.tar.gz',
                        'packagetype': 'sdist',
                        'md5_digest': 'abc123',
                        'digests': {'sha256': 'def456'},
                        'size': 12345
                    }
                ],
                '2.0.0': [
                    {
                        'upload_time': '2021-06-01T00:00:00',
                        'upload_time_iso_8601': '2021-06-01T00:00:00Z',
                        'python_version': 'py3',
                        'url': 'https://example.com',
                        'filename': 'package-2.0.0.tar.gz',
                        'packagetype': 'sdist',
                        'md5_digest': 'ghi789',
                        'digests': {'sha256': 'jkl012'},
                        'size': 23456
                    }
                ],
            },
            'requires_dist': ['requests', 'beautifulsoup4'],
            'urls': [{'url': 'https://example.com/package-2.0.0.tar.gz'}],
        }

        mock_get.side_effect = [mock_response1, mock_response2]
        yield mock_get


@pytest.fixture
def mock_get_package_details_error() -> Generator[Union[MagicMock, AsyncMock], Any, None]:
    """Fixture to mock requests.get for get_package_details error case."""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.RequestException("Request error")
        yield mock_get


@pytest.fixture
def mock_get_all_packages_details_success() -> Generator[Union[MagicMock, AsyncMock], Any, None]:
    """Fixture to mock requests.get for get_all_packages_details success case."""
    with patch('requests.get') as mock_get:
        mock_response_user = Mock()
        mock_response_user.raise_for_status.return_value = None
        mock_response_user.text = '''
        <a class="package-snippet">
            <h3 class="package-snippet__title">Package1</h3>
            <p class="package-snippet__description">Description1</p>
        </a>
        <a class="package-snippet">
            <h3 class="package-snippet__title">Package2</h3>
            <p class="package-snippet__description">Description2</p>
        </a>
        '''
        mock_response_package1 = Mock()
        mock_response_package1.raise_for_status.return_value = None
        mock_response_package1.json.return_value = {
            'info': {
                'name': 'Package1',
                'version': '1.0.0',
                'summary': 'Description1',
                'author': 'Author1',
                'author_email': 'author1@example.com',
                'license': 'MIT',
                'home_page': 'https://example.com',
                'keywords': 'example, package',
                'classifiers': ['Development Status :: 4 - Beta'],
                'requires_python': '>=3.6',
            },
            'releases': {
                '0.9.0': [
                    {
                        'upload_time': '2021-01-01T00:00:00',
                        'upload_time_iso_8601': '2021-01-01T00:00:00Z',
                        'python_version': 'py3',
                        'url': 'https://example.com',
                        'filename': 'package-0.9.0.tar.gz',
                        'packagetype': 'sdist',
                        'md5_digest': 'abc123',
                        'digests': {'sha256': 'def456'},
                        'size': 12345
                    }
                ],
                '1.0.0': [
                    {
                        'upload_time': '2021-06-01T00:00:00',
                        'upload_time_iso_8601': '2021-06-01T00:00:00Z',
                        'python_version': 'py3',
                        'url': 'https://example.com',
                        'filename': 'package-1.0.0.tar.gz',
                        'packagetype': 'sdist',
                        'md5_digest': 'ghi789',
                        'digests': {'sha256': 'jkl012'},
                        'size': 23456
                    }
                ],
            },
            'requires_dist': ['requests', 'beautifulsoup4'],
            'urls': [{'url': 'https://example.com/package-1.0.0.tar.gz'}],
        }
        mock_response_package2 = Mock()
        mock_response_package2.raise_for_status.return_value = None
        mock_response_package2.json.return_value = {
            'info': {
                'name': 'Package2',
                'version': '2.0.0',
                'summary': 'Description2',
                'author': 'Author2',
                'author_email': 'author2@example.com',
                'license': 'MIT',
                'home_page': 'https://example.com',
                'keywords': 'example, package',
                'classifiers': ['Development Status :: 5 - Production/Stable'],
                'requires_python': '>=3.6',
            },
            'releases': {
                '1.0.0': [
                    {
                        'upload_time': '2021-01-01T00:00:00',
                        'upload_time_iso_8601': '2021-01-01T00:00:00Z',
                        'python_version': 'py3',
                        'url': 'https://example.com',
                        'filename': 'package-1.0.0.tar.gz',
                        'packagetype': 'sdist',
                        'md5_digest': 'abc123',
                        'digests': {'sha256': 'def456'},
                        'size': 12345
                    }
                ],
                '2.0.0': [
                    {
                        'upload_time': '2021-06-01T00:00:00',
                        'upload_time_iso_8601': '2021-06-01T00:00:00Z',
                        'python_version': 'py3',
                        'url': 'https://example.com',
                        'filename': 'package-2.0.0.tar.gz',
                        'packagetype': 'sdist',
                        'md5_digest': 'ghi789',
                        'digests': {'sha256': 'jkl012'},
                        'size': 23456
                    }
                ],
            },
            'requires_dist': ['requests', 'beautifulsoup4'],
            'urls': [{'url': 'https://example.com/package-2.0.0.tar.gz'}],
        }
        mock_get.side_effect = [mock_response_user, mock_response_package1, mock_response_package2]
        yield mock_get
