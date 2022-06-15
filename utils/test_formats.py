import json
import os

constant_fields = {
    "sekoiaio": {
        "intake": {
            "coverage": None,
            "parsing_status": "success",
            "dialect": "test",
            "dialect_uuid": "00000000-0000-0000-0000-000000000000",
        }
    },
    "event": {"id": "00000000-0000-0000-0000-000000000000", "outcome": "success"},
    "ecs": {"version": "1.10.0"},
}

# Tests inside this file are actually parametrized depending on arguments
# See `pytest_generate_tests` in conftest.py for details


def test_intakes_produce_expected_messages(manager, intakes_root, test_path):
    with open(os.path.join(intakes_root, test_path)) as f:
        testcase = json.load(f)

    parsed = manager.get_parsed_message(test_path)

    # Make tests simpler to write by removing some default values
    merge_dict(testcase["expected"], constant_fields)

    if testcase["expected"].get("event"):
        merge_dict(parsed, {"event": testcase["expected"]["event"]})

    parsed.pop("message")

    # The order inside `related` is not guaranteed, sort it to make it consistent
    if "related" in parsed:
        for related_field in ["hosts", "ip", "user", "hash"]:
            if related_field in parsed["related"]:
                parsed["related"][related_field] = sorted(
                    parsed["related"][related_field]
                )
                print(parsed["related"][related_field])

    assert parsed == testcase["expected"]


def test_intake_format_coverage(manager, module, intake_format):
    coverage = manager.get_coverage(module, intake_format)

    print(f"Coverage: {coverage['percent']}")
    print("Steps missing coverage:\n")

    for missing in coverage.get("missing", []):
        print(missing)

    assert coverage["percent"] > 75


def test_intake_format_unused_fields(manager, module, intake_format):
    taxonomy = manager.get_taxonomy(module, intake_format)

    number_of_unused_fields = len(taxonomy["unused"])

    print(f"Unused fields ({number_of_unused_fields}):\n")

    for unused in taxonomy["unused"]:
        print(unused)

    assert number_of_unused_fields == 0


def test_intake_format_missing_fields(manager, module, intake_format):
    taxonomy = manager.get_taxonomy(module, intake_format)

    number_of_missing_fields = len(taxonomy["missing"])

    print(f"Missing fields ({number_of_missing_fields}):\n")

    for missing in taxonomy["missing"]:
        print(missing)

    assert number_of_missing_fields == 0


def merge_dict(dst, src):
    """
    Merge two dict without erasing intermediate nodes from `dst`
    """
    for key, value in src.items():
        if isinstance(value, dict):
            if key not in dst:
                dst[key] = {}
            merge_dict(dst[key], value)
        else:
            dst[key] = value
