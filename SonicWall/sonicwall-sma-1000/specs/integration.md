# SonicWall Secure Mobile Access (SMA) 1000 series 12.5

Product vendor: SonicWall
Created by: Anthony David
Workflow status: Development
Integration type: Intake format
Status: In progress
Creation date: February 2, 2026 3:32 PM
Category: Network Device
Core: Yes
Data type: Telemetry
Document type: Specification
Logo: SonicWall%20Secure%20Mobile%20Access%20(SMA)%201000%20series%201/logo.png
Out of beta communication: Not ready
Planned: August 2026
Potential high usage: No
Prime: Yes
Rational: Sonicwall SMA 1000 / OCD MicroSoc (https://app.notion.com/p/Sonicwall-SMA-1000-OCD-MicroSoc-2e9494db63848021b9e9cea3b8faf57a?pvs=21)

# Architecture

## Commercial URL of the product

- [https://www.sonicwall.com/fr-fr/products/remote-access/secure-mobile-access-1000-series](https://www.sonicwall.com/fr-fr/products/remote-access/secure-mobile-access-1000-series)

## Type of technology

- ~~Cloud~~
- On-prem

### Reason for choosing technology type

- The SonicWall Secure Mobile Access (SMA) 1000 Series is a Network Security Appliance (SSL VPN Gateway), so it’s is a physical device

## Product version (on-prem)

- Current version to integrate: SonicWall Secure Mobile Access (SMA) 100**0** Series, version **12.5**

[https://www.sonicwall.com/support/technical-documentation/docs/sma_1000-12-5-release_notes/Content/release_notes.htm](https://www.sonicwall.com/support/technical-documentation/docs/sma_1000-12-5-release_notes/Content/release_notes.htm)

[https://www.mysonicwall.com/muir/ui/workspace/m/feature/products](https://www.mysonicwall.com/muir/ui/workspace/m/feature/products)

- Previously integrated version: SonicWall Secure Mobile Access (SMA) 100 Series, version **10.2**

[https://www.sonicwall.com/support/technical-documentation/docs/sma_100-10.2.2-release_notes/Content/release_notes.htm](https://www.sonicwall.com/support/technical-documentation/docs/sma_100-10.2.2-release_notes/Content/release_notes.htm)

[https://docs.sekoia.io/integration/categories/network_security/sonicwall_sma/](https://docs.sekoia.io/integration/categories/network_security/sonicwall_sma/)

### Prerequisites to use integration (module, plan, role, permission, etc..)

- 

## Detection use-case

Sekoia considers the following scenarii of detection:

- **Threat oriented**: Raise a new alert in Sekoia using available detection engine, to detect threats that were not originally detected by this integration, based on new built-in rules and CTI rule
—> Indeed the events are not enough relevant to automatically raise an alert
- **~~Pass-through**: Raise a new alert in Sekoia each time a security event is created in this integration~~

## Available event types

[https://www.sonicwall.com/support/technical-documentation/docs/sma_1000-12-5-admin_guide/Content/Appendix/log-file-output-formats.htm](https://www.sonicwall.com/support/technical-documentation/docs/sma_1000-12-5-admin_guide/Content/Appendix/log-file-output-formats.htm)

- System Message Log
- Management Message Log
- Management Audit Log
- Management Access Log
- Network Tunnel Audit Log
- Web Proxy Audit Log
- Unregistered Device Log Messages
- WorkPlace Logs

## **Chosen event types**

| Event type | Description |
| --- | --- |
| All previously listed logs
To confirm with @Sébastien Quioc  |  |

## **Chosen event fields**

| Field name | Description |
| --- | --- |
|  |  |

## Log collection method

### Available methods

- PUSH

### Chosen method

- PUSH

SonicWall is providing us with the logs, we need to see if we need to set up a Sekoia Forwarder

### Reason for choosing this **method**

- 

### Prerequisites for log collection

- 

### Log collection schema

- 

# Specification

# GitHub repositories

Location of the automation module: [https://github.com/SEKOIA-IO/automation-library/tree/develop/SonicWall](https://github.com/SEKOIA-IO/automation-library/tree/develop/SonicWall)

Location of the intake format: [https://github.com/SEKOIA-IO/intake-formats/tree/develop/SonicWall](https://github.com/SEKOIA-IO/intake-formats/tree/develop/SonicWall)

Location of the documentation: [https://github.com/SEKOIA-IO/documentation](https://github.com/SEKOIA-IO/documentation)

# **Context**

### Product version

[SonicWall Secure Mobile Access (SMA) 1000 series](https://app.notion.com/p/SonicWall-Secure-Mobile-Access-SMA-1000-series-2fb494db638480a18488e19ebf40c56f?pvs=21) 

### **Vendor description**

[SonicWall](https://app.notion.com/p/SonicWall-e6092b5d0d3642d58a495005c55a8cb2?pvs=21) 

### **Integration**

This development consist of:

- The renaming of the existing SonicWall/sonicwall-sma intake format ([https://github.com/SEKOIA-IO/intake-formats/tree/develop/SonicWall/sonicwall-sma](https://github.com/SEKOIA-IO/intake-formats/tree/develop/SonicWall/sonicwall-sma)), for parsing SonicWall SMA 100 Series (10.2) logs
Rename *SonicWall/sonicwall-sma* to *SonicWall/sonicwall-sma-100*
- The creation of a new intake format, *SonicWall/sonicwall-sma-1000*, for parsing SonicWall SMA 1000 Series (12.5) logs
- The documentation about this integration

Indeed, as SonicWall SMA 100 Series (10.2) and 1000 Series (12.5) logs have different formats, we must create a new *SonicWall/sonicwall-sma-1000* intake format

# **Intake format**

## **Definition**

SonicWall SMA 1000 Series (12.5) logs are structured, text-based records (mostly syslog-like and HTTP access formats, with some XML exports) that encode timestamped security and system events as ordered fields for monitoring, auditing, and incident analysis

## **Samples**

Samples can be found in the official SonicWall SMA 1000 Series (12.5) documentation:
[https://www.sonicwall.com/support/technical-documentation/docs/sma_1000-12-5-admin_guide/Content/Appendix/log-file-output-formats.htm](https://www.sonicwall.com/support/technical-documentation/docs/sma_1000-12-5-admin_guide/Content/Appendix/log-file-output-formats.htm)

## **Parser**

**Specs are available here:**

[Specs - SonicWall SMA 1000 Series 12.5](https://app.notion.com/p/Specs-SonicWall-SMA-1000-Series-12-5-380494db6384807685a2f5d45a49ca76?pvs=21)

Use a single parser with a shared normalization stage and one `set_<log_format>` stage per log format (System Message Log, Management Access Log, Network Tunnel Audit Log, etc.), each gated by a filter after an initial format-detection step

Please see the following draft parser:
[https://github.com/SEKOIA-IO/intake-formats/blob/feature/sonicwall_sma_100_series_integration/SonicWall/sonicwall-sma-12.5/ingest/parser.yml](https://github.com/SEKOIA-IO/intake-formats/blob/feature/sonicwall_sma_100_series_integration/SonicWall/sonicwall-sma-12.5/ingest/parser.yml)

In short: detect once, normalize once, then map the fields in dedicated `set_<log_format>` stages.

# **Documentation**

Add the new *docs/integration/categories/network_security/sonicwall-sma-1000.md* entry in the Sekoia.io documentation for SonicWall SMA 1000 Series (12.5):
[https://github.com/SEKOIA-IO/documentation/tree/main/docs/integration/categories/network_security](https://github.com/SEKOIA-IO/documentation/tree/main/docs/integration/categories/network_security)

This Markdown file should expose what is this integration and how to configure it

You can draw inspiration from the existing documentation, for parsing SonicWall SMA 100 Series (10.2) logs, especially by keeping its structure (sections, etc.):

[https://github.com/SEKOIA-IO/documentation/blob/main/docs/integration/categories/network_security/sonicwall_sma.md](https://github.com/SEKOIA-IO/documentation/blob/main/docs/integration/categories/network_security/sonicwall_sma.md)

## Frontmatter

As [frontmatter](https://daily-dev-tips.com/posts/what-exactly-is-frontmatter/), add the identifier of the intake, its name and the type of the integration

Example for SonicWall SMA 100 Series (10.2):

```markdown
uuid: 622999fe-d383-4d41-9f2d-eed5013fe463
name: SonicWall SMA 100 Series
type: intake
```

## Complete sections

### Overview section

Create an “Overview” section that describes the integration

Retrieve and copy/paste the description from the *manifest.yml* file you will have created in your intake-formats PR, and complete/verify the following documentation block:

```markdown
## Overview

<Copy/paste the integration description from the _manifest.yml_ file here>

- **Vendor**: SonicWall
- **Supported environment**: On prem
- **Version compatibility**: 12.5
- **Detection based on**: Telemetry
- **Supported application or feature**: DNS records
```

### Configure section

To create the “Configure” section, you should be able to access the SonicWall SMA 1000 Series (12.5) Appliance Management Console, which is slightly different from the previous SonicWall SMA 100 Series (10.2) one

To access the SonicWall SMA 1000 Series (12.5) Appliance Management Console, follow these instructions:

```markdown
1. Push your ed25519 ssh public key on the Bare-metal OVH Debian OS

Ask the person in charge to push your ed25519 ssh public key 

2. In a first terminal (keep it opened), run the following command:

```bash
ssh -L 8443:192.168.122.36:8443 firstname_lastname@51.77.165.22
```

3. Launch your browser (Google Chrome) on the following url

```text
https://127.0.0.1:8443
```

N.B.: Your browser will likely warn you about an unsecured connection and ask you to accept the certificate

4. Fill in with the Bitwarden credentials

Use the Bitwarden credentials saved under `SonicWall - SMA Appliance (OVH)`
```

Then complete/verify the following documentation block:

```markdown
## Configure

This setup guide will show you how to forward your SonicWall SMA 1000 Series (12.5) logs to Sekoia.io by means of a syslog transport channel.

### Prerequisites

- Have an internal log concentrator (Rsyslog)

### Enable Syslog forwarding for SonicWall SMA

1. Log in the SonicWall SMA Appliance Management Console
2. Go to `Monitoring > Logging > Configure Logging`
3. In the `Services Log Level` section, define the severity level of log messages
4. In the `Syslog Configuration` section, type the IP address and the port of your log concentrator as primary syslog server (`Server #1`)

    ![SonicWall SMA settings](/assets/instructions/sonicwall_sma_1000/logging_settings.png)

5. Click `Save` to save your logging settings

### Create the intake

Go to the [intake page](https://app.sekoia.io/operations/intakes) and create a new intake from the SonicWall SMA 1000 Series format

### Forward logs to Sekoia.io

Please consult the [Syslog Forwarding](/integration/ingestion_methods/syslog/sekoiaio_forwarder.md) documentation to forward these logs to Sekoia.io
```

The */assets/instructions/sonicwall_sma_1000/logging_settings.png* file:

![logging_settings.png](SonicWall%20Secure%20Mobile%20Access%20(SMA)%201000%20series%201/logging_settings.png)

## Include shared content resources

Add the following lines, to include auto-generated information:

```json
{!_shared_content/operations_center/integrations/generated/<identifier>.md!}

{!_shared_content/integration/detection_section.md!}

{!_shared_content/operations_center/detection/generated/suggested_rules_<identifier>_do_not_edit_manually.md!}

{!_shared_content/operations_center/integrations/generated/<identifier>.md!}
```

## Reference the integration page in MKDocs

Reference the integration page in the following file:
[https://github.com/SEKOIA-IO/documentation/blob/main/mkdocs.yml](https://github.com/SEKOIA-IO/documentation/blob/main/mkdocs.yml)

# **Deliverable**

## 1. PR intake-formats

The 1st deliverable is as a PR on the [https://github.com/SEKOIA-IO/intake-formats](https://github.com/SEKOIA-IO/intake-formats) repository with:

- The renaming of the existing SonicWall/sonicwall-sma intake format ([https://github.com/SEKOIA-IO/intake-formats/tree/develop/SonicWall/sonicwall-sma](https://github.com/SEKOIA-IO/intake-formats/tree/develop/SonicWall/sonicwall-sma)), for parsing SonicWall SMA 100 Series (10.2) logs
Rename *SonicWall/sonicwall-sma* to *SonicWall/sonicwall-sma-100*
- The creation of a new intake format, *SonicWall/sonicwall-sma-1000*, **with the following files:
    - A *_meta/* directory with:
        - A manifest *SonicWall/sonicwall-sma-1000/_meta/manifest.json* with the name, a slug, a description of the format and a list of datasources
        - A logo *SonicWall/sonicwall-sma-1000/_meta/logo.png* with background removed (see [https://www.remove.bg/](https://www.remove.bg/))
        - A list of smart-descriptions in *SonicWall/sonicwall-sma-1000/_meta/smart-descriptions.json*
        - A list of custom fields in the taxomony *SonicWall/sonicwall-sma-1000/_meta/fields.yml*
    - A list of tests in *SonicWall/sonicwall-sma-1000/tests/*, based on the sample logs provided by the official SonicWall documentation or the specs
    - The parser *SonicWall/sonicwall-sma-1000/parser.yml*

## 2. PR documentation

The 2nd deliverable is as a PR on the [https://github.com/SEKOIA-IO/documentation](https://github.com/SEKOIA-IO/documentation) repository with:

- The renaming/update of the existing documentation, from *docs/integration/categories/network_security/sonicwall-sma.md* to *docs/integration/categories/network_security/sonicwall-sma-100.md*
- The creation of the new documentation *docs/integration/categories/network_security/sonicwall-sma-1000.md*

[Specs - SonicWall SMA 1000 Series 12.5](https://app.notion.com/p/Specs-SonicWall-SMA-1000-Series-12-5-380494db6384807685a2f5d45a49ca76?pvs=21)