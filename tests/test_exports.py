import autoparameterized as ap

from autoparameterized.customizers import (
    NonEmptyCustomizer,
    RegexStringCustomizer,
    TypeCastCustomizer,
)


def test_additional_customizers_are_exported():
    assert ap.RegexStringCustomizer is RegexStringCustomizer
    assert ap.TypeCastCustomizer is TypeCastCustomizer
    assert ap.NonEmptyCustomizer is NonEmptyCustomizer


def test_additional_customizers_are_in_all():
    for name in ("RegexStringCustomizer", "TypeCastCustomizer", "NonEmptyCustomizer"):
        assert name in ap.__all__
