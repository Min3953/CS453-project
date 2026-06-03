from autoparameterized.customizers import (
    ChainCustomizer,
    LengthCustomizer,
    NonEmptyCustomizer,
    RegexStringCustomizer,
    TransformCustomizer,
    TypeCastCustomizer,
)


def test_length_customizer_truncates_string_to_exact_length():
    customizer = LengthCustomizer(length=4)

    assert customizer.customize("abcdef") == "abcd"


def test_length_customizer_pads_string_to_exact_length():
    customizer = LengthCustomizer(length=5, fill_value="x")

    assert customizer.customize("ab") == "abxxx"


def test_length_customizer_truncates_list_to_max_length():
    customizer = LengthCustomizer(max_length=2)

    assert customizer.customize([1, 2, 3]) == [1, 2]


def test_length_customizer_pads_list_to_min_length():
    customizer = LengthCustomizer(min_length=4, fill_value=0)

    assert customizer.customize([1, 2]) == [1, 2, 0, 0]


def test_length_customizer_keeps_value_inside_range():
    customizer = LengthCustomizer(min_length=2, max_length=4)

    assert customizer.customize("abc") == "abc"


def test_length_customizer_keeps_unsupported_value():
    customizer = LengthCustomizer(length=3)

    assert customizer.customize(123) == 123


def test_length_customizer_rejects_invalid_lengths():
    for kwargs in (
        {"length": -1},
        {"min_length": -1},
        {"max_length": -1},
        {"min_length": 4, "max_length": 2},
    ):
        try:
            LengthCustomizer(**kwargs)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Expected ValueError for {kwargs}")


def test_transform_customizer_applies_string_transform():
    assert TransformCustomizer("upper").customize("abc") == "ABC"
    assert TransformCustomizer("lower").customize("ABC") == "abc"
    assert TransformCustomizer("strip").customize(" abc ") == "abc"
    assert TransformCustomizer("title").customize("hello world") == "Hello World"


def test_transform_customizer_applies_callable_transform():
    customizer = TransformCustomizer(lambda value: value + 1)

    assert customizer.customize(2) == 3


def test_transform_customizer_keeps_unsupported_value():
    customizer = TransformCustomizer("upper")

    assert customizer.customize(123) == 123


def test_transform_customizer_rejects_invalid_transform():
    for transform in ("capitalize", 123):
        try:
            TransformCustomizer(transform)
        except (TypeError, ValueError):
            pass
        else:
            raise AssertionError(f"Expected error for {transform}")


def test_chain_customizer_applies_customizers_in_order():
    customizer = ChainCustomizer(
        TransformCustomizer("strip"),
        TransformCustomizer("upper"),
        LengthCustomizer(max_length=3),
    )

    assert customizer.customize(" abcd ") == "ABC"


def test_chain_customizer_keeps_value_with_empty_chain():
    customizer = ChainCustomizer()

    assert customizer.customize("abc") == "abc"


def test_chain_customizer_rejects_invalid_customizer():
    try:
        ChainCustomizer(object())
    except TypeError:
        pass
    else:
        raise AssertionError("Expected TypeError for invalid customizer")


def test_regex_string_customizer_rejects_invalid_config():
    invalid_configs = (
        {"pattern": 123},
        {"pattern": "["},
        {"pattern": "[A-Z]+", "fallback": 123},
        {"pattern": "[A-Z]+", "fallback": "abc"},
    )

    for config in invalid_configs:
        try:
            RegexStringCustomizer(**config)
        except (TypeError, ValueError):
            pass
        else:
            raise AssertionError(f"Expected error for {config}")


def test_regex_string_customizer_matches_or_uses_fallback():
    customizer = RegexStringCustomizer("[A-Z]{3}", fallback="ABC")

    assert customizer.customize("XYZ") == "XYZ"
    assert customizer.customize("bad") == "ABC"


def test_regex_string_customizer_keeps_non_string_value():
    customizer = RegexStringCustomizer("[A-Z]+", fallback="ABC")

    assert customizer.customize(123) == 123


def test_type_cast_customizer_rejects_invalid_target_type():
    for target_type in (bool, list, "int"):
        try:
            TypeCastCustomizer(target_type)
        except TypeError:
            pass
        else:
            raise AssertionError(f"Expected TypeError for {target_type}")


def test_type_cast_customizer_converts_values():
    assert TypeCastCustomizer(int).customize("3") == 3
    assert TypeCastCustomizer(str).customize(3) == "3"
    assert TypeCastCustomizer(float).customize("2.5") == 2.5


def test_type_cast_customizer_handles_failed_conversion():
    assert TypeCastCustomizer(int).customize("bad") == "bad"
    assert TypeCastCustomizer(int, fallback=0).customize("bad") == 0


def test_non_empty_customizer_replaces_empty_string():
    customizer = NonEmptyCustomizer(default_string="x")

    assert customizer.customize("") == "x"
    assert customizer.customize("abc") == "abc"


def test_non_empty_customizer_replaces_empty_list():
    customizer = NonEmptyCustomizer(default_item=0)

    assert customizer.customize([]) == [0]
    assert customizer.customize([1, 2]) == [1, 2]
