# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2024-02-21 - 1.0.0

### Added

- code migration
- changed:

| Before update                                                                                                           | After Update                                                                                                                                                                                                                                                                     |
| ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `source.port` is a float                                                                                                | `source.port` is an int                                                                                                                                                                                                                                                          |
| `source.nat.port` is a float                                                                                            | `source.nat.port` is an int                                                                                                                                                                                                                                                      |
| `destination.port` is a float                                                                                           | `destination.port` is an int                                                                                                                                                                                                                                                     |
| `destination.port` is a float                                                                                           | `destination.port` is an int                                                                                                                                                                                                                                                     |
| `action.properties.originsicname: 'CN\\=ertfw01,O=foomgmt.foobar.local.zazgch'`                                         | `'originsicname': 'CN=ertfw01,O=foomgmt.foobar.local.zazgch'`                                                                                                                                                                                                                    |
| `action.properties` is of type list[dict]                                                                               | `action.properties` is of type dict (no impact expected)                                                                                                                                                                                                                         |
| `network.transport` was not always translated to the equivalent string value (ex. 1=>imcp)                              | `network.transport` is always translated to string                                                                                                                                                                                                                               |
| truncated content for `action.properties.encryption_methods`, `action.properties.ike_ids`, `action.properties.ike_mode` | the content of the field is complete (e.g. `ESP` become `ESP: AES-256 + SHA1 + PFS (group 5)`                                                                                                                                                                                    |
| fix user_agent parsing of logs type `geo_protection` (e.g. previously `user_agent.original: Google Chrome`)             | `user_agent.device.name: Other user_agent.name: Chrome user_agent.original: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36 user_agent.os.name: Windows user_agent.os.version: 10 user_agent.version: 88.0.4324 ` |
