"""Module with exceptions for the GitHub source."""


class GitHubExceptions(Exception):
    """Base class for all exceptions related to the GitHub Source."""


class GitHubInvalidRepoException(GitHubExceptions):
    """Exception when a invalid repository is given."""