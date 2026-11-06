"""Tools primitive — tool system with ABC interface and built-in tools."""

from __future__ import annotations

from tlow.tools._stubs import BaseTool, ToolExecutor, ToolSpec

# Import built-in tools to trigger @ToolRegistry.register() decorators.
# Each is wrapped in try/except so the package loads even before the
# individual tool modules are created.
try:
    import tlow.tools.calculator  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.think  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.retrieval  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.llm_tool  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.file_read  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.web_search  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.code_interpreter  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.code_interpreter_docker  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.repl  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.storage_tools  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.mcp_adapter  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.channel_tools  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.http_request  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.docker_shell_exec  # noqa: F401
    import tlow.tools.shell_exec  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.memory_manage  # noqa: F401
except ImportError:
    pass
try:
    import tlow.tools.user_profile_manage  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.skill_manage  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.file_write  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.apply_patch  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.git_tool  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.db_query  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.pdf_tool  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.image_tool  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.audio_tool  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.knowledge_tools  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.text_to_speech  # noqa: F401
except ImportError:
    pass

try:
    import tlow.tools.digest_collect  # noqa: F401
except ImportError:
    pass

__all__ = ["BaseTool", "ToolExecutor", "ToolSpec"]
