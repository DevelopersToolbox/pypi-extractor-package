import json

from wolfsoftware.pypi_extractor import PyPiExtractor, PyPiExtractorError


def get_package_list(username="wolfsoftware"):
    """
    Retrieves a list of packages for the specified user.

    Args:
        username (str): Username to fetch the PyPi packages for.
    
    Returns:
        list: A sorted list of package names.
    """
    pypi_info = PyPiExtractor(verbose=True)
    pypi_info.set_username(username)

    try:
        packages_details = pypi_info.get_all_packages_details()
        return(packages_details)
    except PyPiExtractorError as e:
        print(f"An error occurred while fetching packages: {e.message}")
        return []


def main():
    packages = get_package_list()
    print(packages)


if __name__ == "__main__":
    main()
