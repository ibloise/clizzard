import pytest

from clizzard.option import Option


def test_flag_true_emits_flag_only():
    opt = Option("verbose", True)
    assert opt.to_argv() == ["--verbose"]


def test_flag_false_emits_nothing():
    opt = Option("verbose", False)
    assert opt.to_argv() == []


def test_none_emits_nothing():
    opt = Option("threads", None)
    assert opt.to_argv() == []


def test_key_value_emits_flag_and_value():
    opt = Option("threads", 4)
    assert opt.to_argv() == ["--threads", "4"]


def test_short_prefix_is_supported():
    opt = Option("t", 8, prefix="-")
    assert opt.to_argv() == ["-t", "8"]


def test_repeatable_list_emits_multiple_pairs():
    opt = Option("include", ["a", "b"], repeatable=True)
    assert opt.to_argv() == ["--include", "a", "--include", "b"]


def test_repeatable_false_list_raises():
    opt = Option("include", ["a", "b"], repeatable=False)
    with pytest.raises(TypeError):
        opt.to_argv()


def test_empty_name_raises():
    with pytest.raises(ValueError):
        Option("", True)


def test_invalid_prefix_raises():
    with pytest.raises(ValueError):
        Option("threads", 4, prefix="---")


def test_underscores_are_normalized_by_default():
    opt = Option("log_level", "INFO")
    assert opt.to_argv() == ["--log-level", "INFO"]


def test_can_disable_name_normalization():
    opt = Option("log_level", "INFO", normalize_name=False)
    assert opt.to_argv() == ["--log_level", "INFO"]
