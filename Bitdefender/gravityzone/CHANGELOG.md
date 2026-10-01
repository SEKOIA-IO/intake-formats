# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Map `agent.id` from `BitdefenderGZEndpointId`, so EDR agent identifiers are attached to host assets

### Fixed

- `host.name` now holds the short hostname taken from `BitdefenderGZComputerFQDN`, and the remaining
  labels go to `host.domain`. The full FQDN in `host.name` was rejected by asset discovery, which
  expects a bare hostname, so no asset was created for those events.
