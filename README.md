# SecureShare

A self-learning, privacy-preserving firewall network for Nepal — built for the
"Smart and Secure Future" hackathon track.

The product is the **Smart Firewall Gateway**: a six-layer defense that runs on
a Raspberry Pi (or any Linux box) and gets smarter by privately collaborating
with every other gateway in the network. The cloud platform exists to make the
gateway smarter than any commercial solution.

## Repo layout

```
secureshare/
├── contracts/         Shared API contracts — the single source of truth
│   ├── openapi.yaml          OpenAPI 3.1 spec for the platform REST API
│   ├── python/               Pydantic models (importable by platform + gateway)
│   ├── typescript/           TS types for the React dashboard
│   ├── sigma_templates/      The 5 pre-written Sigma rule templates
│   └── examples/             Sample payloads
├── docs/
│   └── API_CONTRACTS.md      Human-readable contract reference
├── platform/          FastAPI backend + GNN + FL aggregator (P1, P2)
├── gateway/           Smart Firewall Gateway, 6 layers (P4)
├── dashboard/         React + Tailwind CTI dashboard (P2)
└── fl/                Federated learning client/server code (P3)
```

The four implementation directories (`platform/`, `gateway/`, `dashboard/`,
`fl/`) are owned by individual team members and will be created when each
person starts their work in hour 4+.

## Hour-0 priority: lock the contracts

Everyone codes against `contracts/`. If you need to deviate, file a PR — don't
fork the schema in your own service. The Pydantic and TS modules are generated
by hand and kept in lockstep with `openapi.yaml`.

## Quickstart for contributors

```bash
# Use the shared Python models in any platform/ or gateway/ service
pip install -e contracts/python

# In code:
from secureshare_contracts import ThreatReportRequest, SigmaRule, Indicator
```

For the dashboard, copy `contracts/typescript/types.ts` into your project
(or set up a yarn workspace later — not worth it in 60 hours).
