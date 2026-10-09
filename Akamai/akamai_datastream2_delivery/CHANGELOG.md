# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Fix source IP mapping (`cliIP` field name)
- Fix `akamai.datastream2.security_rules` and `akamai.datastream2.cache_status` filters
- Fix TLS version extraction

### Changed

- Map `bytes` to `http.response.bytes`
