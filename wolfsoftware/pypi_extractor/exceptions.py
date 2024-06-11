"""
This module defines custom exceptions for the PyPI package info retriever.

Classes:
    - PyPIPackageInfoError: A custom exception class for errors in the PyPIPackageInfo class.
"""


class PyPIPackageInfoError(Exception):
    """
    Custom exception class for PyPIPackageInfo errors.

    Attributes:
        message (str): The error message to be displayed.
    """

    def __init__(self, message: str) -> None:
        """
        Initialize the PyPIPackageInfoError with a given message.

        Parameters:
            message (str): The error message to be displayed.
        """
        super().__init__(message)
        self.message: str = message
