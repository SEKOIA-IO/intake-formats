# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2026-09-15

### Fixed

- Parse events without syslog header (e.g. forwarded through the Sekoia.io forwarder, which only keeps the message part)
- Parse `pam_unix` session closed events without uid (`session closed for user root`)

### Added

- Parse SSH authentication events:
  - `Failed <method> for <user>` for valid users and all methods
  - `Accepted <method> for <user>` for all methods (e.g. `publickey`)
  - `maximum authentication attempts exceeded`
  - `PAM <n> more authentication failures`
  - `Connection closed by authenticating user` and `Disconnected from user`
  - `user.name` from the `user=` field of `pam_unix` authentication failures
- Parse Proxmox VE web interface authentication failures (`pvedaemon`: `authentication failure; rhost=... user=... msg=...`)
- Parse systemd-logind session events (`New session`, `Session ... logged out`, `Removed session`)
- Parse sudo commands (`user.target.name`, `process.command_line`, `process.working_directory`, failure reason)
- Parse `pvestatd` storage errors (`error fetching datastores`, `storage '...' is not online`)
- Add custom fields `proxmox.proxmox_ve.session.id` and `proxmox.proxmox_ve.storage.name`
- Add smart descriptions for the new events
