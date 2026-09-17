# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-08-13

### Changed

- Add a `host.name` fallback: when dedicated hostname fields are missing, derive `host.name` from machine-oriented username values (`User-Name` with `host/` prefix, or `UserName` in `UseCase=Host Lookup`), while keeping existing `user.name` mapping
