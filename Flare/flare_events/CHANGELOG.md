# Changelog

## [Unreleased]

## 2026-11-02

### Added

- Add support for Flare `cc` events (stolen credit card listings, source `TXN`) through a dedicated parsing stage
- Parse new custom fields:
  - `flare.events.cc.bank`
  - `flare.events.cc.bin`
  - `flare.events.cc.brand`
  - `flare.events.cc.country`
  - `flare.events.cc.expiration`
  - `flare.events.cc.has_cvv`
  - `flare.events.cc.has_date_of_birth`
  - `flare.events.cc.has_mother_maiden_name`
  - `flare.events.cc.has_phone`
  - `flare.events.cc.has_pin`
  - `flare.events.cc.has_ssn`
  - `flare.events.cc.has_track_1`
  - `flare.events.cc.has_vbv`
  - `flare.events.cc.state`
  - `flare.events.cc.zip`
- Add smart descriptions for stolen credit card events
- Add a generic fallback smart description for events without a title (for example leaked credentials, or stealer logs without host details)

## 2026-08-03

### Added

- Add new Flare detection rules for:
    - high-severity exposure
    - leaked credentials with exposed passwords
    - stealer-log malware infection

## 2026-06-08

- Create initial Flare Events intake format.
- Add parser for common Flare envelope and major event subtypes.
- Add custom taxonomy and parsing tests.
