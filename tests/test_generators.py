from autoparameterized import FloatGenerator


def test_float_generator_respects_range():
    generator = FloatGenerator(
        constraints={'min_value': 1.5, 'max_value': 2.5},
        seed=42,
    )

    value = generator.generate()

    assert isinstance(value, float)
    assert 1.5 <= value <= 2.5


def test_float_generator_is_reproducible_with_seed():
    first = FloatGenerator(seed=123).generate()
    second = FloatGenerator(seed=123).generate()

    assert first == second
