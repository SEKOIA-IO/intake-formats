# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2024-03-05 - 1.0.0

### Added

- Migrate format to Ingest

| Before the update                                                                         | After the update              |
| ----------------------------------------------------------------------------------------- | ----------------------------- |
| `url.path` could contain a domain                                                         | `url.path` is properly parsed |
| `http.response.bytes`,`http.response.body.bytes`,`http.request.bytes` are of type `float` | type `int`                    |
