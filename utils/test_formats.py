import copy
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


class JsonSorterEncoder(json.JSONEncoder):
    """Custom json encoder to sort lists and dicts recursively."""

    def encode(self, obj: dict) -> str:
        """
        Encode function with additional sorting.

        Arguments:
            obj: dict

        Returns:
            str: sorted json string
        """
        def _sort(item: any) -> any:
            """
            Recursive function to perform sorting.

            Arguments:
                item: any

            Returns:
                any:
            """
            match item:
                case _ if isinstance(item, list):
                    # As we might have a case when list contains dicts, we should sort them as well
                    if len(item) > 0 and isinstance(item[0], dict):
                        return sorted(item, key=lambda i: i.keys())

                    return sorted(_sort(i) for i in item)

                case _ if isinstance(item, dict):
                    return {k: _sort(v) for k, v in item.items()}

                case _:
                    return item

        return super(JsonSorterEncoder, self).encode(_sort(obj))

# Tests inside this file are actually parametrized depending on arguments
# See `pytest_generate_tests` in conftest.py for details


def pop_field(event: dict, dotted_field: str):
    """Remove a field from an event, also removing intermediate objects if needed"""
    parts = dotted_field.split(".")

    if parts[0] in event:
        if len(parts) == 1:
            event.pop(parts[0])
        else:
            pop_field(event[parts[0]], ".".join(parts[1:]))

            if event[parts[0]] == {}:
                event.pop(parts[0])


def build_fixed_expectation(parsed_message):
    """Build a new and improved expectation from the parsed message"""
    new_expectation = copy.deepcopy(parsed_message)

    pop_field(new_expectation, "sekoiaio.intake.coverage")
    pop_field(new_expectation, "sekoiaio.intake.parsing_status")
    pop_field(new_expectation, "sekoiaio.intake.dialect")
    pop_field(new_expectation, "sekoiaio.intake.dialect_uuid")
    pop_field(new_expectation, "event.id")
    pop_field(new_expectation, "event.outcome")
    pop_field(new_expectation, "ecs.version")

    return new_expectation


def test_intakes_produce_expected_messages(request, manager, intakes_root, test_path):
    test_fullpath = os.path.join(intakes_root, test_path)
    with open(test_fullpath) as f:
        testcase = json.load(f)

    parsed = manager.get_parsed_message(test_path)

    # Make tests simpler to write by removing some default values
    merge_dict(testcase["expected"], constant_fields)

    # Ignore the message field
    testcase["expected"]["message"] = parsed["message"]

    # The order inside `related` is not guaranteed, sort it to make it consistent
    if "related" in parsed:
        for related_field in ["hosts", "ip", "user", "hash"]:
            if related_field in parsed["related"]:
                parsed["related"][related_field] = sorted(
                    parsed["related"][related_field]
                )

    pop_field(parsed, "sekoiaio.intake.parsing_duration_ms")

    expected = testcase["expected"]

    if request.config.getoption("fix_expectations") and parsed != expected:
        testcase["expected"] = build_fixed_expectation(parsed)

        with open(test_fullpath, "w") as out:
            json.dump(testcase, out, indent=2)

    # Perform sorting on all fields(including lists) using custom encoder to make sure we have a consistent order
    # The most simple way is to encode to json string and decode it back :)
    expected_sorted = json.loads(json.dumps(expected, sort_keys=True, cls=JsonSorterEncoder))
    parsed_sorted = json.loads(json.dumps(parsed, sort_keys=True, cls=JsonSorterEncoder))

    assert parsed_sorted == expected_sorted


def test_intake_format_coverage(manager, module, intake_format):
    coverage = manager.get_coverage(module, intake_format)

    print(f"Coverage: {coverage['percent']}")
    print("Steps missing coverage:\n")

    for missing in coverage.get("missing", []):
        print(missing)

    assert coverage["percent"] >= 75


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
