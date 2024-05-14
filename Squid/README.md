# Squid

## Description

Squid is a caching proxy for the Web. Providing squid logs helps
Sekoia.io detect unwanted web requests and supiscious IP
connections. It reduces bandwidth and improves response times by
caching and reusing frequently-requested web pages. Squid has
extensive access controls and makes a great server accelerator.

## Recommended configuration for Sekoia.io

To configure Squid’s logging output, you can create a new
configuration `99-sekoiaio.conf` file in the `/etc/squid/conf.d/`
directory. With most of Squid configurations (including Debian, Red
Hat, etc.), this file will automatically be used.

This file should contain two information:

- The log format used for Sekoia.io.
- The Syslog facility and priority we would like to use.

Content of `/etc/squid/conf.d/99-sekoiaio.conf` file:

```
logformat sekoiaio %ts.%03tu %6tr %>a %Ss/%03>Hs %<st %rm %ru %[un %Sh/%<a %mt "%{Referer}>h" "%{User-Agent}>h"
access_log syslog:local5.info sekoiaio
```

Then you can [configure your local Rsyslog server][doc-squid-sekoiaio]
to forward Squid logs to Sekoia.io.

[doc-squid-sekoiaio]: https://docs.sekoia.io/integrations/squid/
