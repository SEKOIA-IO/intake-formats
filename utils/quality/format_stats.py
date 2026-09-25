import os
import yaml
from collections import defaultdict

def extract_fields_from_yaml(data):
    fields = set()
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "set":
                fields.update(value.keys())
            if isinstance(value, (dict, list)):
                fields.update(extract_fields_from_yaml(value))
    elif isinstance(data, list):
        for item in data:
            fields.update(extract_fields_from_yaml(item))
    return fields

def extract_fields_from_fields_yml(file_path):
    fields = set()
    if os.path.exists(file_path):
        with open(file_path, 'r') as stream:
            try:
                yaml_data = yaml.safe_load(stream)
                if isinstance(yaml_data, dict):
                    for key in yaml_data.keys():
                        fields.add(key)
                print(f"Extracted fields from fields.yml: {fields}")  # Debugging
            except yaml.YAMLError as exc:
                print(f"Error parsing {file_path}: {exc}")
    return fields

def main():
    repo_dir = "../../"  # Chemin vers votre dépôt local
    combined_fields = defaultdict(lambda: {'ingest': set(), 'meta': set()})
    
    for root, dirs, files in os.walk(repo_dir):
        print(f"Visiting directory: {root}")  # Debugging
        if root == repo_dir and 'utils' in dirs:
            dirs.remove('utils')
        if 'ingest' in dirs:  # Check if there is an ingest directory
            ingest_dir = os.path.join(root, 'ingest')
            fields_file = os.path.join(root, '_meta', 'fields.yml')
            parent_dir_name = os.path.basename(root)  # Get the name of the parent directory
            
            for file in os.listdir(ingest_dir):
                if file == 'parser.yml':
                    file_path = os.path.join(ingest_dir, file)
                    print(f"Processing file: {file_path}")  # Debugging
                    with open(file_path, 'r') as stream:
                        try:
                            yaml_data = yaml.safe_load(stream)
                            print(f"Parsed YAML data: {yaml_data}")  # Debugging
                            fields = extract_fields_from_yaml(yaml_data)
                            combined_fields[parent_dir_name]['ingest'].update(fields)
                            print(f"Updated ingest fields for {parent_dir_name}: {combined_fields[parent_dir_name]['ingest']}")  # Debugging
                        except yaml.YAMLError as exc:
                            print(f"Error parsing {file_path}: {exc}")
            
            # Extract fields from fields.yml
            fields = extract_fields_from_fields_yml(fields_file)
            combined_fields[parent_dir_name]['meta'].update(fields)
    
    total_ingest_elements = 0
    total_meta_elements = 0
    min_ingest_elements = float('inf')
    max_ingest_elements = float('-inf')
    min_meta_elements = float('inf')
    max_meta_elements = float('-inf')
    min_ingest_name = None
    max_ingest_name = None
    min_meta_name = None
    max_meta_name = None

    for name, field_types in combined_fields.items():
        ingest_fields = field_types['ingest']
        num_ingest_fields = len(ingest_fields)
        meta_fields = field_types['meta']
        num_meta_fields = len(meta_fields)
        
        total_ingest_elements += num_ingest_fields
        total_meta_elements += num_meta_fields
        
        if num_ingest_fields < min_ingest_elements:
            min_ingest_elements = num_ingest_fields
            min_ingest_name = name
        if num_ingest_fields > max_ingest_elements:
            max_ingest_elements = num_ingest_fields
            max_ingest_name = name
        
        if num_meta_fields < min_meta_elements:
            min_meta_elements = num_meta_fields
            min_meta_name = name
        if num_meta_fields > max_meta_elements:
            max_meta_elements = num_meta_fields
            max_meta_name = name

        print(f"Name: {name}")
        print(f"Number of ingest elements: {num_ingest_fields}")
        for field in sorted(ingest_fields):
            print(f"  - {field}")
        
        print(f"Number of meta elements: {num_meta_fields}")
        for field in sorted(meta_fields):
            print(f"  - {field}")
        
        print()  # Ajouter une ligne vide entre les groupes

    if combined_fields:
        average_ingest_elements = total_ingest_elements / len(combined_fields)
        average_meta_elements = total_meta_elements / len(combined_fields)
        
        print(f"Average number of ingest elements per name: {average_ingest_elements:.2f}")
        print(f"Name with the least ingest elements: {min_ingest_name} ({min_ingest_elements} elements)")
        print(f"Name with the most ingest elements: {max_ingest_name} ({max_ingest_elements} elements)")
        
        print(f"Average number of meta elements per name: {average_meta_elements:.2f}")
        print(f"Name with the least meta elements: {min_meta_name} ({min_meta_elements} elements)")
        print(f"Name with the most meta elements: {max_meta_name} ({max_meta_elements} elements)")

if __name__ == "__main__":
    main()