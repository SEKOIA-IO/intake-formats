import pygrok

patterns = "^(?:<%{NUMBER}>%{NUMBER} %{TIMESTAMP_ISO8601} %{NOTSPACE} %{NOTSPACE} %{NOTSPACE} LOG \\[SEKOIA@53288 intake_key=\"%{NOTSPACE}\"\\] )?%{GREEDYDATA:raw_message}$"
grok = pygrok.Grok(patterns)
syslog_msg = '<14>1 2025-10-27T12:34:56.789Z myhost app 1234 LOG [SEKOIA@53288 intake_key="xxxxxxxxxxxxxxxxxxx"] {"id":"123","uuid__":"abc"}'
json_msg = '{"id":"123","uuid__":"abc"}'

print("Syslog match:", grok.match(syslog_msg))
print("JSON match:", grok.match(json_msg))
