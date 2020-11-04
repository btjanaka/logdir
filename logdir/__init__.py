"""A utility for managing logging directories."""
__version__ = "0.3.0"

__all__ = [
    "LogDir",
]

import datetime
import json
from collections import namedtuple
from pathlib import Path

from ruamel import yaml


class LogDir:
    """A utility for managing logging directories.

    Creates a logging directory on startup; comes with a handful of other handy
    methods.

    [logdir.LogDir.add_readme][]

    Attributes:
        rootdir (pathlib.Path): The root directory for log directories.
        logdir (pathlib.Path): The log directory itself.
    """

    def __init__(self, name, rootdir="logs"):
        """Initializes by creating the logging directory.

        The directory is created under `rootdir` (which is created if it does
        not exist). Logging directory is named with the date, followed by the
        time, followed by the given `name` in lowercase with spaces and
        underscores replaced with dashes, for instance
        `2020-02-14_18:01:45_my-logging-dir`.

        Args:
            name (str or pathlib.Path): Customizable part of the logging
                directory name, e.g. `My cool experiment`
            rootdir (str or pathlib.Path): Root directory for all logging
                directories, e.g. `./logs/`
        """
        # Create the rootdir.
        self.rootdir = Path(rootdir)
        if not self.rootdir.exists():
            self.rootdir.mkdir(parents=True)

        # Create the logdir.
        dirname = (datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_" +
                   name.lower().replace("_", "-").replace(" ", "-"))
        self.logdir = self.rootdir / Path(dirname)
        self.logdir.mkdir()

    def file(self, filename):
        """Returns a string path to the given file.

        Intermediate directories are created if they do not exist.

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
            (str): Path to the new file in the logging directory.
        """
        return str(self.pfile(filename))

    def pfile(self, filename):
        """Same as [file][logdir.LogDir.file], but returns pathlib.Path.

        Args:
            filename (str or pathlib.Path): The name of the file.
        Returns:
            (pathlib.Path): Path to the new file in the logging directory.
        """
        filename = self.logdir / Path(filename)
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

        Args:
            data (dict or list): Dictionary to save.
            filename (str or pathlib.Path): The name of the file; we will create
                it under the logdir using [pfile][logdir.LogDir.pfile].
        Returns:
            (pathlib.path): Full path to the config file.
        Raises:
            RuntimeError: An unsupported filetype was passed into `filename`.
        """
        filepath = self.pfile(filename)

        ext = filepath.suffix[1:]
        if ext == "json":
            with filepath.open("w") as file:
                json.dump(data, file)
        elif ext in ("yml", "yaml"):
            with filepath.open("w") as file:
                yaml.dump(data, file)
        else:
            raise RuntimeError(f"Unsupported filetype '{ext}'")

        return filepath
