# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2023-11-28 - 1.1.0

### Changed

- Migrate to ingest parser

| Before update                                              | After update                                                                                                                               |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `file.created: Mar 14, 2024 @ 11:18:36.000`                | formatted as `file.created: 2024-03-14T10:18:36Z`                                                                                          |
| `file.ctime: Mar 14, 2024 @ 11:18:36.000`                  | formatted as `file.ctime: 2024-03-14T10:18:36Z`                                                                                            |
| `file.size: 18,383` float                                  | int `file.size: 18383`                                                                                                                     |
| `source.address == source.ip`                              | if `source.domain` exists `source.address = source.domain` (this change result in every domain part being split to it's associated field.) |
| `postfix_relay_service`                                    | `postfix.relay_service`                                                                                                                    |
| `postfix_scache_timestamp`                                 | `postfix.scache_timestamp`                                                                                                                 |
| `os.family: linux, os.platform: linux`                     | removed                                                                                                                                    |
| `postfix_relay_service`                                    | removed                                                                                                                                    |
| `postfix_scache_timestamp`                                 | removed                                                                                                                                    |
| `"outcome_reason": "SMTP code do not match in dictionary"` | removed                                                                                                                                    |
| Support for `log.syslog.appname: postfix/scache`           | removed (no valuable info to extract)                                                                                                      |
| `email.from` and `email.to` could contain an email address | the content moved to valid ECS fields such as `email.from.address`                                                                         |
