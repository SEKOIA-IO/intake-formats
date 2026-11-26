# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2026-11-26

### Added

- Extract the user's full name and email from the most granular identity
  - ECS fields: `user.full_name`, `user.email`

### Fixed

- Set the host name from the `Anyconnect Roaming Client` identity instead of the user identity
  - ECS fields: `host.name`, `host.hostname`
