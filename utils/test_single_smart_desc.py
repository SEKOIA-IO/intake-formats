#!/usr/bin/env python3
"""
Test smart description for a single test file
Usage: poetry run python test_single_smart_desc.py <test-file-path>
Example: poetry run python test_single_smart_desc.py "Ping Identity/pingfederate/tests/http_access.json"
"""
import json
import os
import sys
from pathlib import Path
from show_smart_descriptions import SmartDescriptionManager

def test_single_file(test_file_path: str):
    """Test smart description for a single test file"""

    # Resolve paths
    intakes_path = Path(__file__).parent.parent
    full_test_path = intakes_path / test_file_path

    if not full_test_path.exists():
        print(f"❌ Test file not found: {full_test_path}")
        sys.exit(1)

    # Extract module and format from path
    parts = test_file_path.split('/')
    if len(parts) < 4:
        print(f"❌ Invalid test path format. Expected: module/format/tests/file.json")
        sys.exit(1)

    module_name = parts[0]
    format_name = parts[1]

    # Find smart descriptions file
    smart_desc_path = intakes_path / module_name / format_name / "_meta" / "smart-descriptions.json"

    if not smart_desc_path.exists():
        print(f"⚠️  No smart descriptions found at: {smart_desc_path}")
        sys.exit(1)

    # Load smart descriptions
    with open(smart_desc_path, 'r') as f:
        smart_descriptions = json.load(f)

    # Load test file
    with open(full_test_path, 'r') as f:
        test_data = json.load(f)

    expected = test_data.get('expected', {})

    # Generate smart description
    manager = SmartDescriptionManager()
    smart_desc = manager.generate_smart_desc(smart_descriptions, expected)

    # Find matched rule manually
    parsed = manager.flatten_dict(expected)
    candidates = []

    for possible_smart_desc in smart_descriptions:
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
                    condition_value_set = set()
                    if isinstance(condition_value, list):
                        condition_value_set.update(set(condition_value))
                    else:
                        condition_value_set.update(set(item.strip() for item in condition_value.split(",")))

                    if len(parsed[condition_field]) == 0 or set(parsed[condition_field]) != condition_value_set:
                        all_conditions_are_met = False
                        break
                else:
                    if parsed[condition_field] != condition_value:
                        all_conditions_are_met = False
                        break

        if all_conditions_are_met:
            candidates.append(possible_smart_desc)

    candidates = sorted(candidates, key=lambda x: len(x["conditions"]), reverse=True)
    matched_rule = candidates[0] if candidates else None

    # Display results
    print(f"📄 Test File: {test_file_path}")
    print(f"{'='*80}")
    print(f"\n✨ Smart Description:")
    print(f"   {smart_desc}\n")

    if matched_rule:
        print(f"📋 Matched Rule (conditions: {len(matched_rule['conditions'])}):")
        print(f"   Template: {matched_rule['value']}\n")

        print(f"🔍 Conditions:")
        for i, cond in enumerate(matched_rule['conditions'], 1):
            field = cond['field']
            value = cond.get('value', '<any>')
            actual_value = parsed.get(field, '<missing>')
            status = "✅" if field in parsed else "❌"
            print(f"   {status} {i}. {field} = {value} (actual: {actual_value})")
    else:
        print(f"⚠️  No specific rule matched, using default message")

    print(f"\n{'='*80}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: poetry run python test_single_smart_desc.py <test-file-path>")
        print("\nExamples:")
        print('  poetry run python test_single_smart_desc.py "Ping Identity/pingfederate/tests/http_access.json"')
        print('  poetry run python test_single_smart_desc.py "Ping Identity/pingfederate/tests/heartbeat.json"')
        sys.exit(1)

    test_single_file(sys.argv[1])
