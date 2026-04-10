import pytest

from clizzard.positional import Positional


def test_scalar_positional_emits_single_argument():
    arg = Positional("input", "reads.fq.gz")
    assert arg.to_argv() == ["reads.fq.gz"]


def test_none_positional_emits_nothing():
    arg = Positional("optional_output", None)
    assert arg.to_argv() == []


def test_variadic_positional_emits_multiple_arguments():
    arg = Positional("inputs", ["r1.fq.gz", "r2.fq.gz"], variadic=True)
    assert arg.to_argv() == ["r1.fq.gz", "r2.fq.gz"]


def test_non_variadic_list_raises():
    arg = Positional("inputs", ["r1.fq.gz", "r2.fq.gz"], variadic=False)
    with pytest.raises(TypeError):
        arg.to_argv()


def test_empty_name_raises():
    with pytest.raises(ValueError):
        Positional("", "reads.fq.gz")
