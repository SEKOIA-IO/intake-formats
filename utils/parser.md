# EventParser

Parses the event according to the intakes configuration.

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

