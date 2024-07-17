# Intake Parsers

**Welcome to the Sekoia.io Intakes repository!**

![Intakes](https://github.com/SEKOIA-IO/intakes/actions/workflows/main.yml/badge.svg)

This repository contains all the community parsers of Sekoia.io. Parsers are fundamental parts of a cyber analysis and detection process. They extract useful information conveyed by events and make them understandable to decision-making processes. A poor quality parser does not allow informed decision making. Conversely, a good quality parser extracts and normalizes all the useful information present in an event to maximizes its decision making.

We have created this space to ensure the quality of our parsers and allow our users to participate in their development.
Contact support@sekoia.io for questions and feedback.

## Example

```yaml
name: my-intake
pipeline:
  - name: parsed_event
    external:
      name: json.parseJSON
  - name: network
    filter: '{{parsed_event.message.log_type == "network"}}'
  - name: file
    filter: '{{parsed_event.message.log_type == "file"}}'
stages:
  network:
    actions:
      - set:
          destination.ip: "{{parsed_event.message.traffic.target}}"
          source.ip: "{{parsed_event.message.traffic.source}}"
  file:
    actions:
      - set:
          file.name: "{{parsed_event.message.file_name | lower}}"
```

# Documentation

Documentation along with tutorials and examples are available on the [documentation website](https://docs.sekoia.io/integration/develop_integration/overview/).

# Organization

Intakes are organized in modules. Each module is associated with a category or a product vendor.
An intake is made up of three directories:

1. the `_meta` directory contains all the intake metadata such as its description or the icons used for its integration into the public catalog of Sekoia.io,
2. the `ingest` directory contains the definition of the parser,
3. the `events` directory is optional and contains the definitions of `smart-descriptions` and `lookup tables` which adapt the processing and events display within Sekoia.io interfaces.

# Contributing

You can click the Fork button in the upper-right area of the screen to create a copy of this repository in your GitHub account. This copy is called a fork. Make any changes you want in your fork, and when you are ready to send those changes to us, go to your fork and create a new pull request to let us know about it.

Once your pull request is created, a Sekoia.io reviewer will take responsibility for providing clear, actionable feedback. Once merged, your changes will be included in the next release to be deployed on Sekoia.io.
