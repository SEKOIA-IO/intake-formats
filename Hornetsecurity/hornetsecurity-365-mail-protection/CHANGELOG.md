# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 2026-09-23

### Added

- Parse `smtp_status` and `smtp_status_code` into `hornetsecurity.spam_malware_protection.smtp_status` and `hornetsecurity.spam_malware_protection.smtp_status_code` to identify emails relayed by the gateway
- Add tests for a blocked threat (no SMTP status) and a delivered email

## 2025-04-01

Initial version
