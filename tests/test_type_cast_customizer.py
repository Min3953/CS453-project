from autoparameterized.customizers import TypeCastCustomizer


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
