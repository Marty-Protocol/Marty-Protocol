# Deployment Profile — Design Notes

**Version:** 0.1.0

---

## Key Design Decisions

### Deployments Are Declarative

Physical devices do not contain business rules. A gate scanner receives a Deployment Profile ID on initialization and fetches its policy configuration from the server. This means updating what a 500-gate terminal checks requires one policy update, not 500 device pushes.

### Lanes Are Within Profiles, Not Separate Resources

Lanes are embedded in Deployment Profiles rather than independent top-level resources. This avoids orphaned lanes (lanes referencing deleted profiles) and keeps the deployment model self-contained. Lane mutations use `/v1/identity/deployment-profiles/{id}/lanes`.

### Why offline_cache_ttl Is on EnvironmentConfig, Not Network Mode

Different deployments with the same network mode may have different caching needs (a train checkpoint wants 2h cache; an airport gate wants 1h). The cache TTL is per-deployment, not per-mode.

### Update Channels

The `update_channel` field allows operational teams to pin specific deployments to known-good versions during high-stakes events (major holidays, large events) while allowing other deployments to receive automatic updates. `pinned` channel deployments require an explicit version bump to update.

### Multi-Policy Profiles

A single Deployment Profile can reference multiple Presentation Policies (e.g., pre-boarding check vs. boarding check). Devices use `default_policy_id` for most interactions, and applications switch policies based on workflow step. This avoids duplicating trust configuration across near-identical deployments.
