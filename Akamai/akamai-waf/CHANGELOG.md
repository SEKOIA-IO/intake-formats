# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-09-09

### Added

- Parse new ECS fields:
  - `http.request.body.bytes`
- Parse new custom fields:
  - `akamai.http.request.headers.content_type`
- Enrich descriptions of custom fields

### Fixed

- Fix request/response header mix-up by extracting request payload metadata from `httpMessage.requestHeaders`:
  - `httpMessage.requestHeaders.Content-Length` raw field mapped to `http.request.body.bytes` ECS field
  - `httpMessage.requestHeaders.Content-Type` raw field mapped to `akamai.http.request.headers.content_type` custom field

### Removed

- Remove ECS fields:
  - `http.request.mime_type` mapping from `httpMessage.requestHeaders.Content-Type` raw field, because ECS requires MIME type detection from request body content rather than header values
