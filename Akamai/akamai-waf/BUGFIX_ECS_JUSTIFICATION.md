# ECS Justification for Akamai WAF Mapping Decision

- We validated and implemented the following mapping:
  - raw field `httpMessage.requestHeaders.Content-Length` is mapped to ECS field `http.request.body.bytes`, which matches the ECS definition "Size in bytes of the request body"
- Nevertheless the following mapping request was refused:
  - mapping raw field `httpMessage.requestHeaders.Content-Type` to ECS field `http.request.mime_type` is not ECS-compliant because ECS states this field "must only be populated based on the content of the request body, not on the Content-Type header"
  - raw-event limitation: the Akamai/akamai-waf test fixtures only expose declared headers (`Content-Type`, `Content-Length`) in request headers and do not expose request body content
  - so we implemented this workaround: the declared header value is preserved in custom field `akamai.http.request.headers.content_type`
  - consequently, the ECS field `http.request.mime_type` mapping was removed from the parser because ECS requires body-content-based MIME detection and this data source does not provide request body content
