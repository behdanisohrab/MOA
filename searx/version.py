# SPDX-License-Identifier: AGPL-3.0-or-later
# pylint: disable=missing-module-docstring,missing-class-docstring

import os
import logging
import importlib

# Fallback values
VERSION_STRING = "0.4"
VERSION_TAG = "0.4"
DOCKER_TAG = "0.4"
GIT_URL = "unknown"
GIT_BRANCH = "unknown"

logger = logging.getLogger("MOA")


def is_git_installed():
    try:
        from git import Repo, GitCommandError, InvalidGitRepositoryError, NoSuchPathError
        return True
    except ImportError:
        logger.error("GitPython is not installed.")
        return False


def get_latest_tag(repo_path='.'):
    try:
        from git import Repo
        repo = Repo(repo_path)
        latest_tag = repo.git.describe('--tags', '--abbrev=0')
        return latest_tag
    except (GitCommandError, InvalidGitRepositoryError) as e:
        logger.error("Error while getting the latest tag: %s", str(e))
        return "1.0.0"


def get_git_url_and_branch(repo_path='.'):
    try:
        from git import Repo
        repo = Repo(repo_path)
        git_url = next(repo.remote().urls)
        git_branch = repo.active_branch.name

        # Convert ssh URL to https URL
        if git_url.startswith("git@"):
            git_url = git_url.replace(":", "/").replace("git@", "https://")
        if git_url.endswith(".git"):
            git_url = git_url[:-4]

        return git_url, git_branch
    except (GitCommandError, InvalidGitRepositoryError) as e:
        logger.error("Error while getting the git URL & branch: %s", str(e))
        return GIT_URL, GIT_BRANCH


def get_git_version(repo_path='.'):
    try:
        from git import Repo
        repo = Repo(repo_path)
        git_commit = repo.head.commit
        git_commit_date = git_commit.committed_datetime.strftime('%Y.%m.%d')
        git_commit_hash = git_commit.hexsha[:7]
        latest_tag = get_latest_tag(repo_path)
        git_version = f"{git_commit_date}-{git_commit_hash}"
        return f"{git_version}-{latest_tag}", latest_tag, git_version
    except (GitCommandError, InvalidGitRepositoryError) as e:
        logger.error("Error while getting the version: %s", str(e))
        return VERSION_STRING, VERSION_TAG, VERSION_STRING


try:
    vf = importlib.import_module('searx.version_frozen')
    VERSION_STRING, VERSION_TAG, DOCKER_TAG, GIT_URL, GIT_BRANCH = (
        vf.VERSION_STRING,
        vf.VERSION_TAG,
        vf.DOCKER_TAG,
        vf.GIT_URL,
        vf.GIT_BRANCH,
    )
except ImportError:
    if is_git_installed():
        VERSION_STRING, VERSION_TAG, DOCKER_TAG = get_git_version()
        GIT_URL, GIT_BRANCH = get_git_url_and_branch()
    else:
        logger.error(
            "Git is not installed or the directory is not a git repository, falling back to default values.")

logger.info("version: %s", VERSION_STRING)

if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 2 and sys.argv[1] == "freeze":
        python_code = f"""# SPDX-License-Identifier: AGPL-3.0-or-later
# pylint: disable=missing-module-docstring
# This file is generated automatically by searx/version.py

VERSION_STRING = "{VERSION_STRING}"
VERSION_TAG = "{VERSION_TAG}"
DOCKER_TAG = "{DOCKER_TAG}"
GIT_URL = "{GIT_URL}"
GIT_BRANCH = "{GIT_BRANCH}"
"""
        with open(os.path.join(os.path.dirname(__file__), "version_frozen.py"), "w", encoding="utf8") as f:
            f.write(python_code)
            print(f"{f.name} created")
    else:
        shell_code = f"""
VERSION_STRING="{VERSION_STRING}"
VERSION_TAG="{VERSION_TAG}"
DOCKER_TAG="{DOCKER_TAG}"
GIT_URL="{GIT_URL}"
GIT_BRANCH="{GIT_BRANCH}"
"""
        print(shell_code)
