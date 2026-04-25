"""Pydantic models matching contracts/openapi.yaml.

Mirror of the OpenAPI spec — if you change one, change both. The OpenAPI
file is authoritative for external consumers; this module is authoritative
for any Python service in this repo.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class _Base(BaseModel):
    """Shared base — strict by default, forbid unknown fields at the boundary."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class IndicatorType(str, Enum):
    DOMAIN = "domain"
    IPV4 = "ipv4"
    URL = "url"
    FILE_HASH = "file_hash"
    JA4 = "ja4"
    EMAIL_SENDER = "email_sender"


class ThreatType(str, Enum):
    PHISHING = "phishing"
    MALWARE = "malware"
    DDOS = "ddos"
    C2 = "c2"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ClusterRelationship(str, Enum):
    RESOLVES_TO = "resolves_to"
    ISSUED_BY = "issued_by"
    SHARES_CERT_WITH = "shares_cert_with"
    REGISTERED_VIA = "registered_via"
    SAME_ASN = "same_asn"
    EMBEDDING_NEIGHBOR = "embedding_neighbor"


# ---------------------------------------------------------------------------
# Core data shapes
# ---------------------------------------------------------------------------


class Indicator(_Base):
    type: IndicatorType
    value: Annotated[str, Field(min_length=1, max_length=2048)]
    first_seen: datetime


# ---------------------------------------------------------------------------
# /auth/zk-verify
# ---------------------------------------------------------------------------


class ZKVerifyRequest(_Base):
    proof: str | dict
    publicSignals: list[str]
    nullifierHash: str


class ZKVerifyResponse(_Base):
    sessionToken: str
    anonymousId: str
    credibilityScore: Annotated[float, Field(ge=0.0, le=1.0)]


# ---------------------------------------------------------------------------
# /threats/*
# ---------------------------------------------------------------------------


class ThreatReportRequest(_Base):
    type: ThreatType
    indicators: Annotated[list[Indicator], Field(min_length=1)]
    severity: Severity
    description: Annotated[str, Field(max_length=4000)]
    mitre_tactic: str | None = None


class ThreatReportResponse(_Base):
    reportId: str
    sigmaRuleId: str
    anonymousReporter: str


class ThreatReport(_Base):
    reportId: str
    type: ThreatType
    indicators: list[Indicator]
    severity: Severity
    description: str
    mitre_tactic: str | None = None
    anonymousReporter: str
    credibility: Annotated[float, Field(ge=0.0, le=1.0)]
    createdAt: datetime


class Pagination(_Base):
    cursor: str | None = None
    hasMore: bool


class ThreatFeedResponse(_Base):
    reports: list[ThreatReport]
    pagination: Pagination


# ---------------------------------------------------------------------------
# /sigma/rules
# ---------------------------------------------------------------------------


class SigmaRule(_Base):
    id: str
    yaml: str
    sourceCredibility: Annotated[float, Field(ge=0.0, le=1.0)]
    expiresAt: datetime


class SigmaRulesResponse(_Base):
    rules: list[SigmaRule]


# ---------------------------------------------------------------------------
# /telemetry/confirm
# ---------------------------------------------------------------------------


class TelemetryConfirmRequest(_Base):
    ruleIds: list[str]
    hitCounts: list[Annotated[int, Field(ge=0)]]
    aggregatedAt: datetime


class TelemetryConfirmResponse(_Base):
    accepted: int
    credibilityDelta: float


# ---------------------------------------------------------------------------
# /gnn/cluster
# ---------------------------------------------------------------------------


class GnnClusterRequest(_Base):
    seedIndicator: Indicator


class ClusterMember(_Base):
    indicator: Indicator
    score: Annotated[float, Field(ge=0.0, le=1.0)]
    relationship: ClusterRelationship


class GnnClusterResponse(_Base):
    cluster: list[ClusterMember]


# ---------------------------------------------------------------------------
# /fl/*
# ---------------------------------------------------------------------------


class FlRegisterRequest(_Base):
    gatewayPublicKey: str
    capabilities: list[str]


class FlRegisterResponse(_Base):
    clientId: str
    aggregatorEndpoint: HttpUrl
    currentRound: Annotated[int, Field(ge=0)]


class FlSubmitUpdateResponse(_Base):
    accepted: bool
    nextRoundAt: datetime


# ---------------------------------------------------------------------------
# Gateway internal API
# ---------------------------------------------------------------------------


class GatewayStatus(_Base):
    layersActive: list[int]
    ruleCount: int
    modelVersion: str
    blocksToday: int


class BlockEvent(_Base):
    timestamp: datetime
    layer: int
    indicator: str
    reason: str


class BlocksRecentResponse(_Base):
    events: list[BlockEvent]


class WhitelistRequest(_Base):
    domain: str
    reason: str
