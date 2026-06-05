from autoparameterized.customizers import NonEmptyCustomizer


def test_non_empty_customizer_replaces_empty_string():
    customizer = NonEmptyCustomizer(default_string="x")

    assert customizer.customize("") == "x"
    assert customizer.customize("abc") == "abc"


def test_non_empty_customizer_replaces_empty_list():
    customizer = NonEmptyCustomizer(default_item=0)

    assert customizer.customize([]) == [0]
    assert customizer.customize([1, 2]) == [1, 2]
