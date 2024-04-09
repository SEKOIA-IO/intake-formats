import json

import yaml


class YamlDumper(yaml.SafeDumper):
    """This class adds linebreak between each root keys in fields.yml"""

    def write_line_break(self, data=None):
        super().represent_scalar("tag:yaml.org,2002:str", data, style='"')
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


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


def sort_json_keys(test_file: dict) -> dict:
    """
    Perform sorting on all fields(including lists) using custom encoder to make sure we have a consistent order
    The most simple way is to encode to json string and decode it back :)
    """
    return json.loads(json.dumps(test_file, sort_keys=True, cls=JsonSorterEncoder))


def format_input(test_file: dict) -> dict:
    test_input = sort_json_keys(test_file)
    message = test_input["message"]
    del test_input["message"]
    return {"message": message} | test_input


def format_expected(test_file):
    expected = sort_json_keys(test_file)

    if "event" in expected:
        event = {"event": expected["event"]}
        del expected["event"]
        expected = event | expected

    message = {"message": expected["message"]}
    del expected["message"]
    expected = message | expected

    return expected


def format_test(test_file: dict) -> dict:
    # keep the message on top of each parts

    return {
        "input": format_input(test_file["input"]),
        "expected": format_expected(test_file["expected"]),
    }
