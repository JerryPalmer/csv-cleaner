import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT = Path(__file__).resolve().parents[1]
# Prefer project virtualenv python if available, otherwise fall back to current interpreter
_candidate_py = PROJECT / ".venv" / "Scripts" / "python.exe"
PY = str(_candidate_py) if _candidate_py.exists() else sys.executable
SCRIPT = PROJECT / "clean_csv.py"


def run_cmd(args, cwd=None):
    cmd = [str(PY), str(SCRIPT)] + args
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd)
    return proc


def test_removes_empty_rows(tmp_path):
    inp = tmp_path / "in.csv"
    out = tmp_path / "out.csv"
    inp.write_text("a,b\n1,2\n , \n3,4\n")

    proc = run_cmd([str(inp), str(out)])
    assert proc.returncode == 0
    assert out.exists()
    text = out.read_text()
    assert "1,2" in text
    assert "3,4" in text
    # the whitespace-only row should be gone
    assert text.count('\n') == 3  # header + 2 rows + trailing newline


def test_missing_input(tmp_path):
    inp = tmp_path / "nope.csv"
    out = tmp_path / "out.csv"
    proc = run_cmd([str(inp), str(out)])
    assert proc.returncode == 2
    assert "Input file not found" in proc.stderr


def test_input_is_directory(tmp_path):
    inp = tmp_path / "dir"
    inp.mkdir()
    out = tmp_path / "out.csv"
    proc = run_cmd([str(inp), str(out)])
    assert proc.returncode == 3
    assert "Input path is not a file" in proc.stderr


def test_unwritable_output(tmp_path):
    """
    Create an output file and make the file read-only. On Windows, making the directory read-only does not
    prevent file creation, so make the target file read-only to trigger a write permission error.
    """
    inp = tmp_path / "in.csv"
    outdir = tmp_path / "no_write_dir"
    outdir.mkdir()
    out = outdir / "out.csv"

    # create the output file and make it read-only
    out.write_text("existing")
    os.chmod(out, stat.S_IREAD)

    inp.write_text("a,b\n1,2\n")

    proc = run_cmd([str(inp), str(out)])

    # cleanup: make file writable again for pytest to remove it
    os.chmod(out, stat.S_IWRITE | stat.S_IREAD)

    # Depending on OS and ordering, script may report "output exists" (9) or a permission error (4)
    assert proc.returncode in (4, 9)
    assert ("Cannot write to output file" in proc.stderr) or ("output file already exists" in (proc.stderr + proc.stdout).lower())


def test_empty_input_file(tmp_path):
    inp = tmp_path / "empty.csv"
    inp.write_text("")
    out = tmp_path / "out.csv"
    proc = run_cmd([str(inp), str(out)])
    assert proc.returncode == 6
    assert "Input CSV is empty" in proc.stderr
