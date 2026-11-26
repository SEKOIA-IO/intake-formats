# Changelog

All notable changes to this format will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial version of the BlackNoise AEV intake format, covering the two record types
  the platform reports on one intake: adversarial actions (`event.action:
  simulation_event`) and the indicators of compromise they produce (`event.action:
  ioc`), correlated through `trace.id`
