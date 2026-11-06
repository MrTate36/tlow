"""Skill source resolvers — Hermes, OpenClaw, generic GitHub."""

from tlow.skills.sources.base import ResolvedSkill, SourceResolver
from tlow.skills.sources.github import GitHubResolver
from tlow.skills.sources.hermes import HERMES_REPO_URL, HermesResolver
from tlow.skills.sources.openclaw import OPENCLAW_REPO_URL, OpenClawResolver

__all__ = [
    "GitHubResolver",
    "HERMES_REPO_URL",
    "HermesResolver",
    "OPENCLAW_REPO_URL",
    "OpenClawResolver",
    "ResolvedSkill",
    "SourceResolver",
]
