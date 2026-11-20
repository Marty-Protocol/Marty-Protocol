# Canvas MIP Open Badge Flow

This example illustrates how an independent Canvas connector and MIP could
compose an Open Badge workflow. The Canvas Credentials destination is a
protocol example. Marty does not offer this Canvas mirror as a runtime delivery
option.

```text
Canvas LTI/AGS launch
  -> standalone Canvas connector
  -> public Common Gateway evidence submission
  -> unverified observation and separate verification and approval
  -> canonical ElevenID credential issuance
  -> status-list backed revocation and employer verification
```

The [standalone connector](https://github.com/ElevenID/canvas-integration)
owns Canvas traffic and credentials. Its only integration with Marty is the
public Common Gateway. Marty owns evidence admission, approval policy, issuer
identity and credential status. Submission alone does not verify evidence or
authorize issuance.

The adjacent delivery destination fixture illustrates a disabled Canvas mirror
profile. Any future connector-owned mirror needs its own implementation and
qualification.
