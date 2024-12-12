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


def raise_error(*args, **kwargs):
    """Raise an error if the real playwright gets used."""
    raise RuntimeError("Real Playwright should not be invoked!")


@pytest.fixture
def mock_playwright() -> Generator[MagicMock, None, None]:
    """Mock the Playwright sync API."""
    with patch('wolfsoftware.pypi_extractor.pypi.sync_playwright') as mock_sync_playwright:
        mock_playwright_instance = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        # Mock page.goto() and page.wait_for_selector()
        mock_page.goto.return_value = None
        mock_page.wait_for_selector.return_value = None

        # Mock page.query_selector_all() to return simulated package elements
        def mock_query_selector_all(selector):
            """Handle mocking the right data."""
            if selector == 'a.package-snippet':
                return [
                    MagicMock(query_selector=MagicMock(side_effect=[
                        MagicMock(inner_text=MagicMock(return_value="Package1")),
                        MagicMock(inner_text=MagicMock(return_value="Description1")),
                    ])),
                    MagicMock(query_selector=MagicMock(side_effect=[
                        MagicMock(inner_text=MagicMock(return_value="Package2")),
                        MagicMock(inner_text=MagicMock(return_value="Description2")),
                    ])),
                ]
            return []
        mock_page.query_selector_all.side_effect = mock_query_selector_all

        mock_context.new_page.return_value = mock_page
        mock_browser.new_context.return_value = mock_context
        mock_playwright_instance.chromium.launch.return_value = mock_browser
        mock_sync_playwright.return_value.__enter__.return_value = mock_playwright_instance
        yield mock_sync_playwright


@pytest.fixture
def mock_playwright_error() -> Generator[MagicMock, None, None]:
    """Fixture to mock Playwright with an error scenario."""
    with patch('wolfsoftware.pypi_extractor.pypi.sync_playwright') as mock_sync_playwright:
        mock_playwright_instance = MagicMock()
        mock_playwright_instance.chromium.launch.side_effect = Exception("Playwright error")
        mock_sync_playwright.return_value.__enter__.return_value = mock_playwright_instance
        yield mock_sync_playwright


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
def mock_get_all_packages_details_success() -> Generator[MagicMock, None, None]:
    """Mock requests.get for get_all_packages_details success case."""
    with patch('requests.get') as mock_get:
        # Mock response for the user packages API
        mock_response_user = MagicMock()
        mock_response_user.raise_for_status.return_value = None
        mock_response_user.json.return_value = {
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
                '1.0.0': [
                    {
                        'upload_time': '2021-06-01T00:00:00',
                        'upload_time_iso_8601': '2021-06-01T00:00:00Z',
                        'python_version': 'py3',
                        'url': 'https://example.com/package-1.0.0.tar.gz',
                        'filename': 'package-1.0.0.tar.gz',
                        'packagetype': 'sdist',
                        'md5_digest': 'abc123',
                        'digests': {'sha256': 'def456'},
                        'size': 12345
                    }
                ]
            },
            'requires_dist': ['requests', 'beautifulsoup4'],
            'urls': [{'url': 'https://example.com/package-1.0.0.tar.gz'}],
        }

        # Simulate two different package details responses
        mock_response_package1 = MagicMock()
        mock_response_package1.raise_for_status.return_value = None
        mock_response_package1.json.return_value = mock_response_user.json.return_value

        mock_response_package2 = MagicMock()
        mock_response_package2.raise_for_status.return_value = None
        mock_response_package2.json.return_value = {
            'info': {
                'name': 'Package2',
                'version': '2.0.0',
                'summary': 'Description2',
                'author': 'Author2',
                'author_email': 'author2@example.com',
                'license': 'MIT',
                'home_page': 'https://example.com/package2',
                'keywords': 'example, package2',
                'classifiers': ['Development Status :: 5 - Production/Stable'],
                'requires_python': '>=3.6',
            },
            'releases': {
                '2.0.0': [
                    {
                        'upload_time': '2022-06-01T00:00:00',
                        'upload_time_iso_8601': '2022-06-01T00:00:00Z',
                        'python_version': 'py3',
                        'url': 'https://example.com/package-2.0.0.tar.gz',
                        'filename': 'package-2.0.0.tar.gz',
                        'packagetype': 'sdist',
                        'md5_digest': 'ghi789',
                        'digests': {'sha256': 'jkl012'},
                        'size': 23456
                    }
                ]
            },
            'requires_dist': ['requests', 'beautifulsoup4'],
            'urls': [{'url': 'https://example.com/package-2.0.0.tar.gz'}],
        }

        # Simulate the sequence of requests
        mock_get.side_effect = [mock_response_package1, mock_response_package2]
        yield mock_get
