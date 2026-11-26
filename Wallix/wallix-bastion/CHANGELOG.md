# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-11-16

### Added

- Parse PAM sessions of any service (including `sudo-i` and `su`), PAM `auth` authentication failures, `FAILED SU` messages and systemd-logind `New session` messages
- Set `event.action`, `event.category`, `event.type` and, when the message supports it, `event.outcome` on PAM, `su`, logind and sudo `COMMAND=` events
- Add the `wallix.terminal` and `wallix.logind.session.id` fields

### Changed

- For privilege escalation events (`sudo`, `sudo-i`, `su` PAM events and sudo `COMMAND=` lines), the initiating user is now in `user.name`/`user.id` and the target account in `user.target.name`/`user.target.id` (the target was previously stored in `user.name`)

## [Unreleased] - 2026-06-15

### Added

- Parse additional ECS fields from `sessionintegrity` logs:
    - event.end
    - event.start
    - file.extension
    - file.path
- Extract session recording metadata from unquoted `file` and `files` values in `sessionintegrity` logs

## [1.0.2] - 2023-11-02

### Added

- Extract more data from `cron` and `sudo` events

## [1.0.1] - 2023-10-23

### Added

- Extract the data from the keyboard input
