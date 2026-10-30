# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-10-30

### Fixed

- Parse Windows logon failures (4625, 4771, 4776) relayed by Log Inspection as failed authentications
- Parse the Windows event ID of Log Inspection events in `event.code`
- Parse the Windows failure code (sub status) in `trendmicro.WindowsFailureCode`
- Keep `event.type: ["start"]` on `Signed In` events
