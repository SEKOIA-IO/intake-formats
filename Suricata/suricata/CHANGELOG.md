# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2024-03-06 - 1.0.0

### Added

- code migration
- changed:

| Before update                                                                                             | After Update                                                               |
| --------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `source.port`,`destination.port` are of type float                                                        | `int`                                                                      |
| `source.port`,`destination.port` are of type float                                                        | `int`                                                                      |
| `@timestamp` not extracted                                                                                | `@timestamp` extracted from event                                          |
| `dns.answers` not correctly extracted (list of comma separated string e.g. `type: A, A, CNAME, CNAME, A`) | `dns.answers` is a list of correclty extracted fields (e.g. `type: CNAME`) |
| field moved from `action.properties.severity`                                                             | to `event.severity `                                                       |
