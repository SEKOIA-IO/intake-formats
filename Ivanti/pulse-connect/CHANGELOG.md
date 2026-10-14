# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-10-14 - 1.1.0

### Added

- Parse `agent` into `user_agent.original`
- Parse `sessionID` and `ivs` into `ivanti.connect_secure.session.id` and `ivanti.connect_secure.ivs`
- Parse `FBR32068` (bookmark access) and `WEB20174` (web request) events
- Set `event.outcome` for Host Checker events (`AUT24803`, `AUT24804`)

### Fixed

- Remove the trailing escaped carriage return (`#015`) added by rsyslog, which corrupted `event.code` and the parsing of `msg`
- Support Host Checker messages with multiple spaces, email usernames and a trailing session
- Trim leading spaces from `user.roles`

## 2023-10-18 - 1.0.1

### Changed

- extract more information from messages
- categorize the events
