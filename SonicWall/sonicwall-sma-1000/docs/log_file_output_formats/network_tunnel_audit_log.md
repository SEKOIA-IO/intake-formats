Network Tunnel Audit Log

The network tunnel audit log provides detailed information about connection activity, including the status of completed tunnel connections and flows completed within the tunnels.

Network tunnel audit logs are stored on disk in the file /var/log/aventail/extranet_access.log and contain these parameters:

Tunnel Audit:

[source ip] [username @ realm] [date/time] [tunnel protocol version] [“tunnel”] [client vip4, client vip6] [error code] [bytes received] [bytes sent] [duration] [platform prefix] [equipment id]

Example:

::ffff:10.5.105.197]:59234 - "(demo2)@(CT)" "31/Jul/2025:14:41:23.073 +0530" 1.2 tunnel 172.24.35.34 -1 112639 137450 165 W"42 1a 69 3a 6c 75 ac eb-be 8a 0b 90 9b 13 c6 24"

Flow Audit:

[source ip] [username @ realm] [date/time] [tunnel protocol version] [“flow:”protocol] [destination ip] [error code] [bytes received] [bytes sent] [duration] [platform prefix] [equipment id]

Example:

172.24.35.34:5353 - "(demo2)@(CT)" "31/Jul/2025:14:40:33.441 +0530" 1.2 flow:udp 224.0.0.251:5353 -1 540 0 0 W"42 1a 69 3a 6c 75 ac eb-be 8a 0b 90 9b 13 c6 24"

172.24.35.34:59260 - "(demo2)@(CT)" "31/Jul/2025:14:40:47.815 +0530" 1.2 flow:tcp 10.5.252.168:443 0 5436 129963 125 W"42 1a 69 3a 6c 75 ac eb-be 8a 0b 90 9b 13 c6 24"

ICMP: [2001:df5:4c00:7172:1::200]:129 - "(demo)@(CT)" "31/Jul/2025:22:01:11.597 +0530" 1.2 flow:icmpv6 [2001:df5:4c00:7252::1168]:128 0 320 320 33 W"42 2a 7b 36 80 ca 38 d0-9f 59 81 69 40 7a b6 8a"
Network tunnel audit log fields Field 	Description
Source IP 	

For tunnel records this field contains the source address of the outer tunnel connection. For flows this field contains the inner flow source address, which is the virtual IP address assigned from a tunnel pool when the tunnel is established.

Example:172.24.35.21:5353
User name @ realm 	

User accessing the resource, and the realm he or she is logged in to. The format of this field varies, depending on the authentication method used.

Example: (u1)@(Tunnel)
Date/Time 	

Date (in date/month/year format) and time (hours, minutes, seconds, and milliseconds in 24-hour-clock format and hours of time zone +/- GMT) the connection began.

Records containing date/time may not be written immediately to the log.

Example: " 6/3/2025 00:32:41"
Tunnel Protocol version 	

Tunneling protocol version

Example: 1.2
Type service 	

These commands can appear in log file entries for the network tunnel service:

Tunnel

Flow : The flow protocol field identifies a record as a flow and specifies the flow type. Supported values include TCP, UDP, ICMP, ICMPV6, and UNKNOWN.
Client (IPv4/ IPv6) 	The client may contain either or both values, depending on how the appliance is configured, of the tunnel VIPs assigned to a specific tunnel instance.

Destination IP
	

IP address and port number of the resource being accessed. For flows, this is the destination of the TCP, UDP or ICMP flow. For tunnels, this is the external address of the appliance (port number is always 0).

Example: 192.168.136.254:22
Status 	

Successor Error
Bytes-received 	Number of bytes read from source.
Bytes-sent 	Number of bytes written to destination.
Connection duration 	Connection duration (in seconds) based on the time the tunnel was closed, a TCP flow entered its TIME_WAIT state, or a UDP or ICMP flow timed out.
Platform prefix 	

Indicates the client platform.

Example: W = Windows, L = Linux
Equipment ID 	Displays a unique identifier for equipment, which is useful when a user connects using multiple devices.