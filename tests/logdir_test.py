"""Tests for logdir."""
import json
import pickle
from pathlib import Path

import pytest
import toml
from ruamel import yaml

from freezegun import freeze_time
from logdir import LogDir  # isort: skip

# pylint: disable = missing-function-docstring, redefined-outer-name

TIME = "2020-10-31 06:20:45"
TIME_STR = "2020-10-31_06-20-45"
NICE_TIME_STR = "2020-10-31 06:20:45"


@pytest.fixture
def data():
    return {
        "a": 1,
        "b": 2,
        "c": 3,
    }


@freeze_time(TIME)
def test_creates_dir_on_init(tmp_path):
    LogDir("My Experiment", tmp_path)
    expected_path = tmp_path / f"{TIME_STR}_my-experiment"
    assert expected_path.exists()


@freeze_time(TIME)
def test_creates_nested_dir_on_init(tmp_path):
    LogDir("My Experiment", tmp_path / "logs")
    expected_path = tmp_path / "logs" / f"{TIME_STR}_my-experiment"
    assert expected_path.exists()


@freeze_time(TIME)
def test_creates_file(tmp_path):
    logdir = LogDir("My Experiment", tmp_path)
    file = logdir.file("file.txt")
    assert Path(file) == (tmp_path / f"{TIME_STR}_my-experiment" / "file.txt")
    assert Path(file).exists()


@freeze_time(TIME)
def test_creates_nested_file(tmp_path):
    logdir = LogDir("My Experiment", tmp_path)
    file = logdir.file("newdir/file.txt")
    assert Path(file) == (tmp_path / f"{TIME_STR}_my-experiment" / "newdir" /
                          "file.txt")
    assert Path(file).exists()


@freeze_time(TIME)
def test_creates_dir(tmp_path):
    logdir = LogDir("My Experiment", tmp_path)
    dirname = logdir.dir("mydir")
    assert Path(dirname) == (tmp_path / f"{TIME_STR}_my-experiment" / "mydir")
    assert Path(dirname).exists()


@freeze_time(TIME)
def test_creates_nested_dir(tmp_path):
    logdir = LogDir("My Experiment", tmp_path)
    dirname = logdir.dir("newdir/mydir")
    assert Path(dirname) == (tmp_path / f"{TIME_STR}_my-experiment" / "newdir" /
                             "mydir")
    assert Path(dirname).exists()


@pytest.mark.parametrize("ext,load,mode", [
    ("json", json.load, "r"),
    ("yml", yaml.safe_load, "r"),
    ("yaml", yaml.safe_load, "r"),
    ("toml", toml.load, "r"),
    ("pkl", pickle.load, "rb"),
    ("pickle", pickle.load, "rb"),
])
def test_save_data(ext, load, mode, data, tmp_path):
    logdir = LogDir("My Experiment", tmp_path)
    filepath = logdir.save_data(data, f"data.{ext}")

    with filepath.open(mode) as file:
        assert load(file) == data


def test_save_data_goes_to_pkl_with_unknown_ext(data, tmp_path):
    logdir = LogDir("My Experiment", tmp_path)
    with pytest.warns(UserWarning):
        filepath = logdir.save_data(data, "data.foo")
        with filepath.open("rb") as file:
            assert pickle.load(file) == data


# TODO: How to test readme() _with_ a git directory?


@freeze_time(TIME)
def test_readme_writes_correct_info_with_no_git_dir(tmp_path):
    logdir = LogDir("My Experiment", tmp_path)
    with pytest.warns(UserWarning):
        filepath = logdir.readme(date=True,
                                 git_commit=True,
                                 git_path=tmp_path,
                                 info=["random info"])
        with filepath.open() as file:
            assert file.read() == f"""\
# My Experiment

- Date: {NICE_TIME_STR}
- Git Commit: (no repo found)
- random info
"""
