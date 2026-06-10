WorkPlace Shortcut Examples

When a user logs in to Workplace and successfully sees shortcuts, the log file entries looks like this:

    The username credentials are logged with a session ID (when troubleshooting, just look for the username):

    2025-06-30T14:17:23+05:30 WP@ma34.sma local7.debug WP: 2025-06-30 14:17:24 +0530 DEBUG - GOT: CredentialsManager[teamSessionId=/bV+kF/p7QuQWL3BGdokQA==,teamcredentials={username=udbhav} ,credentials={}]

    Later you see a message indicating a successful load of the shortcut (in this case a Web shortcut):

    2025-06-30T14:17:23+05:30 WP@ma34.sma local7.debug WP: 2025-06-30 14:17:23 +0530 DEBUG - PolicyClientSession: <authorize:exit> uri=http://127.0.0.1:8085/ctdownload/ status=PCL_STATUS_SUCCESa

    The successful load of a network shortcut looks like this:

    2025-06-30T14:17:23+05:30 127.0.0.1/127.0.0.1 local7.debug DEBUG [22:03:03,617] pcsession: <authorize:exit> uri=smb://marshare01/marketing status=SUCCESS

If a user does not see shortcuts (because of an access rule you have set up, for example), the denial of access looks like this:

    Look for the username at login:

    2025-06-30T14:17:23+05:30 127.0.0.1/127.0.0.1 local7.debug DEBUG [22:12:15,027] GOT: CredentialsManager[teamSessionId=hZ98BEZxdyARJCtjkGl3lA==,teamcredentials= {username=dsmith} ,credentials={}]

    Look for the shortcut information that is failing to load on the user's WorkPlace portal page. This is an example of a Web shortcut failure:

    2025-06-30T14:17:23+05:30 127.0.0.1/127.0.0.1 local7.debug DEBUG [22:12:15,043] pcsession: <authorize:exit> uri=http://wemmet.internal.net status=FAILURE

    Access (permit/deny) to a resource share is also logged in extaweb_access.log:

    192.168.2.69 - (jdoe)@(AD) [2025-06-30T14:17:23+05:30 +0000] "GET /workplace/access/exec/file/view?path=smb://marshare01/marketing/ reports.doc/ HTTP/1.1" 200 4608

    An additional WorkPlace-related log file in syslog format (/var/log/aventail/wp_init.log) is also available.
