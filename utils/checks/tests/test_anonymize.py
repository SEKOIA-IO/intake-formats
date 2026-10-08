from anonymize import parse_path


def test_parse_path_supports_array_indexes():
    assert parse_path("a.b[0].c") == ["a", "b", "0", "c"]