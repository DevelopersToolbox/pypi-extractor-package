"""
This module defines the PyPiExtractor class for fetching and processing package details from PyPI.

Classes:
    - PyPiExtractor: A class to fetch and process package details for a given PyPI user.
"""
from typing import Any, Dict, List, Optional

import json
import subprocess  # nosec: B404

import requests

from playwright.sync_api import sync_playwright

from .exceptions import PyPiExtractorError


class PyPiExtractor:
    """
    A class to fetch and process package details for a given PyPI user.

    Attributes:
        username (Optional[str]): The PyPI username whose packages are to be fetched.
    """

    def __init__(self, username: Optional[str] = None, verbose: Optional[bool] = False, auto_install: Optional[bool] = False) -> None:
        """
        Initialize the PyPIPackageInfo. The username can be set during initialization or later using the set_username method.

        Arguments:
            username (Optional[str]): The PyPI username. Default is None.
        """
        self.username: Optional[str] = username
        self.verbose: Optional[bool] = verbose
        self.auto_install: Optional[bool] = auto_install

    def set_username(self, username: str) -> None:
        """
        Set the PyPI username.

        Arguments:
            username (str): The PyPI username.

        Raises:
            PyPIPackageInfoError: If the username is not provided.
        """
        if not username:
            raise PyPiExtractorError("Username must be provided")
        self.username = username

    def enable_verbose(self) -> None:
        """Enable verbose output."""
        self.verbose = True

    def enable_auto_install(self) -> None:
        """Enable auto_install."""
        self.auto_install = True

    def ensure_playwright_browsers_and_deps(self) -> None:
        """Ensure Playwright browsers and system dependencies are installed silently."""
        if self.auto_install:
            try:
                # Install Playwright browsers silently
                subprocess.run(["playwright", "install"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # nosec: B603 B607
                if self.verbose:
                    print("Playwright browsers installed successfully.")

                # Install system-level dependencies silently (Linux only)
                subprocess.run(["playwright", "install-deps"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # nosec: B603 B607
                if self.verbose:
                    print("System dependencies installed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error during Playwright setup: {e}")
                raise

    def get_user_packages(self) -> List[Dict[str, str]]:
        """
        Fetch the list of packages for the given PyPI user.

        Returns:
            list: A list of dictionaries containing package names and summaries.

        Raises:
            PyPiExtractorError: If the username is not set or if there is an error fetching or parsing the user profile.
        """
        if not self.username:
            raise PyPiExtractorError("Username must be set before fetching packages")

        profile_url: str = "https://pypi.org/user/" + self.username + "/"
        packages: List[Dict[str, str]] = []

        try:
            self.ensure_playwright_browsers_and_deps()

            with sync_playwright() as p:
                browser: Any = p.chromium.launch(headless=True)
                context: Any = browser.new_context()
                page: Any = context.new_page()

                page.goto(profile_url)
                page.wait_for_selector('.package-snippet')

                elements: Any = page.query_selector_all('a.package-snippet')
                for element in elements:
                    package_name: Any = element.query_selector('h3.package-snippet__title').inner_text().strip()
                    summary: Any = element.query_selector('p.package-snippet__description').inner_text().strip()
                    packages.append({'name': package_name, 'summary': summary})

                browser.close()
        except Exception as e:
            raise PyPiExtractorError(f"Error fetching user profile with Playwright: {e}") from e

        return packages

    def get_package_details(self, package_name: str) -> Dict[str, Any]:
        """
        Fetch detailed information for a specific package.

        Arguments:
            package_name (str): The name of the package.

        Returns:
            dict: A dictionary containing detailed information about the package.

        Raises:
            PyPIPackageInfoError: If there is an error fetching or parsing the package details.
        """
        url: str = "https://pypi.org/pypi/" + package_name + "/json"
        try:
            response: requests.Response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise PyPiExtractorError(f"Error fetching package details: {e}") from e

        try:
            package_data: Any = response.json()
        except json.JSONDecodeError as e:
            raise PyPiExtractorError(f"Error decoding JSON response: {e}") from e

        info: Any = package_data.get('info', {})
        current_version: str = info.get('version')

        # Gather details of all older versions excluding the current version
        older_versions_details: List[Dict[str, Any]] = [
            {
                'version': version,
                'upload_time': release[0]['upload_time'] if release else None,
                'upload_time_iso_8601': release[0]['upload_time_iso_8601'] if release else None,
                'python_version': release[0]['python_version'] if release else None,
                'url': release[0]['url'] if release else None,
                'filename': release[0]['filename'] if release else None,
                'packagetype': release[0]['packagetype'] if release else None,
                'md5_digest': release[0]['md5_digest'] if release else None,
                'sha256_digest': release[0]['digests']['sha256'] if 'digests' in release[0] else None,
                'size': release[0]['size'] if release else None,
            } for version, release in package_data.get('releases', {}).items() if version != current_version
        ]

        details: Dict[str, Any] = {
            'name': info.get('name'),
            'version': current_version,
            'summary': info.get('summary'),
            'author': info.get('author'),
            'author_email': info.get('author_email'),
            'license': info.get('license'),
            'home_page': info.get('home_page'),
            'keywords': info.get('keywords'),
            'classifiers': info.get('classifiers'),
            'requires_python': info.get('requires_python'),
            'dependencies': package_data.get('requires_dist', []),
            'downloads': package_data.get('urls', []),
            'older_versions': older_versions_details
        }

        return details

    def get_all_packages_details(self) -> List[Dict[str, Any]]:
        """
        Fetch detailed information for all packages of the given PyPI user.

        Returns:
            list: A list of dictionaries containing detailed information about each package.

        Raises:
            PyPIPackageInfoError: If there is an error fetching or processing the package details.
        """
        if not self.username:
            raise PyPiExtractorError("Username must be set before fetching package details")

        try:
            packages: List[Dict[str, str]] = self.get_user_packages()
        except PyPiExtractorError as e:
            raise PyPiExtractorError(f"Failed to get user packages: {e}") from e

        if not packages:
            raise PyPiExtractorError(f"No packages found for user/organization '{self.username}'")

        detailed_packages: List[Dict[str, Any]] = []
        for package in packages:
            try:
                details: Dict[str, Any] = self.get_package_details(package['name'])
                detailed_packages.append(details)
            except PyPiExtractorError as e:
                raise PyPiExtractorError(f"Failed to get details for package '{package['name']}': {e}") from e
        return detailed_packages
