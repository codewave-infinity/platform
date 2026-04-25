# SecureShare — Shared API Contracts

> **This is the single source of truth.** If you need to deviate, open a PR
> against this document AND the corresponding artifact under `contracts/`.
> Anyone caught hardcoding a different schema in their service owes the team
> coffee.

These contracts let the four teams work in parallel without blocking each
other. Lock them in hour 0–4.

## Authentication model

Two distinct token types; do not conflate them.

| Token | Issued by | Used by | How obtained |
|---|---|---|---|
| `sessionToken` | `/auth/zk-verify` | A human at a participating org submitting threat reports via the dashboard | Zero-knowledge proof of group membership |
| `gatewayToken` | Out-of-band provisioning | A deployed firewall gateway pulling rules and pushing telemetry | Pre-distributed at registration time (v1) |
| `clientId` | `/fl/register-client` | A federated-learning client (one per gateway) | Public-key registration |

`anonymousId` is derived from the ZK nullifier and is **stable across sessions**
for the same identity but reveals nothing about the underlying organization.

---

## Platform REST API (FastAPI backend)

Base URL: `/api/v1`

### Auth

```
POST   /auth/zk-verify
       Body:    { proof, publicSignals, nullifierHash }
       Returns: { sessionToken, anonymousId, credibilityScore }
```

### Threat reporting

```
POST   /threats/report                 [requires sessionToken]
       Body:    { type, indicators[], severity, description, mitre_tactic? }
       Returns: { reportId, sigmaRuleId, anonymousReporter }

GET    /threats/feed                   [requires sessionToken]
       Query:   ?since=<ISO-8601>&type=<ThreatType>&limit=<int>
       Returns: { reports[], pagination: { cursor, hasMore } }
```

### Sigma rule distribution (gateway-facing)

```
GET    /sigma/rules                    [requires gatewayToken]
       Query:   ?since=<ISO-8601>
       Returns: { rules: [{ id, yaml, sourceCredibility, expiresAt }] }

POST   /telemetry/confirm              [requires gatewayToken]
       Body:    { ruleIds[], hitCounts[], aggregatedAt }
       Returns: { accepted, credibilityDelta }
```

### GNN cluster expansion

```
POST   /gnn/cluster
       Body:    { seedIndicator: { type, value } }
       Returns: { cluster: [{ indicator, score, relationship }] }
```

`relationship` is one of: `resolves_to`, `issued_by`, `shares_cert_with`,
`registered_via`, `same_asn`, `embedding_neighbor`.

### Federated learning

```
POST   /fl/register-client
       Body:    { gatewayPublicKey, capabilities[] }
       Returns: { clientId, aggregatorEndpoint, currentRound }

GET    /fl/global-model
       Returns: binary stream of model weights
       Headers: X-Model-Version, X-Trained-At

POST   /fl/submit-update               [requires clientId]
       Body:    multipart { roundId, sampleCount, weightUpdate (binary) }
       Returns: { accepted, nextRoundAt }
```

---

## Gateway internal API (dashboard + debugging)

Served by the gateway itself on `localhost:8080` — not exposed to the network.

```
GET    /gateway/status
       Returns: { layersActive, ruleCount, modelVersion, blocksToday }

GET    /gateway/blocks/recent
       Query:   ?limit=50
       Returns: { events: [{ timestamp, layer, indicator, reason }] }

POST   /gateway/whitelist
       Body:    { domain, reason }
```

---

## Standard data shapes

### Threat indicator

```json
{
  "type": "domain | ipv4 | url | file_hash | ja4 | email_sender",
  "value": "esewa-verify.xyz",
  "first_seen": "2026-04-25T10:00:00Z"
}
```

### Threat report (request)

```json
{
  "type": "phishing | malware | ddos | c2",
  "indicators": [{ "type": "domain", "value": "...", "first_seen": "..." }],
  "severity": "low | medium | high | critical",
  "description": "free text, anonymized",
  "mitre_tactic": "TA0001"
}
```

### Sigma rule (output)

```yaml
title: SecureShare Auto-Generated Rule {id}
id: {uuid}
status: experimental
logsource:
  product: dns
detection:
  selection:
    query: "esewa-verify.xyz"
  condition: selection
level: high
tags:
  - secureshare.auto
  - secureshare.credibility.high
```

The five Sigma templates live in [`contracts/sigma_templates/`](../contracts/sigma_templates/).

---

## Where the artifacts live

| Artifact | Path | Owner |
|---|---|---|
| OpenAPI 3.1 spec | [`contracts/openapi.yaml`](../contracts/openapi.yaml) | P2 |
| Python Pydantic models | [`contracts/python/secureshare_contracts/`](../contracts/python/secureshare_contracts/) | P2 (with P1, P3, P4 as consumers) |
| TypeScript types | [`contracts/typescript/types.ts`](../contracts/typescript/types.ts) | P2 |
| Sigma rule templates | [`contracts/sigma_templates/`](../contracts/sigma_templates/) | P2 → P4 |
| Sample payloads | [`contracts/examples/`](../contracts/examples/) | shared |

---

## Versioning

Path prefix `/api/v1` is the only supported version for the hackathon. Breaking
changes during the build window: bump in-place, update this doc, ping the team.
After the hackathon: `/api/v2` for breaking changes, additive changes stay on v1.
