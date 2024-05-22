# Utils

## Summary

* [Utils](#utils)
	* [How to ?](#how-to-)
		* [New module](#new-module)
		* [New intake](#new-intake)
        * [Publish intake-format](#publish-intake-format-to-sekoiaio)
        * [Send events to platform](#send-events-to-sekoiaio)
* [Parsers](#parsers)
* [Events](#events)
* [Manifests](#manifests)


markdown.markdown(some_text, extensions=[MyExtClass(), 'myext', 'path.to.my.ext:MyExtClass'])

## How to ?

First `clone intakes` repository.
Then copy and paste {{module_slug}} or {{intake_slug}} repository.

### New module
  
A module is a defined by a product brand with several products using same properties.
Module allow similar features to be grouped in one place to avoid code redundancy.
A module can be composed of :  
.   
├──  ([event](#events))  
│           ├──  [lookups.json](#lookupsjson)  
│           └──  [smart-description.json](#smart-descriptionsjson)  
├──  (ingest)   
│          └──  [stages.yml](#common-stages)   
└──  **README.md**

	
### New intake
  
.   
├──  **ingest**  
│          └──  [parser.yml](#parsers)  
├──  **meta**  
│          ├── (logo.png)  
│          └──  [manifest.yaml](#manifests)  
└──  ([event](#events))  
            ├──  [lookups.json](#lookupsjson)  
            └──  [smart-description.json](#smart-descriptionsjson)  


(...) : not mandatory


# Parsers

Parses the event according to the intakes configuration.
The file configuration is in the ingest repository and called parser.yml.
Some [common stages](#common-stages) could be put into the module repository called ingest, in the file stages.yml.

## General

An intake consists is a sequence of stages organized under a pipeline that modifies the event on the fly.

The following pipeline is made of three stages (`stage1`, `stage2` and `stage3`)
with the execution of `stage2` and `stage3` conditonned to a filter that evaluates the value of the event field `message.log_type` at the end of `stage1`.
```yaml
pipeline:
 - name: stage1
 - name: stage2
   filter: '{{stage1.message.log_type == "network"}}'
 - name: stage3
   filter: '{{stage1.message.log_type == "process"}}'
```


## Stage

A stage is a parsing step that denotes changes in the event that participate in the same semantic definition. A stage can create, update and delete fields by chaining the execution of actions.

For example, the following snippet shows a stage named `my_stage` that consists in two actions.
```yaml
my_stage:
  actions:
   - set:
       destination.ip: 127.0.0.1
       source.ip: 127.0.0.2
   - delete:
      - event.data
```

### Common stages

Common stages are provided to ease the development of new intakes.
The `external` attribute must be used to reference a common stage along with its optional properties.

```yaml
pipeline:
  - name: parsed_event
    external:
      name: example.external-stage
      properties:
        prop1: val1
        prop2: val2
```


#### JSON

The `json.parse-json` stage can be used to deserialize a json from a string.
Per default, the `message` field is parsed but this property can be overwritten to specify any field.

**Example**

In this example, the parser produces an event with fields that take their value from a deserialized json field. Below is the example of the input event.

```json
{
  "message": "{'protocol':'tcp','traffic':{'source':'127.0.0.1','target':'8.8.8.8'}}"
}
```

Below is the parsing pipeline that deserialize the `message` field and set the `source.ip` and `destination.ip` fields.

```yaml
pipeline:
  - name: parsed_event
    external:
      name: json.parseJSON
  - name: network
stages:
  network:
    actions:
      - set:
          destination.ip: '{{parsed_event.message.traffic.target}}'
          source.ip: '{{parsed_event.message.traffic.source}}'
```

The following shows the produced event.

```json
{
  "message": "{'protocol':'tcp','traffic':{'source':'127.0.0.1','target':'8.8.8.8'}}",
  "source": {
    "ip": "127.0.0.1"
  },
  "destination": {
    "ip": "8.8.8.8"
  }
}
```

#### Key-Value

The `kv.parse-kv` stage can be used to deserialize a key-value string.
Per default, the `message` field of the original event is parsed but this property can be overwritten to specify any field. Besides, the default field separator is any whitespace `\s` and the value separator is `=` however both can be overwritten with the respective properties: `item_sep` and `value_sep`.

**Example**

In this example, the parser produces an event with fields and values parsed from a key-value string. Below is the example of the input event, a classical `postfix` event.

```json
{
  "message": "to=john.doe@example.com, relay=mail.isp.com, delay=xxx, delays=xxx, dsn=2.0.0, status=sent (250 2.0.0 OK)"
}
```

Below is the parsing pipeline that deserialize the `message` field and set the `destination.user.email` field.

```yaml
pipeline:
  - name: parsed_event
    external:
      name: kv.parseKV
      properties:
        item_sep: ',\s'
  - name: email
stages:
  email:
    actions:
      - set:
          destination.user.email: '{{parsed_event.message.to}}'
```

The following shows the produced event.

```json
{
  "message": "to=john.doe@example.com, relay=mail.isp.com, delay=xxx, delays=xxx, dsn=2.0.0, status=sent (250 2.0.0 OK)",
  "destination": {
    "user": {
      "email": "john.doe@example.com"
    }
  }
}
```

#### Grok

The `grok.match` stage can be used to match a field against a Grok pattern.
The grok pattern must be specified by means of the `pattern` property.
Per default, the `message` field is parsed but this property can be overwritten to specify any field.
The result of the parsing replace the parsed content.
Custom patterns can be specified with the `custom_patterns` property.

**Example**

In this example, the parser produces an event with fields and values parsed from a groked string. Below is the example of the input event.

```json
{
  "message": "64.3.89.2 took 300 ms"
}
```

Below is the parsing pipeline that deserializes the `message` field and set the `destination.ip` field.

```yaml
pipeline:
  - name: parsed_event
    external:
      name: grok.match
      properties:
        input_field: original.message
		output_field: message
        pattern: '%{IP:client} took %{NUMBER:duration}'
  - name: set_ip
stages:
  set_ip:
    actions:
      - set:
          destination.ip: '{{parsed_event.message.client}}'
```

The following shows the produced event.

```json
{
  "message": "64.3.89.2 took 300 ms",
  "destination": {
    "ip": "64.3.89.2"
  }
}
```

#### Date

The `date.parse` stage can be used to parse a date field.
This stage accepts, as optional properties, the format to parse the date (by default, the stage try to autodetect the format) and the IANA timezone of the parsed date (by default, "UTC").
Per default, the `@timestamp` field of the original message is parsed but this property can be overwritten to specify any field. The result of the resulting date is inserted in the `message` field of the current stage.

**Example**

In this example, the parser produces an event with a parsed date. Below is the example of the input event.

```json
{
  "date": "May 21, 2021 at 11:04:35"
}
```

Below is the parsing pipeline that deserializes the `date` field and set the `@timestamp` field.

```yaml
pipeline:
  - name: parsed_date
    external:
      name: date.parse
      properties:
        input_field: original.date
		output_field: date
        format: "%B %d, %Y at %H:%M:%S"
        timezone: "America/New_York"
  - name: set-date
stages:
  set_date:
    actions:
      - set:
          @timestamp: '{{parsed_date:date}}'
```

The following shows the produced event.

```json
{
  "@timestamp": "2021-05-21T11:04:35Z",
  "date": "May 21, 2021 at 11:04:35"
}
```

#### DSV

The `dsv.parse-dsv` stage can be used to extract values from a delimiter-separated values string.
This stage accepts the list of columns and, as optional, the delimiter (by default, the delimiter is the comma ',').
Per default, the `message` field of the original message is parsed but this property can be overwritten to specify any field.

**Example**

In this example, the parser produces an event with a delimiter-separated values string. Below is the example of the input event.

```json
{
  "message": "2020/12/04 16:47:48;LOGIN;jenkins;2305"
}
```

Below is the parsing pipeline that deserializes the `message` field and set the `user` field.

```yaml
pipeline:
  - name: parsed_dsv
    external:
      name: dsv.parse-dsv
      properties:
        columnnames:
            - date
            - action
            - username
            - user_id
  - name: set_user_id
stages:
  set_user_id:
    actions:
      - set:
          user.name: '{{parsed_dsv.message.username}}'
          user.id: '{{parsed_dsv.message.user_id}}'
```

The following shows the produced event.

```json
{
  "message": "2020/12/04 16:47:48;LOGIN;jenkins;2305",
  "user": {
    "id": "2305",
    "name": "jenkins"
  }
}
```


## Action

An action is an elementary operations that can create, update and delete fields.
The execution of an action can be conditionned to a filter.

### set

Sets the value of one or more fields in the final version of the event.

The field in the final version of the event can be specified with a dotted path (i.e. `field1`, `field1.sub-field1`, …).

The value can either be a constant (i.e. `'my-constant'`, `42`, …) or a reference to the value of another field in the a stage (i.e. `{{stage1.my-field1.attribute2}}`). If the value cannot be computed or is empty, the field is not modified.

Example:

```yaml
- set:
    source.ip: 127.0.0.1
    destination.ip: {{stage1.target.ip}}
  filter: '{{stage1.log_type == "network"}}'
```

### translate

Sets the value of one or more fields according the value of a source field and a dictionary that connect the values.

The field in the final version of the event can be specified with a dotted path (i.e. `field1`, `field1.sub-field1`, …).

An optional fallback value can be defined.
If the value of the source field doesn't match any entries of the mapping dictionary, this fallback value will be used to set the target field.
If no fallback value is defined and the value of the source field doesn't match any entries, the target field will not be created in the final event.


Example:

```yaml
- translate:
  dictionary:
    200: 'OK'
    201: 'Created'
    204: 'No Content'
    400: 'Bad Request'
    401: 'Unauthorized'
    403: 'Forbidden'
    404: 'Not Found'
    500: 'Internal Server Error'
    501: 'Not Implemented'
    502: 'Bad Gateway'
    503: 'Service Unavailable'
    504: 'Gateway Timeout'
  mapping:
    http.response.status_code: http.response.status_message
    api.status_code: api.status_message
  fallback: 'Request Processed'
  filter: '{{stage1.log_type == "network"}}'
```

#### filters

The reference to another field can be extended with filters. Filters are separated from the field path by a pipe symbol (|). Multiple filters can be chained. The output of one filter is applied to the next.

For example, `{{stage1.username |strip |upper}}` remove the whitespace and return the uppercase value of the `username` variable computed in `stage1`.

The following built-in filters are available:

- `abs`: returns the absolute value of the variable.
- `capitalize`: returns the first character uppercase, all others lowercase.
- `float`: converts the variable in float
- `int`: converts the variable in int
- `length`: returns the number of items
- `lower`: returns the value all lowercase
- `max`: returns the largest item from the variable
- `min`: returns the smallest item from the variable
- `strip`: returns the variable removed from heading and leading whitespaces
- `upper`: returns the value all uppercase


### delete

Deletes fields in the final version of the event.

Example:

```yaml
- delete:
   - source.ip
   - destination.ip
  filter: '{{stage1.log_type != "network"}}'
```


# Events

This section contains data files that are used by the Operation Center to help analysts better understand their events.

## smart-descriptions.json

This file is used to provide analysts with an understandable version of their events. Here is an example, as seen on the Events page:

![image](https://user-images.githubusercontent.com/35897/111750859-0e37b000-8894-11eb-9f47-1947000f4086.png)

And here is the part of the JSON file responsible for this description:

```json
{
  "windows": [
    {
      "value": "{user.domain}\\{user.name} logged on to {log.hostname} with special privileges",
      "relationships": [{
        "source": "user.name",
        "target": "log.hostname",
        "type": "logged on to"
      }],
      "conditions": [{
          "field": "action.id",
          "value": 4672
        },
        {
          "field": "event.provider",
          "value": "Microsoft-Windows-Security-Auditing"
        }
      ]
    },
  ]
}
```

The JSON file contains a list of descriptions associated with an intake name (here: "windows"). Each description has the following properties:

* `value`: the Smart Description itself, with variables from the event expressed as `{ECS_EVENT_PATH}`
* `conditions`: a set of conditions that should be met for this description to be used. Each condition has a `field` name and a `value`. A condition without a `value` means that the field should be set (whatever the value).
* `relationships` (optional): this will be used in the future to display events inside an investigation graph. Each relationship should have a `source` (object path), a `target` (object path) and a `type` (text, description of the relationship).

When several conditions match the same event, the Smart Description with the most conditions is used.

## lookups.json

This file is used to provide a friendly description for some event constants that are usually meant for machines. Here is an example as seen on the Events page:

![image](https://user-images.githubusercontent.com/35897/111752811-6f608300-8896-11eb-843f-b479178b8503.png)

And here is the corresponding part of the JSON file:

```json
{
  "action.properties.LogonType": [{
    "values": {
      "0": "System - Used only by the System account, for example at system startup.",
      "2": "Interactive - A user logged on to this computer.",
      "3": "Network - A user or computer logged on to this computer from the network.",
      "4": "Batch - Batch logon type is used by batch servers, where processes may be executing on behalf of a user without their direct intervention.",
      "5": "Service - A service was started by the Service Control Manager.",
      "7": "Unlock - This workstation was unlocked.",
      "8": "NetworkCleartext - A user logged on to this computer from the network. The user's password was passed to the authentication package in its unhashed form.",
      "9": "NewCredentials - A caller cloned its current token and specified new credentials for outbound connections. The new logon session has the same local identity, but uses different credentials for other network connections.",
      "10": "RemoteInteractive - A user logged on to this computer remotely using Terminal Services or Remote Desktop.",
      "11": "CachedInteractive - A user logged on to this computer with network credentials that were stored locally on the computer. The domain controller was not contacted to verify the credentials.",
      "12": "CachedRemoteInteractive - Same as RemoteInteractive. This is used for internal auditing.",
      "13": "CachedUnlock - Workstation logon."
    },
    "conditions": []
  }],
}
```

The JSON file contains a lookup table associated with each object path (`action.properties.LogonType` in this example). Each lookup table has the following properties:

* `values`: an object with the actual values as keys and the associated descriptions as values
* `conditions`: a set of conditions, similar to the ones used for the Smart Descriptions. When the list is empty, it means that the lookup table always applies for this field.

## Testing Changes

When making changes to these files, you can test your changes directly from your browser by using special cookies values:

* `event-smart-descriptions`: set this cookie to an URL hosting your modified `smart-descriptions.json` file
* `event-lookups`: set this cookie to an URL hosting your modified `lookups.json` file

Do not forget to remove these cookies once you are done, or make sure to limit their lifetime to the session.

### Testing changes locally

In order to test changes from local copies of the file, you can use a simple webserver such as `http-server --cors -p 8000`. `http-server` can be installed with `npm install http-server`.

When using this local server, you should then set (depending on which file you are modifying):

* `event-smart-descriptions` to `http://localhost:8000/smart-descriptions.json`
* `event-lookups` to `http://localhost:8000/lookups.json`

### Testing changes from a GitHub fork

You can also test your changes by creating a GitHub fork and use the raw URL inside the cookies:

* `event-smart-descriptions` to `https://raw.githubusercontent.com/SEKOIA-IO/intakes/main/module?/intake/events/smart-descriptions.json`
* `event-lookups` to `https://raw.githubusercontent.com/SEKOIA-IO/intakes/main/module?/intake/events/lookups.json`

Replace `SEKOIA-IO/intakes` with the path to your GitHub fork.
Replace `module?/intake` with the module name if it exist and the intake name.


# Manifest

## General

manifest.yml define the intake.

## Pattern

```
uuid: uuid v4
name: Intake name
slug: Slug (**Convention**: space in the name converted to '_', the '-' remains, all in lower case.)

description: >-
  Quick description.

data_sources:
	Pick data sources from the next section.

```

### Data sources

* Access tokens
* Anti- virus
* API monitoring
* Application logs
* Asset management
* Authentication logs
* AWS CloudTrail logs
* Azure activity logs
* Binary file metadata
* BIOS
* Browser extensions
* Component firmware
* Data loss prevention
* Detonation chamber
* Digital certificate logs
* Disk forensics
* DLL monitoring
* DNS records
* Domain registration
* EFI
* Email gateway
* Environment variable
* File monitoring
* GCP audit logs
* Host network interface
* Kernel drivers
* Loaded DLLs
* Mail server
* Malware reverse engineering
* MBR
* Named Pipes
* Netflow/Enclave netflow
* Network device command history
* Network device configuration
* Network device logs
* Network device run- time memory
* Network intrusion detection system
* Network protocol analysis
* OAuth audit logs
* Office 365 account logs
* Office 365 audit logs
* Office 365 trace logs
* Packet capture
* PowerShell logs
* Process command- line parameters
* Process monitoring
* Process use of network
* Sensor health and status
* Services
* Social media monitoring
* SSL/TLS certificates
* SSL/TLS inspection
* Stackdriver logs
* System calls
* Third- party application logs
* User interface
* VBR
* Web application firewall logs
* Web logs
* Web proxy
* Windows Error Reporting
* Windows event logs
* Windows Registry
* WMI Objects

## Send events to SEKOIA.IO

### Usage

```console
Usage: send_events.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.
  --help                Show this message and exit.

Commands:
  from-cli
  from-intake-formats
  from-text-file
```

### Example

### From intake-formats input files

Each test file `["input"]["message"]` will be sent as an event.

```console
poetry run python send_events.py from-intake-formats "<intake-key>" ./../module/format/
```

### From text file

Each line will be sent as an event

```console
poetry run python3 send_events.py from-text-file "<intake-key>" ../Downloads/example.txt --url https://app.eur1.sekoia.io/api/v1/intake-http/batch 
```

### From the terminal

Send one line from the terminal

```console
poetry run python send_events.py from-cli "<intake-key>" "<event>"
```

## Publish intake-format to SEKOIA.IO

### Usage

```console
usage: poetry run publish_format.py [-h] path apikey url
publish_format.py: error: the following arguments are required: path, apikey url
```

### Example

### Publish
```
poetry run python publish_format.py ./../module/format/ '<API KEY>' '<URL>'
```
