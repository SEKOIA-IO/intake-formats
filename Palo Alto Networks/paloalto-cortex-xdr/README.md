# Palo Alto Cortex XDR Alerts (API v3)

This format (`paloalto-cortex-xdr`) parses historical Cortex XDR Alerts API v3 payloads and endpoint events. It remains associated with automation module `PaloAltoCortexXDR` (`2bb1aaf9-a90c-411d-8e5f-c72b1b46b3d7`) and connector `971276ce-91c7-4149-a311-da076ebc54d1`.

The Alerts connector uses `/public_api/v1/alerts/get_alerts_multi_events`. Existing Alerts connectors and intake keys continue to use this format.

For Issues API v5, select the separate `PaloAltoCortexXDRIssues` automation module and `paloalto-cortex-xdr-issues` intake format. Its `/public_api/v1/issue/search` endpoint returns individual issue updates with a different field contract. See the [Issues configuration and mappings](../paloalto-cortex-xdr-issues/README.md).
