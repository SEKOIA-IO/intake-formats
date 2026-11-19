# Palo Alto Cortex XDR Issues (API v5)

## Choose an integration

| Source | Automation module | Intake format | API endpoint |
| --- | --- | --- | --- |
| Alerts API v3 and endpoint events | `PaloAltoCortexXDR` | `paloalto-cortex-xdr` | `/public_api/v1/alerts/get_alerts_multi_events` |
| Issues API v5 | `PaloAltoCortexXDRIssues` | `paloalto-cortex-xdr-issues` | `/public_api/v1/issue/search` |

The Issues integration is separate from the historical Alerts integration. Keep existing Alerts connectors and intake keys associated with the Alerts format. Create an intake using the Issues format for the new connector.

Despite the API v5 integration name, the Issues endpoint contains `/public_api/v1/`.

## Configure the Issues connector

The automation module is **Palo Alto Cortex XDR Issues (API v5)**, slug `paloalto_cortex_xdr_issues`, version `1.0.0`. These settings follow the supplied contract for automation-library branch `Imp/paloalto-xdr-api-v5`, commits `4eeb34b8` and `50918267` (2026-10-26).

| Module setting | Required | Handling |
| --- | --- | --- |
| `api_key` | Yes | Secret |
| `api_key_id` | Yes | Secret |
| `fqdn` | Yes | Cortex XDR API FQDN |

Select **Fetch Issues from Cortex [API v5]** (`docker_parameters: cortex_query_issues`).

| Connector argument | Required | Default |
| --- | --- | --- |
| `frequency` | No | `60` seconds (integer) |
| `chunk_size` | No | `100` (integer) |
| `intake_key` | Yes | Key of the Issues intake |
| `intake_server` | No | `https://intake.sekoia.io` |

The format manifest associates automation module UUID `9466f885-adf6-496a-b971-ed4bf1006fc8` and connector/trigger UUID `3f56671c-b8a4-4d38-94ef-26a7a20b237f`. The intake format keeps its own UUID, `424c0ef7-1b3e-4cfb-a80f-bdd573892600`.

## Event contract and mappings

The connector posts to `/public_api/v1/issue/search`, filtering `modification_time` with `gte`, sorting by descending modification time and paginating with `search_from`/`search_to`. It reads `reply.issues` and `reply.total_count`, then serializes each issue individually without changing its fields. The parser receives one raw JSON issue per event, without the response envelope or an issues array.

The connector's minimal test fixture is:

```json
{
  "issue_id": "5930923",
  "severity": "MEDIUM",
  "modification_time": 1705912900118,
  "is_excluded": false
}
```

This is a test fixture, not a production capture or an exhaustive schema.

| Source field | Normalized field | Meaning |
| --- | --- | --- |
| `issue_id` | `paloalto.cortex.xdr.issue.id` | Stable issue identity across updates |
| `modification_time` | `@timestamp` | Issue modification time, converted from Unix milliseconds to UTC |
| `modification_time` | `paloalto.cortex.xdr.issue.modification_time` | Original millisecond value; together with the issue ID, identifies the revision |
| `severity` | `log.level`, `paloalto.cortex.xdr.issue.severity` | Original severity label; no inferred numeric severity scale |
| `is_excluded` | `paloalto.cortex.xdr.issue.is_excluded` | Boolean exclusion flag, including `false`; does not imply resolution |

The format follows the historical Cortex XDR convention for alert categorization (`event.kind: alert`, `event.category: [intrusion_detection]`, `event.type: [info]`) with `event.dataset: issue`. Observer vendor and product identify Palo Alto Cortex XDR.

The connector deduplicates by the pair `issue_id` + `modification_time`. A later revision of the same issue must remain a separate event. The parser retains both values and leaves `event.id` to the ingestion platform. Modification time is neither creation time nor ingestion time, so it is not mapped to `event.created` or `event.ingested`.

Issues without `issue_id` are skipped by the connector. Excluded issues are still transmitted. Missing optional severity or exclusion values remain unset. The parser does not infer issue status, host identity, case links, descriptions or MITRE fields: these need a verified Issues API schema or reliable samples before adding mappings. Raw fields remain available in `message`.

## Collection state

The initial cursor starts five minutes before the first run. Saved cursors older than seven days are clamped to seven days. Issues state is stored separately in `context_issues.json`.

## Validation

The Issues tests cover the connector's minimal fixture, a later revision of the same issue with `is_excluded: true`, and omitted optional fields. The latter two are synthetic variations using only the verified fields.

```shell
mise run test --format paloalto-cortex-xdr-issues --format paloalto-cortex-xdr
uv run --project utils python utils/linter.py check --format paloalto-cortex-xdr-issues --format paloalto-cortex-xdr
```
