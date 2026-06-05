from autoparameterized.customizers import LengthCustomizer


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
