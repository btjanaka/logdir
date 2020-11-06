# LogDir

A utility for managing logging directories.

|                    Source                    |                                          PyPI                                           |                                                                                             CI/CD                                                                                             |                        Docs                        |                                                                         Docs Status                                                                         |
| :------------------------------------------: | :-------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------: |
| [GitHub](https://github.com/btjanaka/logdir) | [![PyPI version](https://badge.fury.io/py/logdir.svg)](https://badge.fury.io/py/logdir) | [![Test and Deploy](https://github.com/btjanaka/logdir/workflows/Test%20and%20Deploy/badge.svg?branch=master)](https://github.com/btjanaka/logdir/actions?query=workflow%3A"Test+and+Deploy") | [logdir.btjanaka.net](https://logdir.btjanaka.net) | [![Netlify Status](https://api.netlify.com/api/v1/badges/b3cdff86-dfcf-4b62-9a64-ab431bc5040f/deploy-status)](https://app.netlify.com/sites/logdir/deploys) |

## Installation

To install from PyPI, run:

```bash
pip install logdir
```

To install from source, clone this repo, cd into it, and run:

```bash
pip install -e .
```

## Usage

If your experiment is called `My Experiment`, you can create a logging directory
for it with:

```python
from logdir import LogDir

logdir = LogDir("My Experiment")
```

This will create a logging directory of the form
`./logs/YYYY-MM-DD_HH-MM-SS_my-experiment-dir`; you can change `./logs` by
passing in a second argument for the root directory when initializing `LogDir`,
i.e. `LogDir("My Experiment", "./different-log-dir")`.

You now have access to useful methods for creating files and saving data in the
directory. For example, start writing to a file `new.txt` in the directory with:

```python
with logdir.pfile("new.txt").open() as file:
    file.write("Hello World!")
```

This takes advantage of the [pfile()](/api/#logdir.LogDir.pfile) method, which
creates a `pathlib.Path` to the new file. It also uses `pathlib.Path.open()`.

`pfile()` will also create intermediate directories, so this will work even if
`foo/bar/` does not exist in the logging directory already:

```python
with logdir.pfile("foo/bar/new.txt").open() as file:
    file.write("Hello World!")
```

Finally, there is also [save_data()](/api/#logdir.LogDir.pickle), which saves
data to your desired filetype. JSON, YAML, TOML, and pickle are currently
supported.

```python
logdir.save_data({"a": 1, "b": 2, "c": 3}, "file.json")
```
