Access Policy Decisions

One of the main uses for the system message log is to audit access policy decisions. Each time a user request matches a policy rule, the appliance writes an entry to the message text field (the last field in the message log) explaining the action taken.

A sample message for an access policy decision looks like this:

[6/3/2025 00:32:36.115] E-Class SMASSLVPN 002421 ps 100004b3 Info EWACL User ' (192.168.136.70 (Dominique Daba)@(Students)' connecting from '192.168.136.70:37975' matched rule 'accessRule(AV1091719670706:preauth access rule)', access to '127.0.0.1:455' is permitted.

For each connection request that matches a rule, a log message is generated at the Info level.

Verbose level: Verbose CSACL User '(user1)@(RealmLocal)' connecting from '172.16.86.81:0' matched rule #4 'Rule-user1-to-host12-tcp', access to '172.16.86.12:23' is permitted.

Requests that don’t match a rule are logged at the Verbose level.

Debug1 level: Debug 1 CSACL avtNetwork accessRule(AV1753771393289AEA:Rule-user1-to-Tunnel): FAILED destination address check, Testing: 172.16.86.12:23.

When no rule match is found the request is logged at the Warning level.

Verbose level: Verbose CSACL User '(user1)@(RealmLocal)' connecting from '172.16.86.81:0' found no matching access rule, access to '172.16.86.12:8' is denied.

For policy decisions, the logging message text field (everything after Info in the previous example) includes the information shown in the Logging message text fields table.
Logging message text fields Field 	Description

Log type
	

The access policy being evaluated. The log types are:

    CSACL—client/server access policy

    EWACL—Web access policy

    WPACL—WorkPlace access policy

    NEACL—file system access policy (file shares accessed from the Network

    Explorer page in WorkPlace)

User name 	

The user making the request. If the appliance is configured to use multiple realms, the username will appear in the format (user)@(realm).

Example: User '(192.168.136.70 (Dominique Daba)@(Students)'
Source of request 	

The address of the user making the request.

Example: Connecting from 192.168.136.70:37975
Match status 	

Rule match status (either Matched or No Match) and the ID for the rule.

Example: matched rule accessRule(AV1091719670706:preauth access rule
Rule outcome 	

Details

If the rule matched, this field will be empty. If the rule did not match, one of the following messages will appear:

    Source Network is <network>

    Date/time specification <time>

    User <username> not in User/Group List

    Destination network is <dest>

    Virtual Host is <vhost>

    Destination services dest is <dest>

    Command is <command>

    UDPEncrypt is <true or false>

    Key Length <length from the policy rule> requires a stronger cipher

Example: access to '127.0.0.1:455' is permitted

If no rule matched, an Info-level message is generated indicating that no matching rule was found.

Examples

Example 1: Success at Info Level

[02/Jul/2025:18:43:11.568282 +0000] SMAnode 002764 ps 00000000 Info Session Session Start: '(user1)@(RealmLocal)', authenticated.

Example 2: Failure at Info Level

[02/Jul/2025:18:42:02.823435 +0000] SMAnode 002764 ps 00000000 Info Session Authentication for user '(user1)@(RealmLocal)' FAILED in method AuthLocal, Auth::FAIL. 