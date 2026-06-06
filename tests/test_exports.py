import autoparameterized as ap

from autoparameterized.generators import (
    DateGenerator,
    EnumGenerator,
    LiteralGenerator,
    TupleGenerator,
)

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


def test_date_generator_is_exported():
    assert ap.DateGenerator is DateGenerator
    assert "DateGenerator" in ap.__all__


def test_tuple_generator_is_exported():
    assert ap.TupleGenerator is TupleGenerator
    assert "TupleGenerator" in ap.__all__


def test_enum_and_literal_generators_are_exported():
    assert ap.EnumGenerator is EnumGenerator
    assert ap.LiteralGenerator is LiteralGenerator
    assert "EnumGenerator" in ap.__all__
    assert "LiteralGenerator" in ap.__all__
