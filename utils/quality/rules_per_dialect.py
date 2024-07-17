import os
import yaml
import requests
import argparse

def read_dialect_uuid(format_path):
    """
    Read the 'uuid' field from the manifest.yml file in the _meta directory of the format.
    """
    manifest_path = os.path.join(format_path, "_meta", "manifest.yml")
    if os.path.isfile(manifest_path):
        try:
            with open(manifest_path, 'r') as file:
                manifest_content = yaml.safe_load(file)
                return manifest_content.get("uuid")
        except Exception as e:
            print(f"Failed to read {manifest_path}: {e}")
    return None

def count_unique_sets_in_dict(data, unique_sets):
    """
    Recursively traverse YAML data to find unique field names within 'set' keys.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "set":
                # Assuming the value corresponding to 'set' is a dictionary
                for sub_key in value.keys():
                    unique_sets.add(sub_key)
            elif isinstance(value, (dict, list)):
                count_unique_sets_in_dict(value, unique_sets)
    elif isinstance(data, list):
        for item in data:
            count_unique_sets_in_dict(item, unique_sets)

def extract_fields_from_sigma(sigma_dict):
    """
    Extract fields and condition from a Sigma rule dictionary.
    """
    fields = {}
    expected_dialect_uuid = None
    detection_clause = sigma_dict.get('detection', {})
    if detection_clause:
        for key, value in detection_clause.items():
            if key != 'condition' and isinstance(value, dict):
                extracted_keys = set()
                for field_key in value.keys():
                    # Retain only the part before the '|', if present
                    cleaned_key = field_key.split('|')[0]
                    extracted_keys.add(cleaned_key)
                fields[key] = extracted_keys
            elif key == 'condition':
                condition = value
            # Check for dialect_uuid in the selection fields
            if isinstance(value, dict):
                for field_key, field_val in value.items():
                    if field_key == 'sekoiaio.intake.dialect_uuid':
                        expected_dialect_uuid = field_val
    else:
        condition = None

    return fields, condition, expected_dialect_uuid

def check_condition(fields, condition, unique_fields):
    """
    Check if the unique fields satisfy the condition of the Sigma pattern.
    """
    # Handle AND conditions
    if condition and ' and ' in condition:
        conditions = condition.split(' and ')
        return all(check_condition(fields, cond.strip(), unique_fields) for cond in conditions)

    # Handle OR conditions
    if condition and ' or ' in condition:
        conditions = condition.split(' or ')
        return any(check_condition(fields, cond.strip(), unique_fields) for cond in conditions)

    # Handle the NOT condition
    if condition and condition.startswith('not '):
        return not check_condition(fields, condition[4:].strip(), unique_fields)

    # Handle single condition
    if condition in fields:
        required_fields = fields[condition]
        if "sekoiaio.intake.dialect_uuid" in required_fields:
            required_fields.remove("sekoiaio.intake.dialect_uuid")
        return required_fields.issubset(unique_fields)

    return False

def process_parser_yml(file_path, sigma_patterns, dialect_uuid):
    """
    Process the parser.yml file, extract unique fields, and compare them with Sigma patterns.
    """
    unique_fields = set()

    try:
        with open(file_path, 'r') as file:
            content = yaml.safe_load(file)
            count_unique_sets_in_dict(content, unique_fields)

        # Add the default field with the correct value
        unique_fields.add("sekoiaio.intake.dialect_uuid")
        #unique_fields_dict["sekoiaio.intake.dialect_uuid"] = dialect_uuid

        print(f"Unique fields in {file_path}: {len(unique_fields)}")
        print(f"Fields: {', '.join(unique_fields)}")

        # Find Sigma patterns that potentially match the unique fields
        matching_patterns = []
        for sigma in sigma_patterns:
            fields, condition, expected_dialect_uuid = extract_fields_from_sigma(sigma['payload_dict'])
            # Compare dialect UUIDs if expected one is specified in the Sigma pattern
            if expected_dialect_uuid and expected_dialect_uuid != dialect_uuid:
                continue
            if check_condition(fields, condition, unique_fields):
                matching_patterns.append(sigma)

        print(f"Potentially matching Sigma patterns for {file_path}: {len(matching_patterns)}")
        for sigma in matching_patterns:
            print(f" - {sigma['name']}")
            print(sigma['payload'])  # Print the complete Sigma pattern

    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

def traverse_root_directory(root_dir, sigma_patterns, target_format=None):
    """
    Traverse all directories at the root level.
    """
    for module_name in os.listdir(root_dir):
        module_path = os.path.join(root_dir, module_name)

        if os.path.isdir(module_path) and module_name != "utils":
            traverse_module(module_path, sigma_patterns, target_format)

def traverse_module(module_path, sigma_patterns, target_format=None):
    """
    Traverse all format directories within the module.
    """
    for format_name in os.listdir(module_path):
        # Check if we should process this format
        if target_format and format_name != target_format:
            continue

        format_path = os.path.join(module_path, format_name)

        if os.path.isdir(format_path) and format_name != "_meta":
            traverse_format(format_path, sigma_patterns)

def traverse_format(format_path, sigma_patterns):
    """
    Navigate to the "ingest" directory.
    """
    # Retrieve the dialect UUID for the format
    dialect_uuid = read_dialect_uuid(format_path)

    ingest_path = os.path.join(format_path, "ingest")

    if os.path.isdir(ingest_path):
        parser_yml_path = os.path.join(ingest_path, "parser.yml")

        if os.path.isfile(parser_yml_path):
            process_parser_yml(parser_yml_path, sigma_patterns, dialect_uuid)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process parser.yml files and compare with Sigma patterns.")
    parser.add_argument('--format', help="Specify a particular format to process.")
    args = parser.parse_args()

    root_directory = "../.."
    target_format = args.format

    # Perform the HTTP request once and extract Sigma patterns
    try:
        response = requests.get('https://api.sekoia.io/v1/sic/conf/rules-catalog/multi-tenant/rules?match[type]=sigma&verified=true',
        headers={'Authorization': 'Bearer XXXX'})

        if response.status_code == 200:
            response_json = response.json()
            sigma_patterns = []
            for item in response_json.get('items', []):
                try:
                    sigma_dict = yaml.safe_load(item['payload'])
                    sigma_patterns.append({
                        'name': item['name'],
                        'payload': item['payload'],
                        'payload_dict': sigma_dict
                    })
                except yaml.YAMLError as e:
                    print(f"Failed to parse Sigma pattern: {e}")
        else:
            print(f"HTTP request failed with status code: {response.status_code}")
            sigma_patterns = []

    except Exception as e:
        print(f"Failed to perform HTTP request: {e}")
        sigma_patterns = []

    # Traverse the root directory and process each parser.yml file
    traverse_root_directory(root_directory, sigma_patterns, target_format)