Unregistered Device Log Messages

Unregistered device log messages provide device IDs from login attempts by users on devices that are not registered. The AMC provides a way to export the unregistered device log messages in XML format. On the Logging page, select Unregistered device log from the Log file drop-down list and then click Export. You can reduce the size of the exported file by first applying filter or search criteria.

You can also access and export the list of unregistered devices to an XML format on another system. The list can be accessed directly in a Web browser using the following URL:

https://(internal IP address)/UnregisteredDevices.xml

This URL requires BASIC HTTP authentication, and the credentials must be an AMC user with at least View access to the Monitoring category.

A curl or wget command can be used to obtain the list programmatically from the external machine:
Command 	Syntax
curl 	curl -k3u (user):(password) https://(internal IP):8443/UnregisteredDevices.xml
wget 	wget --no-check-certificate --http-user=(user) --http-password=(password) https://(internal IP address):8443/UnregisteredDevices.xml

Both of these commands turn off SSL certificate checking, which is useful when using a self-signed certificate.

A full definition of the URL used to fetch the XML version of the unregistered device report is provided in:
URL 	https://<internal address>:8443/UnregisteredDevices.xml?parameter=value&parameter=value
Authentication 	BASIC HTTP authentication, credentials must be AMC user with at least view access to the Monitoring category.

Parameters (all optional)

username
	

string, case insensitive, default * (all users)

Search for login attempts from users that contain this value as part of their username. Example: username=li will return entries for Linda and Melinda
realm 	

string, case insensitive, default * (all realms)

Search for login attempts to Realms that contain this value as part of the Realm name. Example: realm=Corp will return entries for Corporate and Non-Corporate
platform 	

string, enumerated values below

Search for login attempt from devices running only the specified platform:

all - all platforms (default)

windows - only Windows devices

mac - only Mac devices

linux - only Linux devices

ios - only iOS devices

android - only Android devices

activeSyncMobile - only Exchange ActiveSync devices

mobilePhone - only Mobile Phone devices

unknown - only devices on which the platform could not be

determined
exported 	

string, enumerated values below

Search for entries that have or have not already been exported either in AMC

or via an HTTP get command.

all - all entries, whether or not they have been exported (default)

exported - only entries that have already been exported

unexported - only entries that have not already been exported
limit 	

number, default 1000

Limit the search to this many entries.
deviceCount 	

number, 0-3, default all entries

Search for users with only the specified number of devices already registered in the external AD/LDAP store.

0- user has no devices registered

1- user has one device registered

2- user has two devices registered

3- user has three or more devices registered
lastLoginTime 	

string, enumerated values below, default all

Search for user login attempts that happened only in the time period specified, relative to the current time.

all- all login attempts

hour- attempts in the last hour

day- attempts in the last day (24 hour period)

week- attempts in the last week (7 days)