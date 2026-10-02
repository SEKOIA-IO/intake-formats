# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-10-02

### Fixed

- Fix CEF test expectations for `Application Control Detection Alert` when repeated keys are present in input
- Extract hostname from `request` before mapping `destination.domain` in `Syslog Website Accessed` events
- Anonymize `Syslog Website Accessed` fixture request host with an `example.com` domain and regenerate URL/domain expectations
