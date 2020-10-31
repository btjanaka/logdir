"""Tests for logdir."""
from pathlib import Path

from freezegun import freeze_time
from logdir import LogDir

# pylint: disable = missing-function-docstring

TIME = "2020-10-31 06:20:45"
TIME_STR = "2020-10-31_06-20-45"


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
