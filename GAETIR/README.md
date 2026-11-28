# GAETIR

GAETIR provides email security decisions and observed mailbox feedback through an outbound HTTPS feed.

## Formats

- **GAETIR Email Security** (`gaetir-email`): normalizes `gaetir.decision.v2` and `gaetir.feedback.v1` events, with disclosure-aware metadata, Smart Descriptions and explicit threat/failure classifications.

Processing completion, intended actions, recorded action results and observed folder movement remain distinct. Feedback does not prove a human action or establish ground truth. Attachment metadata is an array of JSON strings, one record per attachment.

Configuration documentation is proposed in [the companion documentation PR](https://github.com/SEKOIA-IO/documentation/pull/3410). Hosted evaluation and final homologation remain pending. This module contains only integration artifacts and synthetic fixtures; private GAETIR application code is not included.
