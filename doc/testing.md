# Tests

## Test files

To validate the parser of a format, a set of test files should be hosted in the directory `tests` of the format.

A test file is a [JSON](https://json.org) document, containing an input (`input`) and an expectation (`expected`).

The input hosts two information:

- the identifier of the format the test should verify (defined in the field `sekoiaio.intake.dialect_uuid`)
- the raw event (defined in the field `message`)

The expectation contains the [structured event](structured_event.md) expected as the output of the parser for the raw event.

## Create a new test

In order to create a new test, you can use the command `mise run create-test` to generate a new test file.

The command accepts the following arguments:

- The path to the test file to create. Supply the path to the test file in the format directory.
- The raw event: You can provide the raw event as an argument of the script, or through the stdin with the argument `-`

By suppling the path of the test file in the format directory, the script will read manifest information of the format.

```shell
$ cd utils
$ uv sync  # optional, only when dependencies are not already installed
$ mise run create-test ../My\ module/my-format/tests/test1.json "My raw event"
$ cat /tmp/raw_event.txt | mise run create-test ../My\ module/my-format/tests/test2.json -
```

## Test the parser

To execute the tests against the parser, then execute `mise run test`:

```shell
$ mise run test -vv
```

All parsers will be verified against the tests associated to their format.

To execute a subset of tests, you could define some options:

- `mise run test --changes`: to only run tests for updated parsers
- `mise run test --module='<module-directory>'`: to only run tests for a specific module (`<module-directory>` correspond to the name of the module directory)
- `mise run test --format='<format-slug>'`: to only run tests for a specific format (`<format-slug>` correspond to the slug defined in the manifest of the format)

The option `--fix-expectations` can be used to automatically replace the expected files with the actual result in the test files. Use this option carefully to avoid data loss in your test files.


## Validate the format

To validate the format, you can use the command `mise run validate` to check that all tests are passing and that the format is well defined.

```shell
$ mise run validate
```
