"""
This test module provides unit tests for the PyPI Package Info module using pytest.

It includes tests for versioning and various functionality tests for the PyPIPackageInfo class.
"""

from typing import Any, Dict, List, Optional
import importlib.metadata

import pytest

from wolfsoftware.pypi_extractor import PyPIPackageInfo, PyPIPackageInfoError  # pylint: disable=unused-import
from .testconf import (  # noqa: F401  pylint: disable=unused-import
    mock_get_user_packages_success,
    mock_get_user_packages_error,
    mock_get_package_details_success,
    mock_get_package_details_error,
    mock_get_all_packages_details_success
)


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
    pypi_info = PyPIPackageInfo()

    with pytest.raises(PyPIPackageInfoError, match="Username must be set before fetching packages"):
        pypi_info.get_user_packages()

    with pytest.raises(PyPIPackageInfoError, match="Username must be set before fetching package details"):
        pypi_info.get_all_packages_details()


def test_set_username() -> None:
    """
    Test setting the username after initialization.

    This test verifies that the username can be set after initializing the PyPIPackageInfo class,
    and that it functions correctly with the set username.
    """
    pypi_info = PyPIPackageInfo()
    pypi_info.set_username("testuser")
    assert pypi_info.username == "testuser"  # nosec: B101


def test_set_username_with_invalid_value() -> None:
    """
    Test setting the username with an invalid value.

    This test verifies that setting the username to an empty string raises a PyPIPackageInfoError.
    """
    pypi_info = PyPIPackageInfo()

    with pytest.raises(PyPIPackageInfoError, match="Username must be provided"):
        pypi_info.set_username("")


def test_get_user_packages_success(mock_get_user_packages_success) -> None:  # noqa: F811  pylint: disable=redefined-outer-name, unused-argument
    """
    Test get_user_packages method for a successful case.

    This test uses the mock_get_user_packages_success fixture to mock requests.get method
    to return a successful response and verifies that the get_user_packages method returns
    the expected list of packages.
    """
    pypi_info = PyPIPackageInfo("testuser")
    packages: List = pypi_info.get_user_packages()

    assert len(packages) == 2  # nosec: B101
    assert packages[0]['name'] == "Package1"  # nosec: B101
    assert packages[0]['summary'] == "Description1"  # nosec: B101
    assert packages[1]['name'] == "Package2"  # nosec: B101
    assert packages[1]['summary'] == "Description2"  # nosec: B101


def test_get_user_packages_error(mock_get_user_packages_error) -> None:  # noqa: F811  pylint: disable=redefined-outer-name, unused-argument
    """
    Test get_user_packages method when there is an error.

    This test uses the mock_get_user_packages_error fixture to mock requests.get method
    to raise an exception and verifies that the get_user_packages method raises a PyPIPackageInfoError.
    """
    pypi_info = PyPIPackageInfo("testuser")

    with pytest.raises(PyPIPackageInfoError, match="Error fetching user profile: Request error"):
        pypi_info.get_user_packages()


def test_get_package_details_success(mock_get_package_details_success) -> None:  # noqa: F811  pylint: disable=redefined-outer-name, unused-argument
    """
    Test get_package_details method for a successful case.

    This test uses the mock_get_package_details_success fixture to mock requests.get method
    to return a successful response and verifies that the get_package_details method returns
    the expected package details.
    """
    pypi_info = PyPIPackageInfo("testuser")
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


def test_get_package_details_error(mock_get_package_details_error) -> None:  # noqa: F811  pylint: disable=redefined-outer-name, unused-argument
    """
    Test get_package_details method when there is an error.

    This test uses the mock_get_package_details_error fixture to mock requests.get method
    to raise an exception and verifies that the get_package_details method raises a PyPIPackageInfoError.
    """
    pypi_info = PyPIPackageInfo("testuser")

    with pytest.raises(PyPIPackageInfoError, match="Error fetching package details: Request error"):
        pypi_info.get_package_details("Package1")


def test_get_all_packages_details_success(mock_get_all_packages_details_success) -> None:  # noqa: F811  pylint: disable=redefined-outer-name, unused-argument
    """
    Test get_all_packages_details method for a successful case.

    This test uses the mock_get_all_packages_details_success fixture to mock requests.get method
    to return a successful response for both user packages and package details, and verifies that
    the get_all_packages_details method returns the expected list of detailed package information.
    """
    pypi_info = PyPIPackageInfo("testuser")
    details: List = pypi_info.get_all_packages_details()

    assert len(details) == 2  # nosec: B101
    assert details[0]['name'] == "Package1"  # nosec: B101
    assert details[1]['name'] == "Package2"  # nosec: B101
