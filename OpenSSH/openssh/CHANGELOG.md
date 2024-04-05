# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2024-01-17 - 2.0.0

### Changed

- Migrated parser

| Before update                                                           | After update                                                                                                    |
| ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| incomplete `action.outcome_reason: 'Normal Shutdown'`                   | complete `action.outcome_reason: 'Normal Shutdown, Thank you for playing'`                                      |
| `event.outcome: success` was set when the event was successfully parsed | No more linked to parsing status but to event result (e.g. auth failed will result in `event.outcome: failure`) |
| `action.outcome_reason: pam_unix(sshd:auth): check pass`                | contains more info `action.outcome_reason: pam_unix(sshd:auth): check pass; user unknown`                       |
| `action.name: negociate`                                                | `action.name: negotiate`                                                                                        |
