# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Map AnyConnect roaming client identities to `host.name`, `host.hostname`, and
  `host.ip` to improve endpoint search and asset correlation.
- Prefer the roaming-client hostname in DNS smart descriptions when available.
