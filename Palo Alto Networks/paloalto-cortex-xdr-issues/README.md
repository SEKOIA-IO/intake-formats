# Palo Alto Cortex XDR Issues

This format parses issue and case records from the Palo Alto Cortex XDR v5 Issues API. Cortex XDR v3 alerts and endpoint events remain in the separate `paloalto-cortex-xdr` format.

Issue identifiers, status, severity, category, action status, description, associated case IDs, and exclusion state are mapped to `paloalto.cortex.xdr.issue.*`. Host identity and IP addresses use ECS host and agent fields; MITRE technique and tactic labels are split into their respective ECS ID and name fields.

The API's `is_excluded` boolean is retained as `paloalto.cortex.xdr.issue.is_excluded`; it is not treated as the v3 alert's `is_whitelisted` field.
