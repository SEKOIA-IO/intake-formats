Management Audit Log

An individual with administrative privileges can review the AMC audit log to view the history of configuration changes made to the appliance. This log provides a comprehensive audit history of configuration changes made in AMC by administrators.

Management audit logs are stored on disk in the file /var/log/aventail/consoleaudit.log and contain these parameters:

[level] [date] [time] [username] [message]

This example illustrates a management audit log file entry:

Info 6/3/2025 00:31:02 admin Applied configuration changes

Management Console Audit log fields
Field 	Description

Level (Severity)
	

The message severity levels are:

    Error—A problem caused the server to shut down or fail to communicate with another component. A name resolution problem at startup is logged at this level.

    Warning—Something unexpected occurred that does not adversely affect the operation of the server. For example, a single failed attempt to access a RADIUS server is logged at the Info level, but if all attempts fail, an entry is added to the log file at the Warning level.

    Info—A normal event that you might want to track; for example, a specific user has logged in, or has matched a given access control rule.

    Verbose—Like an Info message, this level identifies normal operations, but includes the steps in a process. For example, when processing access control rules a message for each non-match is at the Verbose level, while a matched rule is identified as Info.

Date/Time 	

The date and time at which the request was received by the appliance.

Example: 6/3/25 00:31:02
User name 	

If the user has logged in, this field displays the user’s name.

If a user has not yet authenticated or is accessing content that does not require authentication (such as the WorkPlace login page), this field contains a dash (-).

Example: admin
Message 	

Describers the configuration changes that were made to the appliance.

Example:Applied configuration changes