from autoparameterized.customizers import RegexStringCustomizer


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
