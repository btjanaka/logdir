"""Tests for logdir."""
import json
import pickle
from pathlib import Path

import pytest
import toml
from freezegun import freeze_time
from ruamel import yaml

from logdir import LogDir  # isort: skip

# pylint: disable = missing-function-docstring, redefined-outer-name

TIME = "2020-10-31 06:20:45"
TIME_STR = "2020-10-31_06-20-45"


@pytest.fixture
def data():
    return {
        "a": 1,
        "b": 2,
        "c": 3,
    }


@freeze_time(TIME)
def test_creates_dir_on_init(tmp_path):
    LogDir("My Logging Dir", tmp_path)
    expected_path = tmp_path / f"{TIME_STR}_my-logging-dir"
    assert expected_path.exists()


@freeze_time(TIME)
def test_creates_nested_dir_on_init(tmp_path):
    LogDir("My Logging Dir", tmp_path / "logs")
    expected_path = tmp_path / "logs" / f"{TIME_STR}_my-logging-dir"
    assert expected_path.exists()


@freeze_time(TIME)
def test_creates_file(tmp_path):
    logdir = LogDir("My Logging Dir", tmp_path)
    file = logdir.file("file.txt")
    assert Path(file) == (tmp_path / f"{TIME_STR}_my-logging-dir" / "file.txt")
    assert Path(file).exists()


@freeze_time(TIME)
def test_creates_nested_file(tmp_path):
    logdir = LogDir("My Logging Dir", tmp_path)
    file = logdir.file("newdir/file.txt")
    assert Path(file) == (tmp_path / f"{TIME_STR}_my-logging-dir" / "newdir" /
                          "file.txt")
    assert Path(file).exists()


@pytest.mark.parametrize("ext,loader,mode", [
    ("json", json.load, "r"),
    ("yml", yaml.safe_load, "r"),
    ("yaml", yaml.safe_load, "r"),
    ("toml", toml.load, "r"),
    ("pkl", pickle.load, "rb"),
    ("pickle", pickle.load, "rb"),
])
def test_save_data(ext, loader, mode, data, tmp_path):
    logdir = LogDir("My Logging Dir", tmp_path)
    filepath = logdir.save_data(data, f"data.{ext}")

    with filepath.open(mode) as file:
        assert loader(file) == data


def test_save_data_fails_with_unknown_ext(data, tmp_path):
    logdir = LogDir("My Logging Dir", tmp_path)
    with pytest.raises(RuntimeError):
        logdir.save_data(data, "data.foo")
