# Advanced Examples

This directory will contain advanced MIP use-case examples, including:

- **Zero-knowledge predicates** — age verification and threshold proofs using ZK circuits without revealing raw values
- **Offline presentation** — BLE/NFC proximity presentation flows with no network connectivity
- **Multi-lane deployments** — single credential template serving ONLINE, OFFLINE, and KIOSK lanes simultaneously
- **Cascading revocation** — parent credential revocation propagating to dependent child credentials
- **Cross-jurisdictional interoperability** — a single presentation policy accepting credentials from multiple compliance profiles (AAMVA mDL + EUDI PID)

These examples are planned for the 0.2.0 milestone. See [CHANGELOG.md](../../CHANGELOG.md) for status.

For working examples today, see [`examples/realistic/`](../realistic/) and [`examples/minimal/`](../minimal/).
