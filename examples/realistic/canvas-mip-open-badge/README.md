# Canvas MIP Open Badge Flow

This example shows the intended production alignment between Canvas and MIP:

```text
Canvas LTI/AGS launch
  -> EvidenceFact
  -> Cedar approval PolicySet
  -> canonical ElevenID credential issuance
  -> status-list backed revocation
  -> Canvas Credentials delivery destination
  -> employer verification against the canonical issuer DID
```

Canvas is the learning system and evidence provider. MIP remains the source of
facts, approval policy, issuer identity, credential status, delivery
projection, and verification trust.

