"""Shared API contracts for the SecureShare platform and gateway.

Both the FastAPI backend and the gateway services import models from here.
Keep this package free of business logic — only schemas, enums, and
serialization helpers.
"""

from .models import (
    BlockEvent,
    BlocksRecentResponse,
    ClusterMember,
    ClusterRelationship,
    FlRegisterRequest,
    FlRegisterResponse,
    FlSubmitUpdateResponse,
    GatewayStatus,
    GnnClusterRequest,
    GnnClusterResponse,
    Indicator,
    IndicatorType,
    Pagination,
    Severity,
    SigmaRule,
    SigmaRulesResponse,
    TelemetryConfirmRequest,
    TelemetryConfirmResponse,
    ThreatFeedResponse,
    ThreatReport,
    ThreatReportRequest,
    ThreatReportResponse,
    ThreatType,
    WhitelistRequest,
    ZKVerifyRequest,
    ZKVerifyResponse,
)

__all__ = [
    "BlockEvent",
    "BlocksRecentResponse",
    "ClusterMember",
    "ClusterRelationship",
    "FlRegisterRequest",
    "FlRegisterResponse",
    "FlSubmitUpdateResponse",
    "GatewayStatus",
    "GnnClusterRequest",
    "GnnClusterResponse",
    "Indicator",
    "IndicatorType",
    "Pagination",
    "Severity",
    "SigmaRule",
    "SigmaRulesResponse",
    "TelemetryConfirmRequest",
    "TelemetryConfirmResponse",
    "ThreatFeedResponse",
    "ThreatReport",
    "ThreatReportRequest",
    "ThreatReportResponse",
    "ThreatType",
    "WhitelistRequest",
    "ZKVerifyRequest",
    "ZKVerifyResponse",
]
