"""A utility for managing logging directories."""
__version__ = "0.1.0"

__all__ = [
    "LogDir",
]

import time
from pathlib import Path


class LogDir:
    """A utility for managing logging directories.

    Creates a logging directory on startup; comes with a handful of other handy
    methods.
    """

    def __init__(self, name, rootdir="logs"):
        """Initializes by creating the logging directory.

        The directory is created under rootdir (which is created if it does not
        exist). Logging directory is named with the date, followed by the time,
        followed by the given name with spaces and underscores replaced with
        dashes, for instance ``2020-02-14_18:01:45_my-logging-dir``.
        """
        # Create the rootdir.
        self.rootdir = Path(rootdir)
        if not self.rootdir.exists():
            self.rootdir.mkdir(parents=True)

        # Create the logdir.
        dirname = (time.strftime("%Y-%m-%d_%H-%M-%S") + "_" +
                   name.replace("_", "-").replace(" ", "-"))
        self.logdir = self.rootdir / Path(dirname)
        self.logdir.mkdir()
