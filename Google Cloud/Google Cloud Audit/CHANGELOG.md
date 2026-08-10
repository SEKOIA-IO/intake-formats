# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-08-10

### Added

- Improve compromise-detection coverage by extracting service account key identifiers and lifetime metadata for key creation and subsequent key-based API actions after potential IMDS token theft
- Parse new ECS fields:
	- cloud.project.id
	- user.target.email
	- user.target.name
- Parse new custom fields:
	- google_cloud_audit.protoPayload.authenticationInfo.serviceAccountKeyName
	- google_cloud_audit.protoPayload.response.name
	- google_cloud_audit.service_account.email
	- google_cloud_audit.service_account.key.id
	- google_cloud_audit.service_account.key.key_algorithm
	- google_cloud_audit.service_account.key.key_origin
	- google_cloud_audit.service_account.key.key_type
	- google_cloud_audit.service_account.key.name
	- google_cloud_audit.service_account.key.private_key_type
	- google_cloud_audit.service_account.key.valid_after_time
	- google_cloud_audit.service_account.key.valid_before_time
