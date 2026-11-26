# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-11-26

### Fixed

- Build lists and dicts without mutating them in place (`.append`, `.update`, ...), which not every Jinja engine supports
- Escape the role names in `user.changes.user.roles`, so that a quote in a role name no longer breaks the list or adds roles
