"""A utility for managing logging directories."""
__version__ = "0.5.0"

__all__ = [
    "LogDir",
]

import datetime
import json
import pickle
import warnings
from collections import namedtuple
from pathlib import Path

import toml
from dulwich.repo import Repo
from ruamel import yaml


class LogDir:
    """A utility for managing logging directories.

    Creates a logging directory on startup; comes with a handful of other handy
    methods.
    """

    def __init__(self, name, rootdir="./logs"):
        """Initializes by creating the logging directory.

        The directory is created under `rootdir` (which is created if it does
        not exist). Logging directory is named with the date, followed by the
        time, followed by the given `name` in lowercase with spaces and
        underscores replaced with dashes, for instance
        `2020-02-14_18:01:45_my-logging-dir`.

        Args:
            name (str): Customizable part of the logging directory name, e.g.
                `My cool experiment`
            rootdir (str or pathlib.Path): Root directory for all logging
                directories, e.g. `./logs/`
        """
        self._name = name

        # Create the rootdir.
        rootdir = Path(rootdir)
        if not rootdir.exists():
            rootdir.mkdir(parents=True)

        # Create the logdir.
        self._datetime = datetime.datetime.now()
        dirname = (self._datetime.strftime("%Y-%m-%d_%H-%M-%S") + "_" +
                   name.lower().replace("_", "-").replace(" ", "-"))
        self._logdir = rootdir / Path(dirname)
        self._logdir.mkdir()

    @property
    def name(self) -> str:
        """The name passed in at initialization time."""
        return self._name

    @property
    def datetime(self) -> datetime.datetime:
        """Date and time of this class's creation."""
        return self._datetime

    @property
    def logdir(self) -> Path:
        """Path to the directory itself."""
        return self._logdir

    def file(self, filename):
        """Returns a string path to the given file.

        Intermediate directories are created if they do not exist.

        The file is automatically created, so even if you do not use it, there
        will still be an empty file in the directory.

        Example:
            Basic usage:
            ```python
            logdir = LogDir("logdir")
            logdir.filepath("file.txt") # "..._logdir/file.txt"
            ```
            Creating intermediate directories:
            ```python
            logdir = LogDir("logdir")
            logdir.filepath("newdir/file.txt") # "..._logdir/newdir/file.txt"
            ```
        Args:
            filename (str or pathlib.Path): The name of the file.
        Returns:
            str: Path to the new file in the logging directory.
        """
        return str(self.pfile(filename))

    def pfile(self, filename):
        """Same as [file][logdir.LogDir.file], but returns pathlib.Path.

        Args:
            filename (str or pathlib.Path): The name of the file.
        Returns:
            pathlib.Path: Path to the new file in the logging directory.
        """
        filename = self._logdir / Path(filename)
        if not filename.parent.exists():
            filename.parent.mkdir(parents=True)
        filename.touch()
        return filename

    def save_data(self, data, filename):
        """Saves data to `filename` in the log directory.

        This is particularly useful when saving configuration options or other
        pieces of data that are dict's or lists.

        Supported file types are:

        - JSON (`*.json`)
        - YAML (`*.yml`, `*.yaml`)
        - TOML (`*.toml`)
        - Pickle (`*.pkl`, `*.pickle`)

        Args:
            data (dict or list): Dictionary to save.
            filename (str or pathlib.Path): The name of the file; we will create
                it under the logdir using [pfile][logdir.LogDir.pfile]. If the
                filetype is unsupported, we will default to pickle and raise a
                warning.
        Returns:
            pathlib.path: Full path to the config file.
        """
        filepath = self.pfile(filename)

        ext = filepath.suffix[1:]
        if ext == "json":
            with filepath.open("w") as file:
                json.dump(data, file)
        elif ext in ("yml", "yaml"):
            with filepath.open("w") as file:
                yaml.dump(data, file)
        elif ext == "toml":
            with filepath.open("w") as file:
                toml.dump(data, file)
        else:
            # Pickle is default if file extension cannot be identified.
            with filepath.open("wb") as file:
                pickle.dump(data, file)
            if ext not in ("pkl", "pickle"):
                warnings.warn(f"Filetype {ext} not found. Used pickle instead.")

        return filepath

    def readme(self, date=True, git_commit=False, git_path=".", info=()):
        """Adds a README.md with useful info.

        The README consists of the name of the directory (passed in at init
        time), followed by a bulleted list with various pieces of info.

        Args:
            date (bool): Add the date and time in the bulleted list of info.
            git_commit (bool): Add the current git commit hash in the bulleted
                list of info.
            git_path (str or pathlib.Path): The path to the git repo (i.e. a
                directory that contains `.git`). Only applicable if `git_commit`
                is True. If the path given is not to a Git repo, a warning is
                issued, and the Git Commit is replaced with `"(no repo found)"`
            info (list of str): A list of additional bullets to add in the
                README.
        Returns:
            pathlib.path: Full path to the README.
        """
        readme_path = self.pfile("README.md")
        with readme_path.open("w") as file:
            lines = [f"# {self._name}", ""]

            if date:
                date_str = self._datetime.strftime("%Y-%m-%d %H:%M:%S")
                lines.append(f"- Date: {date_str}")
            if git_commit:
                git_path = Path(git_path)
                if (git_path / ".git").exists():
                    repo = Repo(str(git_path))
                    commit_hash = repo.head()
                else:
                    warnings.warn("No Git repo found")
                    commit_hash = "(no repo found)"
                lines.append(f"- Git Commit: {commit_hash}")

            lines.extend(map(lambda s: f"- {s}", info))
            file.write("\n".join(lines) + "\n")

            return readme_path
