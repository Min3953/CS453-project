from autoparameterized.customizers import TransformCustomizer


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
