# Tests

## Test files

To validate the parser of a format, a set of test files should be hosted in the directory `tests` of the format.

A test file is a [JSON](https://json.org) document, containing an input (`input`) and an expectation (`expected`).

The input hosts two information:
- the identifier of the format the test should verify (defined in the field `sekoiaio.intake.dialect_uuid`)
- the raw event (defined in the field `message`)


The expectation contains the [structured event](structured_event.md) expected as the output of the parser for the raw event.


## Validate parser

To execute the test against the parser, go to the `utils` directory, then execute pytest with `test_formats.py` as argument:

```shell
$ cd utils
$ poetry install
$ poetry run pytest test_formats.py -vv
```

All parsers will be verified against the tests associated to their format.

To execute a subset of test, you could define some options:
- `poetry run pytest test_formats.py --changes`: to only run tests for updated parsers
- `poetry run pytest test_formats.py --module='module-name'`: to only run tests for a specific module (`module-name` correspond to the name defined in the manifest of the module)
- `poetry run pytest test_formats.py --format='format-name'`: to only run tests for a specific format (`format-name` correspond to the name defined in the manifest of the format)
