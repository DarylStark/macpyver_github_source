"""Moduel that contains the GitHub source classes.

There are two GitHub source classes; one to retrieve the versions from the tags
of repositories, one to retrieve the versions from the releases of
repositories.
"""

from requests import get

from macpyver_core.model import Version
from macpyver_core.version_source import VersionSource

from .exceptions import GitHubInvalidRepoException


class GitHubReleasesSource(VersionSource):
    """Class to retrieve version from GitHub releases.

    Will retrieve the releases from GitHub for a specific repository. For this
    to work, the `github_repository` attribute of the given `software` object
    has to be set.
    """
    # pylint: disable=too-few-public-methods

    def _convert_github_release_to_version(
            self,
            github_release: dict) -> Version:
        """Convert a GitHub release to a `Version` object.

        When retrieving GitHub releases, we get dictionaries back. These should
        be converted to Version objects.

        Args:
            github_release: the dict object we get from GitHub API.

        Returns:
            The created Version object.
        """
        name = github_release['name']
        if name == '':
            name = github_release['tag_name']
        return Version(
            version=name,
            release_datetime=github_release.get('published_at', None))

    def get_all_versions(self) -> list[Version]:
        """Retrieve all releases from GitHub.

        Retrieves all releases from GitHub, converts them to `Version` objects
        and puts them in a list to return. For this to work, the
        `github_repository` key has to be set in the `extra_information`
        attribute from the Software object. This has to be in the
        `<Username>/<Repo>` form.

        Returns:
            A list with Version objects for the specific software.

        Raises:
            GitHubInvalidRepoException: when the given repository is invalid.
        """
        repo = self.software.extra_information.get('github_repository', None)
        if not isinstance(repo, str):
            raise GitHubInvalidRepoException('Invalid repository given')

        releases = get(
            url=f'https://api.github.com/repos/{repo}/releases?per_page=100',
            headers={
                'Accept': 'application/vnd.github+json',
                'X-GitHub-Api-Version': '2022-11-28'},
            timeout=30)

        return_list: list[Version] = []
        for release in releases.json():
            new_version = self._convert_github_release_to_version(release)
            return_list.append(new_version)
        return return_list


class GitHubTagsSource(VersionSource):
    """Class to retrieve version from GitHub tags.

    Will retrieve the tags from GitHub for a specific repository. For this to
    work, the `github_repository` attribute of the given `software` object has
    to be set.
    """
    # pylint: disable=too-few-public-methods

    def _convert_github_tag_to_version(
            self,
            github_tag: dict) -> Version:
        """Convert a GitHub tag to a `Version` object.

        When retrieving GitHub tag, we get dictionaries back. These should be
        converted to Version objects. For this to work, the `github_repository`
        key has to be set in the `extra_information` attribute from the
        Software object. This has to be in the `<Username>/<Repo>` form.

        Args:
            github_tag: the dict object we get from GitHub API.

        Returns:
            The created Version object.
        """
        name = github_tag['name']
        return Version(version=name)

    def get_all_versions(self) -> list[Version]:
        """Retrieve all tags from GitHub.

        Retrieves all tags from GitHub, converts them to `Version` objects and
        puts them in a list to return.

        Returns:
            A list with Version objects for the specific software.

        Raises:
            GitHubInvalidRepoException: when the given repository is invalid.
        """
        repo = self.software.extra_information.get('github_repository', None)
        if not isinstance(repo, str):
            raise GitHubInvalidRepoException('Invalid repository given')

        tags = get(
            url=f'https://api.github.com/repos/{repo}/tags?per_page=100',
            headers={
                'Accept': 'application/vnd.github+json',
                'X-GitHub-Api-Version': '2022-11-28'},
            timeout=30)

        return_list: list[Version] = []
        for tag in tags.json():
            new_version = self._convert_github_tag_to_version(tag)
            return_list.append(new_version)
        return return_list
