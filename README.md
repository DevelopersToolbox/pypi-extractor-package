<!-- markdownlint-disable -->
<p align="center">
    <a href="https://github.com/DevelopersToolbox/">
        <img src="https://cdn.wolfsoftware.com/assets/images/github/organisations/developerstoolbox/black-and-white-circle-256.png" alt="DevelopersToolbox logo" />
    </a>
    <br />
    <a href="https://github.com/DevelopersToolbox/pypi-extractor-package/actions/workflows/cicd.yml">
        <img src="https://img.shields.io/github/actions/workflow/status/DevelopersToolbox/pypi-extractor-package/cicd.yml?branch=master&label=build%20status&style=for-the-badge" alt="Github Build Status" />
    </a>
    <a href="https://github.com/DevelopersToolbox/pypi-extractor-package/blob/master/LICENSE.md">
        <img src="https://img.shields.io/github/license/DevelopersToolbox/pypi-extractor-package?color=blue&label=License&style=for-the-badge" alt="License">
    </a>
    <a href="https://github.com/DevelopersToolbox/pypi-extractor-package">
        <img src="https://img.shields.io/github/created-at/DevelopersToolbox/pypi-extractor-package?color=blue&label=Created&style=for-the-badge" alt="Created">
    </a>
    <br />
    <a href="https://github.com/DevelopersToolbox/pypi-extractor-package/releases/latest">
        <img src="https://img.shields.io/github/v/release/DevelopersToolbox/pypi-extractor-package?color=blue&label=Latest%20Release&style=for-the-badge" alt="Release">
    </a>
    <a href="https://github.com/DevelopersToolbox/pypi-extractor-package/releases/latest">
        <img src="https://img.shields.io/github/release-date/DevelopersToolbox/pypi-extractor-package?color=blue&label=Released&style=for-the-badge" alt="Released">
    </a>
    <a href="https://github.com/DevelopersToolbox/pypi-extractor-package/releases/latest">
        <img src="https://img.shields.io/github/commits-since/DevelopersToolbox/pypi-extractor-package/latest.svg?color=blue&style=for-the-badge" alt="Commits since release">
    </a>
    <br />
    <a href="https://github.com/DevelopersToolbox/pypi-extractor-package/blob/master/.github/CODE_OF_CONDUCT.md">
        <img src="https://img.shields.io/badge/Code%20of%20Conduct-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/DevelopersToolbox/pypi-extractor-package/blob/master/.github/CONTRIBUTING.md">
        <img src="https://img.shields.io/badge/Contributing-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/DevelopersToolbox/pypi-extractor-package/blob/master/.github/SECURITY.md">
        <img src="https://img.shields.io/badge/Report%20Security%20Concern-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/DevelopersToolbox/pypi-extractor-package/issues">
        <img src="https://img.shields.io/badge/Get%20Support-blue?style=for-the-badge" />
    </a>
</p>

## Overview

PyPI Extractor is a Python package designed to fetch and process detailed information about packages hosted on the
Python Package Index (PyPI). This package is particularly useful for users who want to retrieve and analyze metadata for packages
maintained by a specific PyPI user.

## Features

- Retrieve a list of packages maintained by a specific PyPI user.
- Fetch detailed metadata for each package, including versions, author information, dependencies, and more.
- Custom exceptions for handling errors gracefully.
- Option to set the PyPI username after initializing the class.

## Installation

You can install the package using pip:

```sh
pip install wolfsoftware.pypi-extractor
```

## Usage

### Basic Usage

Here's a basic example of how to use the PyPI Extractor:

```python
from wolfsoftware.pypi_extractor import PyPIPackageInfo

# Initialize without username
pypi_info = PyPIPackageInfo()

# Set username later
pypi_info.set_username("your_pypi_username")

# Get detailed information for all packages
try:
    packages_details = pypi_info.get_all_packages_details()
    print(packages_details)
except PyPIPackageInfoError as e:
    print(f"An error occurred: {e.message}")
```

### Setting Username During Initialization

You can also set the username during initialization:

```python
pypi_info = PyPIPackageInfo("your_pypi_username")
```

### Retrieving User Packages

You can retrieve a list of packages maintained by a specific user:

```python
packages = pypi_info.get_user_packages()
print(packages)
```

### Retrieving Package Details

To get detailed information about a specific package:

```python
package_details = pypi_info.get_package_details("package_name")
print(package_details)
```

## API Reference

### Classes

#### `PyPIPackageInfo`

A class to fetch and process package details for a given PyPI user.

##### `__init__(self, username: str)`

- Initializes the `PyPIPackageInfo` with a username.
- Parameters:
  - `username` (str): The PyPI username.
- Raises:
  - `PyPIPackageInfoError`: If the username is not provided.

##### `set_username(self, username: str)`

- Sets the PyPI username.
- Parameters:
  - `username` (str): The PyPI username.
- Raises:
  - `PyPIPackageInfoError`: If the username is not provided.

##### `get_user_packages(self) -> list`

- Fetches the list of packages for the given PyPI user.
- Returns:
  - `list`: A list of dictionaries containing package names and summaries.
- Raises:
  - `PyPIPackageInfoError`: If there is an error fetching or parsing the user profile.

##### `get_package_details(self, package_name: str) -> dict`

- Fetches detailed information for a specific package.
- Parameters:
  - `package_name` (str): The name of the package.
- Returns:
  - `dict`: A dictionary containing detailed information about the package.
- Raises:
  - `PyPIPackageInfoError`: If there is an error fetching or parsing the package details.

##### `get_all_packages_details(self) -> list`

- Fetches detailed information for all packages of the given PyPI user.
- Returns:
  - `list`: A list of dictionaries containing detailed information about each package.
- Raises:
  - `PyPIPackageInfoError`: If there is an error fetching or processing the package details.

#### `PyPIPackageInfoError`

Custom exception class for `PyPIPackageInfo` errors.

<br />
<p align="right"><a href="https://wolfsoftware.com/"><img src="https://img.shields.io/badge/Created%20by%20Wolf%20on%20behalf%20of%20Wolf%20Software-blue?style=for-the-badge" /></a></p>
