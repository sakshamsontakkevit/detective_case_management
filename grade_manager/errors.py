"""Custom exceptions so error messages stay clear and specific."""


class GradeManagerError(Exception):
    """Base class for all errors raised by this project."""


class ValidationError(GradeManagerError):
    """Raised when user input is not valid."""


class StudentNotFoundError(GradeManagerError):
    """Raised when a registration number is not in the system."""


class DuplicateStudentError(GradeManagerError):
    """Raised when adding a student that already exists."""
