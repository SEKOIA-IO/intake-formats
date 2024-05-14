# Suricata

## Description

Suricata is a free and open source, mature, fast and robust network threat detection engine.
Suricata inspects the network traffic using a powerful and extensive rules and signature language,
and has powerful Lua scripting support for detection of complex threats.

## Recommended configuration for Sekoia.io

Suricata leverages its EVE output module to report alerts, metadata, file info and protocol records in JSON. As described in the official documentation, this module can report its findings through the syslog facility.

### Configure Suricata to forward events to rsyslog

Open the Suricata configuration file (please note that the path to the configuration file may change depending on the OS and your configuration):

```bash
sudo vim /etc/suricata/suricata.yaml
```

Paste the following declaration in your suricata configuration to trigger the production of syslog entries under the `local5` facility:

```
outputs:
  - eve-log:
      enabled: yes
      type:syslog
      identity: suricata
      facility: local5
      level: Info
      types:
        - alert
        - http
        - dns
        - tls
```

Then you can [configure your local Rsyslog server][doc-suricata-sekoiaio]
to forward Suricata logs to Sekoia.io.

[doc-suricata-sekoiaio]: https://docs.sekoia.io/integrations/suricata/
