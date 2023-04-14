import sys
from os import PathLike, getcwd
from pathlib import Path
from shutil import rmtree
from subprocess import CompletedProcess
from typing import Final

import pytest
from icecream import ic

from alto2txt import extract_publications_text as ept

DEMO_FILES_PATH: Final[str] = "demo-files"
DEMO_OUTPUT_PATH: Final[str] = "demo-files"


@pytest.fixture
def demo_files_path(path: str = DEMO_FILES_PATH) -> str:
    return path


@pytest.fixture
def demo_output_path(path: str = DEMO_OUTPUT_PATH) -> str:
    return path


@pytest.fixture
def demo_output_dir(tmp_path: Path, demo_output_path: PathLike) -> Path:
    output_dir = tmp_path / demo_output_path
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def set_test_dir(request, monkeypatch):
    monkeypatch.chdir(request.fspath.dirname)


def test_cli_no_args(capsys):
    # Test that not supplying any args should give a usage message
    with pytest.raises(SystemExit):
        sys.argv[1:] = ""
        ept.main()

    captured = capsys.readouterr()
    assert captured.err.startswith("usage")


def test_input_dir_args(demo_files_path, demo_output_path):
    # Test that an error is raised `xml_in_dir` and `txt_out_dir` are the same.
    with pytest.raises(AssertionError) as ae:
        sys.argv[1:] = [demo_files_path, demo_files_path]
        ept.main()

    assert ic(ae.match("should be different"))

    # Test that a non-existant `xml_in_dir` if caught
    with pytest.raises(AssertionError) as ae:
        sys.argv[1:] = ["non-existant-input-dir", demo_output_path]
        ept.main()

    assert ic(ae.match("non-existant-input-dir"))
    assert ic(ae.match("xml_in_dir.+not found"))


def test_output_dir_args(tmp_path, demo_files_path):
    # Use the `tmp_path` fixture to ensure that the so-called "non-existant" dirs aren't
    # later inadvertently created within the repo.

    # Test that a non-existant `txt_out_dir` is created, including if it is a very deeply nested dir.
    # output_dir = tmp_path / "non-existant-output-dir"
    output_dirs_list = [
        tmp_path / "non-existant-output-dir",
        tmp_path
        / "a"
        / "b"
        / "c"
        / "d"
        / "very"
        / "deeply"
        / "nested"
        / "nonexistent"
        / "dir",
    ]

    for output_dir in output_dirs_list:
        assert not output_dir.exists()
        sys.argv[1:] = [demo_files_path, str(output_dir)]
        ept.main()
        assert output_dir.exists()

    # Check that passing a existing file (rather than a dir) is caught
    file_not_dir = tmp_path / "output-file.txt"
    file_not_dir.touch()

    with pytest.raises(AssertionError) as ae:
        sys.argv[1:] = [demo_files_path, str(file_not_dir)]
        ept.main()

    assert ae.match("output-file.txt")
    assert ae.match("txt_out_dir.+not a directory")


@pytest.mark.skip("Correct behaviour not confirmed. See GH Issue #27")
def test_non_empty_output_dir(demo_files_path, tmp_path):
    # Run twice to ensure that on the second run `txt_out_dir` is not empty.
    # What should the correct behaviour be here?
    # See https://github.com/Living-with-machines/alto2txt/issues/27

    run_twice_dir = str(tmp_path / "run-twice")

    # Run first time to ensure that there is already content
    sys.argv[1:] = [demo_files_path, run_twice_dir]
    ept.main()

    with pytest.raises(ValueError) as ve:
        sys.argv[1:] = [demo_files_path, run_twice_dir]
        ept.main()

    # TODO: confirm the expected behaviour here. These assert statements are
    # illustrative. (See link to GitHub issue above)
    assert ic(ve.match("run-twice"))
    assert ic(ve.match("txt_out_dir.+not empty"))

    # Leave this test failing until the GH issue above is complete
    assert False


def test_log_file_args(demo_files_path, demo_output_dir, tmp_path):
    # Test path to `-l log_file`. Does it exist?
    # If so is it overwritten, or clobbered

    log_file = tmp_path / "logfile.log"
    # It doesn't exist before we run it
    assert not log_file.exists()

    # Test that a non-existant `txt_out_dir` if caught
    # output_dir = tmp_path / demo_output_path
    # output_dir.mkdir()
    # output_dir = str(output_dir)

    sys.argv[1:] = ["-l", str(log_file), demo_files_path, str(demo_output_dir)]
    ept.main()

    # It does exist after we run it
    assert log_file.exists()
    first_run_size = log_file.stat().st_size

    # Run a second time and check that the logfile is roughly twice the original size
    # This asserts that the correct behaviour is that alto2txt always appends to an existing
    # logfile and does not overwrite it.
    sys.argv[1:] = ["-l", str(log_file), demo_files_path, str(demo_output_dir)]
    ept.main()
    second_run_size = log_file.stat().st_size

    assert (1.9 * first_run_size) < second_run_size
    assert (3.0 * first_run_size) > second_run_size


@pytest.mark.skip("Not yet implemented")
def test_processor_args():
    # Test `-p`, with (a) valid, (b) invalid and (c) null values.

    # Test `-n`
    # - Error/warning if specified without `-p` option
    # - Error/warning if specified with a `-p` option other than `-p spark`
    # - Error/warning if specified with a value < 1.
    # - Warning on an upper sane limit? What is the correct behaviour?
    assert False


@pytest.mark.skip("Not yet implemented")
def test_downsample_arg():
    # Test `-d`
    # What does this do/mean?

    assert False


class TestVerifyOutput:

    """Test running verify_output wrapper of alto2txt-verify.sh"""

    def rm_temp_files(self) -> None:
        """Ensure temp files generated from verify_output are removed."""
        if ept.VERIFY_SCRIPT_TEMP_PATH.exists():
            rmtree(ept.VERIFY_SCRIPT_TEMP_PATH)

    @property
    def abosulte_default_temp_path(self) -> Path:
        return getcwd() / ept.VERIFY_SCRIPT_TEMP_PATH

    def get_input_path(self, path: PathLike) -> Path:
        return Path(ept.VERIFY_TEMP_INPUT_PATH) / path

    def get_output_path(self, path: PathLike) -> Path:
        return Path(ept.VERIFY_TEMP_OUTPUT_PATH) / path

    def setup_method(self) -> None:
        self.rm_temp_files()

    def teardown_method(self) -> None:
        self.rm_temp_files()

    def test_verify_path_error(
        self, demo_files_path, demo_output_dir, set_test_dir
    ) -> None:
        """Test ScriptPathError raised due to script not in default relative path."""
        with pytest.raises(ept.ScriptPathError) as excinfo:
            ept.verify_output(demo_files_path, demo_output_dir)
        assert str(ept.VERIFY_SCRIPT_PATH) in str(excinfo)

    def test_verify_output(self, demo_files_path, demo_output_dir, capsys) -> None:
        """Test paths are correctly generated to verify output."""
        test_file_name = Path("0002647-1824.txt")
        correct_input_file_path: Path = self.get_input_path(test_file_name)
        correct_output_file_path: Path = self.get_output_path(test_file_name)
        assert not correct_input_file_path.exists()
        assert not correct_output_file_path.exists()
        completed_process: CompletedProcess = ept.verify_output(
            demo_files_path, demo_output_dir
        )
        assert completed_process.returncode == 0  # Default success code
        script_temp_path: Path = self.abosulte_default_temp_path
        assert script_temp_path.is_dir()
        assert correct_input_file_path.exists()
        assert correct_output_file_path.exists()
