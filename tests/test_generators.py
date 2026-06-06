from autoparameterized import BoolGenerator, FloatGenerator


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


def test_bool_generator_returns_boolean():
    value = BoolGenerator(seed=42).generate()

    assert isinstance(value, bool)


def test_bool_generator_probability_constraint():
    assert BoolGenerator(constraints={'probability': 1.0}, seed=42).generate() is True
    assert BoolGenerator(constraints={'probability': 0.0}, seed=42).generate() is False


def test_bool_generator_is_reproducible_with_seed():
    first = BoolGenerator(seed=123).generate()
    second = BoolGenerator(seed=123).generate()

    assert first == second
