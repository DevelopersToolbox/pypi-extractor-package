"""
This test module provides unit tests for the PyPI Package Info module using pytest.

It includes tests for versioning and various functionality tests for the PyPIPackageInfo class.
"""

from typing import Any, Dict, List, Optional
import importlib.metadata

import pytest

from wolfsoftware.pypi_extractor import PyPiExtractor, PyPiExtractorError  # pylint: disable=unused-import, no-name-in-module


def test_version() -> None:
    """
    Test to ensure the version of the Package is set and not 'unknown'.

    This test retrieves the version of the package using importlib.metadata and asserts that the version
    is not None and not 'unknown'.
    """
    version: Optional[str] = None

    try:
        version = importlib.metadata.version('wolfsoftware.pypi_extractor')
    except importlib.metadata.PackageNotFoundError:
        version = None

    assert version is not None, "Version should be set"  # nosec: B101
    assert version != 'unknown', f"Expected version, but got {version}"  # nosec: B101


def test_init_with_empty_username() -> None:
    """
    Test initializing PyPIPackageInfo with an empty username.

    This test asserts that initializing the PyPIPackageInfo class with an empty username
    does not raise an error, and that attempting to fetch packages without setting a username
    raises a PyPIPackageInfoError.
    """
    pypi_info = PyPiExtractor()

    with pytest.raises(PyPiExtractorError, match="Username must be set before fetching packages"):
        pypi_info.get_user_packages()

    with pytest.raises(PyPiExtractorError, match="Username must be set before fetching package details"):
        pypi_info.get_all_packages_details()


def test_set_username() -> None:
    """
    Test setting the username after initialization.

    This test verifies that the username can be set after initializing the PyPiExtractor class,
    and that it functions correctly with the set username.
    """
    pypi_info = PyPiExtractor()
    pypi_info.set_username("testuser")
    assert pypi_info.username == "testuser"  # nosec: B101


def test_set_username_with_invalid_value() -> None:
    """
    Test setting the username with an invalid value.

    This test verifies that setting the username to an empty string raises a PyPiExtractorError.
    """
    pypi_info = PyPiExtractor()

    with pytest.raises(PyPiExtractorError, match="Username must be provided"):
        pypi_info.set_username("")


@pytest.mark.usefixtures("mock_playwright")
def test_get_user_packages_success() -> None:
    """Test the get_user_packages method for a successful case."""
    pypi_extractor = PyPiExtractor("testuser")
    packages = pypi_extractor.get_user_packages()

    assert len(packages) == 2
    assert packages[0]['name'] == "Package1"
    assert packages[0]['summary'] == "Description1"
    assert packages[1]['name'] == "Package2"
    assert packages[1]['summary'] == "Description2"


@pytest.mark.usefixtures("mock_playwright_error")
def test_get_user_packages_error() -> None:
    """Test the get_user_packages method when Playwright fails."""
    pypi_extractor = PyPiExtractor("testuser")
    with pytest.raises(PyPiExtractorError, match="Error fetching user profile with Playwright"):
        pypi_extractor.get_user_packages()


@pytest.mark.usefixtures("mock_get_package_details_success")
def test_get_package_details_success() -> None:
    """
    Test get_package_details method for a successful case.

    This test uses the mock_get_package_details_success fixture to mock requests.get method
    to return a successful response and verifies that the get_package_details method returns
    the expected package details.
    """
    pypi_info = PyPiExtractor("testuser")
    details: Dict[str, Any] = pypi_info.get_package_details("Package1")

    assert details['name'] == "Package1"  # nosec: B101
    assert details['version'] == "1.0.0"  # nosec: B101
    assert details['summary'] == "Description1"  # nosec: B101
    assert details['author'] == "Author1"  # nosec: B101
    assert details['author_email'] == "author1@example.com"  # nosec: B101
    assert details['license'] == "MIT"  # nosec: B101
    assert details['home_page'] == "https://example.com"  # nosec: B101
    assert details['keywords'] == "example, package"  # nosec: B101
    assert details['classifiers'] == ['Development Status :: 4 - Beta']  # nosec: B101
    assert details['requires_python'] == ">=3.6"  # nosec: B101
    assert details['dependencies'] == ['requests', 'beautifulsoup4']  # nosec: B101
    assert details['downloads'] == [{'url': 'https://example.com/package-1.0.0.tar.gz'}]  # nosec: B101
    assert len(details['older_versions']) == 1  # nosec: B101
    assert details['older_versions'][0]['version'] == "0.9.0"  # nosec: B101


@pytest.mark.usefixtures("mock_get_package_details_error")
def test_get_package_details_error() -> None:
    """
    Test get_package_details method when there is an error.

    This test uses the mock_get_package_details_error fixture to mock requests.get method
    to raise an exception and verifies that the get_package_details method raises a PyPiExtractorError.
    """
    pypi_info = PyPiExtractor("testuser")

    with pytest.raises(PyPiExtractorError, match="Error fetching package details: Request error"):
        pypi_info.get_package_details("Package1")


@pytest.mark.usefixtures("mock_playwright", "mock_get_all_packages_details_success")
def test_get_all_packages_details_success() -> None:
    """
    Test get_all_packages_details method for a successful case.

    This test uses the mock_get_all_packages_details_success fixture to mock requests.get method
    to return a successful response for both user packages and package details, and verifies that
    the get_all_packages_details method returns the expected list of detailed package information.
    """
    pypi_info = PyPiExtractor("testuser")
    details: List = pypi_info.get_all_packages_details()

    assert len(details) == 2  # nosec: B101
    assert details[0]['name'] == "Package1"  # nosec: B101
    assert details[1]['name'] == "Package2"  # nosec: B101
