# DIDComm Delivery

`POST /v1/issuance/didcomm/deliver` is the authenticated, tenant-scoped
transport for pushing a credential produced by an existing issuance
transaction to a holder DID.

The public request is exactly `organization_id`, `transaction_id`, and
`holder_did`. The implementation resolves the transaction inside the
authenticated organization, signs the credential through the transaction's
resolved issuer DID and active issuer profile, and resolves the holder DID
through deployment-managed resolver configuration. Callers cannot select an
issuer profile, signing service, key, KMS, resolver provider, or resolver URL.

Delivery is encrypted DIDComm v2. The resolved DID Document must contain a
compatible key-agreement method and an HTTPS `DIDCommMessaging` service
endpoint. Encryption or endpoint validation failure is a failed request; an
implementation must not downgrade credential delivery to plaintext.

Inbound acknowledgements and problem reports are not part of the current
public contract. They may be introduced only when the receiving DID is
resolved to an authorized active issuer profile and decryption/authentication
is performed through that profile's managed custody service. An implementation
must not accept an encrypted message without processing it or let an
unauthenticated plaintext message mutate issuance state.
