"""Structural protocols for substituting fakes in place of TLOWSystem."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Protocol

if TYPE_CHECKING:
    from tlow.core.config import TLOWConfig
    from tlow.core.events import EventBus
    from tlow.engine._stubs import InferenceEngine
    from tlow.security.capabilities import CapabilityPolicy
    from tlow.sessions.session import SessionStore
    from tlow.tools._stubs import BaseTool
    from tlow.tools.storage._stubs import MemoryBackend
    from tlow.traces.collector import TraceCollector
    from tlow.traces.store import TraceStore


class OrchestratorDeps(Protocol):
    """Minimum surface of TLOWSystem that QueryOrchestrator depends on.

    Tests can satisfy this with a lightweight class — no need to construct
    the full TLOWSystem dataclass or materialize every subsystem.
    """

    config: TLOWConfig
    bus: EventBus
    engine: InferenceEngine
    engine_key: str
    model: str
    agent_name: str
    tools: List[BaseTool]
    memory_backend: Optional[MemoryBackend]
    capability_policy: Optional[CapabilityPolicy]
    session_store: Optional[SessionStore]
    trace_store: Optional[TraceStore]
    trace_collector: Optional[TraceCollector]  # written by _run_agent

    # Optional attribute (getattr with default) — declared for type clarity.
    _skill_few_shot_examples: Any
