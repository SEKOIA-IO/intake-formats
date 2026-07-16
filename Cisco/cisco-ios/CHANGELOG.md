# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-07-16

### Added

- Parse custom fields:
	- `cisco.ios.ssh.terminal`
	- `cisco.ios.ssh.cipher`
	- `cisco.ios.ssh.hmac`

## 2026-06-16

### Added

- Parse ECS dynamic fields for HTTPS connection logs without Cisco header:
    - destination.ip
    - event.action
    - event.category
    - event.code
    - event.outcome
    - event.reason
    - event.type
    - network.protocol
    - source.ip
    - user.name
- Add smart descriptions for HTTPS connection accepted and terminated events

### Changed

- Update parser fallback to handle description-only messages and to map HTTPS connection states to ECS
