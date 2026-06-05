from autoparameterized.customizers import (
    ChainCustomizer,
    LengthCustomizer,
    TransformCustomizer,
)


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
