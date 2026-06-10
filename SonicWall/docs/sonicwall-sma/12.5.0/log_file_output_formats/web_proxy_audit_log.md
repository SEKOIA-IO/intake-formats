Web Proxy Audit Log

The Web proxy audit log provides detailed information about connection activity, including a list of users accessing your network and the amount of data transferred.

Web proxy audit logs are stored on disk in the file /var/log/aventail/extraweb_access.log and contain these parameters:

[Status] [date/time] [source ip] [bytes-sent] [username@realm] [identity] [request] [HTTP-return-code]

The audit log file messages are stored in the World Wide Web Consortium (W3C) Common Log Format (CLF). See http://httpd.apache.org/docs/logs.html for more information on CLF logs.

This example illustrates a web proxy service audit log file entry:

200 6/3/25 00:32:24 10.5.105.245 3 - GET /__api__/logon/1f712dd30772c1cc712bc720fb48624b/endpoints HTTP/1
Web Proxy audit log fields Field 	Description
Status 	

Displays color-coded return codes for each HTTP request. Move the pointer over an HTTP return code number to see explanatory text. The code numbers are in the following ranges and colors:

    500: server error (red)
    400: client error (orange)
    300: redirection (green)
    200: success (green)

Date/Time 	

The date and time at which the request was received by the appliance.

Example: [16/Apr/2017:21:36:37 +0000]
Source IP 	

IP address of the computer accessing the Web proxy service (this field may contain a translated address if NAT is in use).

Example: 192.168.200.162
Bytes-sent 	Number of bytes sent in the body of the response (this does not include the size of the HTTP headers).
User name @ realm 	

User accessing the resource, and the realm he or she is logged in to. The format of this field varies, depending on the authentication method used.

Example: (u3)@(local)
Identity 	This field is not used by the Web proxy service; it always contain a dash (-).
Request 	

First line of the HTTP request, containing the HTTP command (such as GET or POST), the requested resource, and the HTTP version number.

Example: "GET /alias1/foo.gif HTTP/2.0"
HTTP-return-code 	

The server responds with one of the following return codes:

    2xx codes indicate a successful request.

    3xx codes indicate some form of redirection or cached response.

    4xx codes indicate an error (such as a resource that is not found or an unauthorized request).

    5xx codes indicate a server error.

Examples

    If an authentication attempt fails—for example, because the user enters an invalid username or password—a single message appears in the log with a return code of 200 (OK), indicating the client request was understood). Notice that the source IP address in the message is the only way for you to identify who made the request:

    192.168.2.69 - - [6/3/2025 00:32:36.115 +0000] "POST /__extraweb__authen HTTP/2.0" 200 3610 352711-01-521146-5

    For a successful authentication, a similar message appears, but with a return code of 302 (Found). It is immediately followed by another message that contains the user's authentication credentials and a return code of 200:

    192.168.2.69 - - [6/3/2025 00:32:36.115 +0000] "POST /__extraweb__authen HTTP/2.0" 302 206 352711-01-521146-5

    192.168.2.69 - (jsmith)@(AD) [6/3/2025 00:32:36.115 +0000] "GET /workplace/access/home HTTP/1.1" 200 15424

    If a user successfully authenticates, but is denied access to a Web resource by an access rule, a message containing a return code of 403 (Forbidden) is logged:

    192.168.2.69 - (jsmith)@(AD) [6/3/2025 00:32:36.115 +0000] "GET /dukes HTTP/2.0" 403 3358 352711-01-521146-5

    If a user successfully authenticates and is permitted to access a URL, a message appears that is identical to the one for a failed authentication (a return code of 200), except that this one includes the user’s credentials:

    192.168.2.69 - (jdoe)@(AD) [6/3/2025 00:32:36.115 +0000] "GET /dukes HTTP/2.0" 200 262 352711-01-521146-5
