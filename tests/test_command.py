# tests/test_command.py
import pytest

from clizzard import Option, Positional
from clizzard.command import Command


def test_command_with_exe_only():
    cmd = Command("ls")
    assert cmd.to_argv() == ["ls"]


def test_command_with_args():
    cmd = Command("echo", args=["hello", "world"])
    assert cmd.to_argv() == ["echo", "hello", "world"]


def test_command_with_single_option():
    cmd = Command("tool", options=[Option("threads", 4)])
    assert cmd.to_argv() == ["tool", "--threads", "4"]


def test_command_with_multiple_options_preserves_order():
    cmd = Command("tool", options=[Option("b", True), Option("a", True)])
    assert cmd.to_argv() == ["tool", "--b", "--a"]


def test_command_with_subcommands():
    cmd = Command(
        "git", subcommands=["commit"], options=[Option("m", "msg", prefix="-")]
    )
    assert cmd.to_argv() == ["git", "commit", "-m", "msg"]


def test_command_combines_all_parts_in_order():
    cmd = Command(
        "spades.py",
        subcommands=[],
        options=[Option("threads", 8), Option("careful", True)],
        args=["-1", "r1.fq.gz", "-2", "r2.fq.gz"],
    )
    assert cmd.to_argv() == [
        "spades.py",
        "--threads",
        "8",
        "--careful",
        "-1",
        "r1.fq.gz",
        "-2",
        "r2.fq.gz",
    ]




def test_command_with_positional_objects():
    cmd = Command(
        "tool",
        options=[Option("threads", 8)],
        args=[Positional("input", "in.txt"), Positional("output", "out.txt")],
    )

    assert cmd.to_argv() == ["tool", "--threads", "8", "in.txt", "out.txt"]


def test_command_with_variadic_positional_object():
    cmd = Command("cat", args=[Positional("files", ["a.txt", "b.txt"], variadic=True)])
    assert cmd.to_argv() == ["cat", "a.txt", "b.txt"]

def test_raises_in_exe_empty_string():
    with pytest.raises(ValueError):
        Command(exe="")


def test_command_to_string():
    cmd = Command(
        "git",
        subcommands=["commit"],
        options=[Option("msg", value="example", prefix="--")],
    )

    assert cmd.to_string() == "git commit --msg example"
