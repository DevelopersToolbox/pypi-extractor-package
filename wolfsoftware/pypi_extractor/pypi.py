"""
This module defines the PyPIPackageInfo class for fetching and processing package details from PyPI.

Classes:
    - PyPIPackageInfo: A class to fetch and process package details for a given PyPI user.
"""
from typing import Any, Dict, List, Optional

import json
import requests
from bs4 import BeautifulSoup

from .exceptions import PyPIPackageInfoError


class PyPIPackageInfo:
    """
    A class to fetch and process package details for a given PyPI user.

    Attributes:
        username (Optional[str]): The PyPI username whose packages are to be fetched.
    """

    def __init__(self, username: Optional[str] = None) -> None:
        """
        Initialize the PyPIPackageInfo. The username can be set during initialization or later using the set_username method.

        Arguments:
            username (Optional[str]): The PyPI username. Default is None.
        """
        self.username: Optional[str] = username

    def set_username(self, username: str) -> None:
        """
        Set the PyPI username.

        Arguments:
            username (str): The PyPI username.

        Raises:
            PyPIPackageInfoError: If the username is not provided.
        """
        if not username:
            raise PyPIPackageInfoError("Username must be provided")
        self.username = username

    def get_user_packages(self) -> List[Dict[str, str]]:
        """
        Fetch the list of packages for the given PyPI user.

        Returns:
            list: A list of dictionaries containing package names and summaries.

        Raises:
            PyPIPackageInfoError: If the username is not set or if there is an error fetching or parsing the user profile.
        """
        if not self.username:
            raise PyPIPackageInfoError("Username must be set before fetching packages")

        profile_url: str = "https://pypi.org/user/" + self.username + "/"
        try:
            response: requests.Response = requests.get(profile_url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise PyPIPackageInfoError(f"Error fetching user profile: {e}") from e

        soup = BeautifulSoup(response.text, 'html.parser')
        packages: List[Dict[str, str]] = []
        for project in soup.find_all('a', class_='package-snippet'):
            try:
                package_name: str = project.find('h3', class_='package-snippet__title').text.strip()
                summary: str = project.find('p', class_='package-snippet__description').text.strip()
                packages.append({'name': package_name, 'summary': summary})
            except AttributeError as e:
                raise PyPIPackageInfoError(f"Error parsing package details: {e}") from e

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
            raise PyPIPackageInfoError(f"Error fetching package details: {e}") from e

        try:
            package_data: Any = response.json()
        except json.JSONDecodeError as e:
            raise PyPIPackageInfoError(f"Error decoding JSON response: {e}") from e

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
            raise PyPIPackageInfoError("Username must be set before fetching package details")

        try:
            packages: List[Dict[str, str]] = self.get_user_packages()
        except PyPIPackageInfoError as e:
            raise PyPIPackageInfoError(f"Failed to get user packages: {e}") from e

        if not packages:
            raise PyPIPackageInfoError(f"No packages found for user/organization '{self.username}'")

        detailed_packages: List[Dict[str, Any]] = []
        for package in packages:
            try:
                details: Dict[str, Any] = self.get_package_details(package['name'])
                detailed_packages.append(details)
            except PyPIPackageInfoError as e:
                raise PyPIPackageInfoError(f"Failed to get details for package '{package['name']}': {e}") from e
        return detailed_packages
