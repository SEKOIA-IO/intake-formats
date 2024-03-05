import csv
from io import StringIO

import requests

if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/elastic/ecs/main/generated/csv/fields.csv"

    content = requests.get(url).text

    handler = StringIO(content)
    reader = csv.reader(handler)
    next(reader)  # ignore the header

    field_names = [line[3] for line in reader]
    with open("validators/data/built_in_fields.txt", "wt") as file:
        file.write("\n".join(field_names))
