"""A utility for managing logging directories."""
__version__ = "0.11.1"

__all__ = [
    "LogDir",
]

import datetime
import json
import pickle
import shutil
import warnings
from collections import namedtuple
from pathlib import Path
from uuid import uuid4

import slugify
import toml
from dulwich.repo import Repo
from ruamel import yaml


class LogDir:
    """A utility for managing logging directories.

    Creates a logging directory on startup; comes with a handful of other handy
    methods.
    """

    def __init__(self,
                 name,
                 rootdir="./logs",
                 custom_dir=None,
                 slugify_kwargs=None,
                 uuid=False):
        """Initializes by creating the logging directory.

        The directory is created under `rootdir` (which is created if it does
        not exist). Logging directory is named with the date, followed by the
        time, followed by the slugified `name`, followed by a UUID (if
        `uuid=True`). For example:

        ```
        2020-02-14_18-01-45_my-logging-dir_16fd2706-8baf-433b-82eb-8c7fada847da
        ```

        A custom directory may also be passed in via `custom_dir`.

        `name` is slugified with
        [python-slugify](https://github.com/un33k/python-slugify). Pass options
        to `slugify` with `slugify_kwargs`.

        Args:
            name (str): Name to associate with this directory. This is used in
                creating the logging directory name. It is also used in places
                like the README.
            rootdir (str or pathlib.Path): Root directory for all logging
                directories, e.g. `./logs/`
            custom_dir (str or pathlib.Path): If passed in, this directory
                will be used instead of automatically generating one in
                `rootdir`. This directory can be one that already exists. If it
                does not exist, it will be created.
            slugify_kwargs: kwargs for
                [slugify](https://github.com/un33k/python-slugify#options).
            uuid (bool): If passed in, generates a
                [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier)
                and appends it to the directory name, i.e. `..._[UUID]`. This
                can be useful if you are generating multiple logging directories
                at the same time -- by default, directories will have name
                conflicts if they are generated during the same second. The
                UUID is generated randomly with
                [uuid4](https://docs.python.org/3/library/uuid.html#uuid.uuid4).
                Ignored when `custom_dir` is passed in.
        """
        self._name = name

        self._datetime = datetime.datetime.now()
        if custom_dir is None:
            # Automatically generate directory in `rootdir`.
            rootdir = Path(rootdir)
            slugify_kwargs = {} if slugify_kwargs is None else slugify_kwargs
            name_slug = slugify.slugify(name, **slugify_kwargs)
            uuid = f"_{uuid4()}" if uuid else ""
            dirname = (self._datetime.strftime("%Y-%m-%d_%H-%M-%S") + "_" +
                       name_slug + uuid)
            self._logdir = rootdir / Path(dirname)
        else:
            # Use custom directory.
            self._logdir = Path(custom_dir)

        if not self._logdir.exists():
            # Creates intermediate directories as well if needed.
            self._logdir.mkdir(parents=True)

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

    def file(self, filename, touch=False, touch_inter=True):
        """Returns a string path to the given file.

        By default, intermediate directories are created if they do not exist.
        However, the file itself it not created (this helps avoid confusing
        situations where one is checking for the existence of a file). This can
        be changed by passing in `touch=True`.

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
            touch (bool): Whether to automatically touch the file so that an
                empty file exists even if it is not opened.
            touch_inter (bool): Whether to automatically create intermediate
                directories. If this option is set to False, `touch` is also set
                to False.
        Returns:
            str: Path to the new file in the logging directory.
        """
        return str(self.pfile(filename, touch, touch_inter))

    def pfile(self, filename, touch=False, touch_inter=True):
        """Same as [file][logdir.LogDir.file], but returns pathlib.Path.

        See [file][logdir.LogDir.file] for args.

        Returns:
            pathlib.Path: Path to the new file in the logging directory.
        """
        touch = False if not touch_inter else touch
        filename = self._logdir / Path(filename)
        if touch_inter and not filename.parent.exists():
            filename.parent.mkdir(parents=True)
        if touch and not filename.exists():
            filename.touch()
        return filename

    def dir(self, dirname, touch=False, touch_inter=True):
        """Returns a string path to the given directory.

        By default, intermediate directories are created if they do not exist.
        However the directory itself is not created. This can be changed by
        passing in `touch=True`.

        Example:
            ```python
            logdir = LogDir("logdir")
            logdir.filepath("mydir") # "..._logdir/mydir/"
            ```

        Args:
            dirname (str or pathlib.Path): The name of the directory.
            touch (bool): Whether to automatically create the directory.
            touch_inter (bool): Whether to automatically create intermediate
                directories. If this option is set to False, `touch` is also set
                to False.
        Returns:
            str: Path to the new directory in the logging directory.
        """
        return str(self.pdir(dirname, touch, touch_inter))

    def pdir(self, dirname, touch=False, touch_inter=True):
        """Same as [dir][logdir.LogDir.dir], but returns pathlib.Path.

        See [dir][logdir.LogDir.dir] for args.

        Returns:
            pathlib.Path: Path to the new directory in the logging directory.
        """
        touch = False if not touch_inter else touch
        dirname = self._logdir / Path(dirname)
        if touch_inter and not dirname.parent.exists():
            dirname.parent.mkdir(parents=True)
        if touch and not dirname.exists():
            dirname.mkdir()
        return dirname

    def copy(self, src, dest):
        """Copies a file into the logging directory.

        Example:
            The following copies `foobar.txt` in the current directory to
            `new/foobar2.txt` _within the logging directory_.
            ```python
            logdir = LogDir("logdir")
            logdir.copy("foobar.txt", "new/foobar2.txt")
            ```

        Args:
            src (str or pathlib.Path): The source file. It is evaluated relative
                to the current working directory of the program (it could also
                be absolute).
            dest (str or pathlib.Path): Destination location _within the
                logging directory_. Intermediate directories are created.
        """
        shutil.copy(str(src), self.file(dest))

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
            data (object): Data to save. Typically a dict or list for JSON,
                YAML, and TOML, and any pickle-able object for pickle.
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
                yaml_worker = yaml.YAML(typ="unsafe")
                yaml_worker.dump(data, file)
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
                    commit_hash = repo.head().decode("utf-8")
                else:
                    warnings.warn("No Git repo found")
                    commit_hash = "(no repo found)"
                lines.append(f"- Git Commit: {commit_hash}")

            lines.extend(map(lambda s: f"- {s}", info))
            file.write("\n".join(lines) + "\n")

            return readme_path
