import json
import os

import yaml

from helpers import YamlDumper
from helpers import format_test


def test_linting_taxonomy(format_fields_path, module_fields_path):
    """Ensure that keys are sorted in the taxonomy"""
    for fields_path in [module_fields_path, format_fields_path]:
        # verify that the file exists
        if not os.path.isfile(fields_path):
            continue

        # read file
        with open(file=format_fields_path, mode="r", encoding="utf-8") as f:
            fields: dict = yaml.safe_load(f)

        if fields is None:
            continue

        # write new sorted file
        with open(file=format_fields_path, mode="w", encoding="utf-8") as f:
            updated_fields = yaml.dump(data=fields, Dumper=YamlDumper, sort_keys=True)
            f.write(updated_fields)


def test_linting_test_files(intakes_root, test_path):
    """Ensure that keys are sorted in tests files"""
    test_fullpath = os.path.join(intakes_root, test_path)
    with open(test_fullpath) as f:
        current_test_file = json.load(f)

    new_test_file = format_test(current_test_file)
    with open(test_fullpath, "w") as out:
        json.dump(new_test_file, out, indent=2)

    assert new_test_file == current_test_file
