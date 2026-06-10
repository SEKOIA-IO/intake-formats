Management Access Log

The management access log provides detailed information about authenticated usernames, the date and time of each action, and the network location from which the action was performed. Logged activities include logins, data access, configuration changes, and other system-related tasks.

Management access logs are stored on disk in the file /var/log/aventail/management_access.log and contain these parameters:

[SOURCE] [USERNAME] [DATETIME TIMEZONE] [HTTP REQUEST LINE] [STATUS] [BYTESOUT]

This example illustrates a management access log file entry:

127.0.0.1 - admin [25/Jul/2025:05:30:52 -0700] "GET /Console/PendingChanges HTTP/1.1" 200 308

Management Access log fields
Field 	Description
Source-IP 	

IP address of the computer accessing the Web proxy service (this field may contain a translated address if NAT is in use).

Example: 127.0.0.1
User name 	

If the user has logged in, this field displays the user’s name.

If a user has not yet authenticated or is accessing content that does not require authentication (such as the WorkPlace login page), this field contains a dash (-).

Example: admin
Date/Time 	

The date and time at which the request was received by the appliance.

Example: [25/Jul/2025:05:30:52 -0700]
Request 	

First line of the HTTP request, containing the HTTP command (such as GET or POST), the requested resource, and the HTTP version number.

Example: "GET /Console/PendingChanges HTTP/1.1"
Status 	

Displays color-coded return codes for each HTTP request. Move the pointer over an HTTP return code number to see explanatory text. The code numbers are in the following ranges and colors:

    500: server error (red)
    400: client error (orange)
    300: redirection (green)
    200: success (green)

HTTP-return-code 	

The server responds with one of the following return codes:

    2xx codes indicate a successful request.

    3xx codes indicate some form of redirection or cached response.

    4xx codes indicate an error (such as a resource that is not found or an unauthorized request).

    5xx codes indicate a server error.

For more information on these codes, see http://www.ietf.org/rfc/rfc2616.txt.
Bytes 	Number of bytes sent in the body of the response (this does not include the size of the HTTP headers).