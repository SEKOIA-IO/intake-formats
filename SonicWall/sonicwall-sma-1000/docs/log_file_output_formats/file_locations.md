File Locations

the Log file names for SMA services table lists the names of the log files on the appliance, which are initially stored locally (/var/log/aventail/).
Log file names for SMA services Secure Mobile Access service 	File format 	File name

System messages

This log contains message records for the Web proxy service, the network tunnel service, and the policy server. It also includes messages from unregistered devices.

See System Message Log
	syslog 	access_servers.log
Management message log

This log contains message records of AMC operations, noting when the console was started and stopped and any errors encountered during its operation.

See Management Message Log
	syslog 	management.log

Management audit log

This log contains message records of the history of configuration changes performed by administrators in AMC, specifying when each change occurred and which administrator executed it.

See Management Audit Log
	syslog 	

policy_audit.log

management.log
Management access log

This log contains entries regarding all actions performed by the user, including logins, data access, configuration changes, and other system-related activities.

See Management Access Log
	syslog 	management_access.log

Network tunnel audit log

This log contains information regarding connection activity, a list of users accessing the network, and the volume of data transferred for the network tunnel service.

See Network Tunnel Audit Log
		extranet_access.log

Web proxy audit log

This log provides information about connection activity for users accessing resources via Web Proxy Access or Translated Access, including a list of users and the volume of data transferred.

See Web Proxy Audit Log
	W3C CLF 	extraweb_access.log

Client installation

See Client Installation Logs (Windows)
	syslog 	<username>@<realm>.log

WorkPlace

See WorkPlace Logs
	syslog 	

workplace.log

wp_init.log

Upgrade log

This log is a record of any upgrades you have made to the appliance.
	text 	upgrade.log

Migration log

Stored in /var/log/, these are the logging messages recorded during migration from version <n.n.n>.
	syslog 	migrate_<n.n.n>.log

To minimize storage requirements for log files, the appliance rotates the files. The log rotation procedures vary, depending on the frequency you specify:
Log rotation procedures Frequency 	Procedure
Every 15 minutes 	

    Rotate any log files that are larger than 750MB.

    Force a rotation of the syslog log file.

    Turn on Compression for rotated files.

    Compression Ratio is set to 0.10 of actual file size.

    Each file is compressed after rotation.

Every day 	

    Force a rotation of all log files.

    Delete any log files that are older than seven days.

Log files of more than one day old are stored in uncompressed format. The log file names contain a suffix that is numbered sequentially from 1 through 7, so that if the log rotation occurs daily, a log file with the suffix 7 is one week old. For example:

    extraweb_access.log is the current log file for Web proxy service.

    extraweb_access.log1 through extraweb_access.log7 are the logs from the previous rotations.
