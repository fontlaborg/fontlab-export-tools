from datetime import datetime
from git import Repo

from .utils import read_config


class GitHandler:
    def __init__(self, config_path):
        self.config = read_config(config_path)
        self.public_repo_folder = self.config.public_repo_folder
        self.public_repo_url = self.config.public_repo_url
        try:
            self.repo = Repo(self.public_repo_folder)
        except Exception:
            self.repo = None

    @staticmethod
    def _commit_message():
        now = datetime.now()
        timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
        return f"Commit on {timestamp_str}"

    def clone(self):
        self.repo = Repo.clone_from(self.public_repo_url, self.public_repo_folder)

    def pull(self):
        origin = self.repo.remote(name="origin")
        origin.pull()

    def clone_or_pull(self):
        if not self.public_repo_folder.exists():
            self.clone()
        else:
            self.pull()

    def commit(self, msg=None):
        commit_message = msg or self._commit_message()
        for untracked_file in self.repo.untracked_files:
            self.repo.index.add(untracked_file)
        self.repo.index.commit(commit_message)

    def push(self):
        self.repo.remote(name="origin").push()

    def commit_and_push(self, msg=None):
        self.commit(msg)
        self.push()

    def sync(self, msg=None):
        self.clone_or_pull()
        self.commit(msg)
        self.push()
