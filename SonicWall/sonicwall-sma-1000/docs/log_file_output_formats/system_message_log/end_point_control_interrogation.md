End Point Control Interrogation

The system message log captures information during client EPC interrogation when the log level is set to verbose. The appliance checks for the presence of certain device profile attributes on the client, and the log file records the query and the results.

In the following example, EPC is checking for a certain antimalware application (Symantec Client Security, version 9.x or later). When the application is not found, this particular device is relegated to the Default zone:

[6/3/2025 00:32:36.115 +0000] E-Class SMASSLVPN 027186 uk 00000001 Verbose System ::API::QAABA145dFYNZimCKNWHB7p2q2Y=::(timwillis)@(Students)::CLIENT:: Interrogation: Evaluation of OPSWATAV AV1128462569762A [NortonAV.dll,Symantec Corp.,Symantec Client Security,>=,9.x,,,,,FALSE] results: FALSE

6/3/2025 00:32:36.118 +0000] E-Class SMASSLVPN 027186 uk 00000001 Verbose System ::API::QAABA145dFYNZimCKNWHB7p2q2Y=::(timwillis)@(Students):: Classified into zone: Default zone 