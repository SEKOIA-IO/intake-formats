Viewing Client Certificate Errors in the Log

If the appliance is unable to verify a certificate chain, a message such as this one appears in the system message log file:

[02/Jul/2025:18:47:29.113075 +0000] SMAnode 013581 ps 00000000 Info System Auth: CRL-CERT: Cert verification status = 0, err = 19, reason = 'self-signed certificate in certificate chain', subject='/C=US/ST=Washington/L=Seattle/O=SonicWall/OU=Engineering/CN=Untrusted CA'

This message includes an error code (in this case, 20) reporting why the certificate check failed. These error codes are described in the Client certificate error codes table.
Client certificate error codes Code 	Error message 	Description
2 	Unable to get issuer certificate 	The issuer certificate of an untrusted certificate could not be found.
7 	Certificate signature failure 	The signature of the certificate is invalid.
9 	Certificate is not yet valid 	The certificate is not yet valid.
10 	Certificate has expired 	The certificate has expired.
18 	Self-signed certificate 	The passed certificate is self-signed and cannot be found in the list of trusted certificates.
19 	Self-signed certificate in certificate chain 	The certificate chain can be built using the untrusted certificates, but the root cannot be found locally.
20 	Unable to get local issuer certificate 	This normally means the list of trusted certificates is not complete. This error can also occur when an intermediate certificate is used for authentication (a root certificate is required).
21 	Unable to verify the first certificate 	No signatures could be verified because the chain contains only one certificate and is not self-signed.
22 	Certificate chain too long 	The certificate chain length is greater than the supplied maximum depth.
23 	Certificate revoked 	The certificate has been revoked.
24 	Invalid CA certificate 	A CA certificate is invalid. Either it is not a CA or its extensions are not consistent with the supplied purpose.