import sys

# from alto2txt
import extract_publications_text as ept
import pytest
from icecream import ic


def test_cli_no_args(capsys):

    # Test that not supplying any args should give a usage message
    with pytest.raises(SystemExit):
        sys.argv[1:] = ""
        ept.main()

    captured = capsys.readouterr()
    assert captured.err.startswith("usage")


def test_input_dir_args():
    # Test that an error is raised `xml_in_dir` and `txt_out_dir` are the same.
    with pytest.raises(AssertionError) as ae:
        sys.argv[1:] = ["demo-files", "demo-files"]
        ept.main()

    assert ic(ae.match("should be different"))

    # Test that a non-existant `xml_in_dir` if caught
    with pytest.raises(AssertionError) as ae:
        sys.argv[1:] = ["non-existant-input-dir", "demo-output"]
        ept.main()

    assert ic(ae.match("non-existant-input-dir"))
    assert ic(ae.match("xml_in_dir.+not found"))


def test_output_dir_args(tmp_path):
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
        sys.argv[1:] = ["demo-files", str(output_dir)]
        ept.main()
        assert output_dir.exists()

    # Check that passing a existing file (rather than a dir) is caught
    file_not_dir = tmp_path / "output-file.txt"
    file_not_dir.touch()

    with pytest.raises(AssertionError) as ae:
        sys.argv[1:] = ["demo-files", str(file_not_dir)]
        ept.main()

    assert ae.match("output-file.txt")
    assert ae.match("txt_out_dir.+not a directory")

    # Test that `txt_out_dir` is empty. What should the correct behaviour be here?
    # See https://github.com/Living-with-machines/alto2txt/issues/27

    run_twice_dir = str(tmp_path / "run-twice")

    # Run first time to ensure that there is already content
    sys.argv[1:] = ["demo-files", run_twice_dir]
    ept.main()

    with pytest.raises(ValueError) as ve:
        sys.argv[1:] = ["demo-files", run_twice_dir]
        ept.main()

    # TODO: confirm the expected behaviour here. These assert statements are
    # illustrative. (See link to GitHub issue above)
    assert ic(ve.match("run-twice"))
    assert ic(ve.match("txt_out_dir.+not empty"))

    # Leave this test failing until the GH issue above is complete
    assert False


def test_log_file_args(tmp_path):
    # Test path to `-l log_file`. Does it exist?
    # If so is it overwritten, or clobbered

    log_file = tmp_path / "logfile.log"
    # It doesn't exist before we run it
    assert not log_file.exists()

    # Test that a non-existant `txt_out_dir` if caught
    output_dir = tmp_path / "output-dir"
    output_dir.mkdir()
    output_dir = str(output_dir)

    sys.argv[1:] = ["--l", str(log_file), "demo-files", output_dir]
    ept.main()

    # It does exist after we run it
    assert log_file.exists()
    first_run_size = log_file.stat().st_size

    # Run a second time and check that the logfile is roughly twice the original size
    # This asserts that the correct behaviour is that alto2txt always appends to an existing
    # logfile and does not overwrite it.
    sys.argv[1:] = ["--l", str(log_file), "demo-files", output_dir]
    ept.main()
    second_run_size = log_file.stat().st_size

    assert (1.9 * first_run_size) < second_run_size
    assert (2.1 * first_run_size) > second_run_size


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
    # What does this does/mean?

    assert False
