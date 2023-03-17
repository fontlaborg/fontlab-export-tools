from git import Repo
from pathlib import Path
import yaml
from .utils import read_config

from datetime import datetime


def _commit_message():
    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    return f"Commit on {timestamp_str}"


def clone_or_pull(config_path):
    config = read_config(config_path)
    public_repo_folder = config.public_repo_folder
    public_repo_url = config.public_repo_url
    if not public_repo_folder.exists():
        Repo.clone_from(public_repo_url, public_repo_folder)
    else:
        repo = Repo(public_repo_folder)
        origin = repo.remote(name="origin")
        origin.pull()


def commit_and_push(config_path, msg=None):
    commit_message = msg or _commit_message()
    # Read the config file
    config = read_config(config_path)
    public_repo_folder = config.public_repo_folder
    public_repo_url = config.public_repo_url

    # Create a GitPython repository object
    repo = Repo(public_repo_folder)

    # Add all files to the index
    repo.index.add("*")

    # Create a new commit
    repo.index.commit(commit_message)

    # Push the changes to the remote repository
    origin = repo.remote(name="origin")
    origin.push()
