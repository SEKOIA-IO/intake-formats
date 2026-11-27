# Changelog

## [Unreleased]

## 2026-11-25

### Added

- Add the text that matched the tenant's identifiers, the English translation, Flare's topics and intents, and the CVEs mentioned: `flare.events.content_preview`, `flare.events.content_en`, `flare.events.title_en`, `flare.events.topics`, `flare.events.intents`, `flare.events.vulnerabilities`
- Add the context of stealer logs and bots: `flare.events.stealer_log.credential_hosts` (the sites of the stolen credentials, or the sites a bot holds access to), `flare.events.stealer_log.applications`, `flare.events.stealer_log.access_types`, `flare.events.stealer_log.pii_types`, `flare.events.stealer_log.analysis_labels`, `flare.events.stealer_log.secrets_count`; the location and OS of bots
- Add the context of code platform items (`driller`): `url.full`, `file.path`, the author in `user.*`, `flare.events.driller.type`, `flare.events.driller.project_name`, `flare.events.driller.dork_name`, `flare.events.driller.commit_sha`, `flare.events.driller.issue_title`, `flare.events.driller.snippets`, `flare.events.driller.secret_detected`, `flare.events.driller.secret_detection_rule_ids`
- Add the message link of chat messages (`flare.events.chat_message.message_link`), the file of attachments (`file.name`, `file.mime_type`, `flare.events.attachment.url`, `flare.events.attachment.extracted_content`), and the title and first post of forum topics

### Fixed

- Exposed services: read the host name, IP address, service, product, ASN, organization and country Flare sends. `destination.address` is now the IP address; the host name is in `host.name`

## 2026-11-24

### Changed

- Read a missing field like a `null` one, so that events keep the same parsing when the connector stops sending the fields set to `null`
- `bot` events, which have no `credentials` or `cookies` list, no longer get `flare.events.stealer_log.credentials_count: 0` and `cookies_count: 0`: both are left unset

## 2026-11-18

### Added

- Add `flare.events.truncated_fields`: the fields the connector cut to fit the intake size limit (from 0.6.7)

## 2026-11-17

### Changed

- Date events by when Flare matched the item to the tenant (`metadata.matched_at`, added by the connector from 0.6.5), as in Flare's feed, instead of the item's own date, which can be years old. Events without it keep the item's date

### Added

- Parse the item's own date in `flare.events.created_at`

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
