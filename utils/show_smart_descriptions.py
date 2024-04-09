import argparse
import json
import os
import re
import subprocess
import urllib.parse

from conftest import IntakeTestManager

INTAKES_PATH = os.path.dirname(os.path.dirname(__file__))


class SmartDescriptionManager(IntakeTestManager):
    def flatten_dict(self, input_dict: dict, prefix: str = ""):
        result = {}
        for key, value in input_dict.items():
            new_key = f"{prefix}.{key}" if prefix else key

            if isinstance(value, dict):
                flattened_subdict = self.flatten_dict(value, new_key)
                result.update(flattened_subdict)

            else:
                result[new_key] = value

        return result

    def generate_smart_desc(self, smart_desc: dict, parsed_message: dict) -> str:
        parsed = self.flatten_dict(parsed_message)
        candidates = []

        for possible_smart_desc in smart_desc:
            conditions = possible_smart_desc["conditions"]

            all_conditions_are_met = True
            for condition in conditions:
                condition_field = condition["field"]
                condition_value = condition.get("value")

                if condition_field not in parsed:
                    all_conditions_are_met = False
                    break

                if condition_value is not None:
                    if isinstance(parsed[condition_field], list):
                        condition_value_set = set(
                            item.strip() for item in condition_value.split(",")
                        )

                        if (
                            len(parsed[condition_field]) == 0
                            or set(parsed[condition_field]) != condition_value_set
                        ):
                            all_conditions_are_met = False
                            break

                    else:
                        if parsed[condition_field] != condition_value:
                            all_conditions_are_met = False
                            break

            if all_conditions_are_met:
                candidates.append(possible_smart_desc)

        candidates = sorted(
            candidates, key=lambda x: len(x["conditions"]), reverse=True
        )
        if len(candidates) == 0:
            return parsed_message.get("message", "")

        longest_candidate = candidates[0]
        message = longest_candidate["value"]

        def sub_fields(g: re.Match) -> str:
            field_name = g.group(0).strip("{").strip("}")
            field_parsed_value = parsed.get(field_name, "NULL")
            if type(field_parsed_value) == list:
                field_parsed_value = ", ".join(field_parsed_value)

            return "`%s`" % str(field_parsed_value)

        message = re.sub(r"(\{[a-zA-Z0-9\.\_]+\})", sub_fields, message)
        return message

    def run(self, prsha: str | None = None):
        table = []
        for module_name, intakes in self._intakes.items():
            for intake_name, intake_tests in intakes.items():
                smart_desc_path = os.path.join(
                    INTAKES_PATH,
                    module_name,
                    intake_name,
                    "_meta",
                    "smart-descriptions.json",
                )
                if not os.path.exists(smart_desc_path):
                    continue

                with open(smart_desc_path, "rt") as f:
                    smart_descriptions = json.load(f)

                for test in intake_tests:
                    test_path = os.path.join(INTAKES_PATH, test)
                    with open(test_path, "rt") as file:
                        raw = json.load(file)

                    test_result = raw["expected"]
                    test_smart_desc = self.generate_smart_desc(
                        smart_descriptions, test_result
                    )

                    test_label = test
                    if prsha:
                        test_url = (
                            "https://github.com/SEKOIA-IO/intake-formats/blob/%s/%s"
                            % (prsha, urllib.parse.quote(test))
                        )
                        test_label = f"[{test}]({test_url})"

                    table.append((test_label, test_smart_desc))

        # sort the first column (with test paths)
        table = sorted(table, key=lambda x: x[0])

        # generate markdown table
        markdown = "| Test File | Smart Description |\n|---|---|\n"
        for row in table:
            markdown += "|" + "|".join(row) + "|" + "\n"

        print(markdown)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check smart descriptions")
    parser.add_argument(
        "--module", action="append", default=[], help="name of the module to test"
    )
    parser.add_argument(
        "--format", action="append", default=[], help="name of the format to test"
    )
    parser.add_argument("--prsha", default=None, help="SHA-1 of PR")
    parser.add_argument(
        "--changes", action="store_true", help="only check formats that were modified"
    )

    args = parser.parse_args()

    modules = args.module
    intake_formats = args.format

    if args.changes:
        check_all = False
        changed_modules = set()
        changed_formats = set()

        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main"], capture_output=True
        )
        for changed_file in result.stdout.splitlines():
            changed_file = changed_file.decode()
            parts = changed_file.split("/")

            if parts[-1] in ["conftest.py", "test_formats.py"]:
                check_all = True
                break

            if len(parts) > 2:
                changed_modules.add(parts[0])
                changed_formats.add(parts[1])

        if check_all:
            modules = []
            intake_formats = []
        else:
            modules = list(changed_modules)
            intake_formats = list(changed_formats)

    manager = SmartDescriptionManager()
    manager.load(modules=modules, intake_formats=intake_formats)
    manager.run(prsha=args.prsha)
