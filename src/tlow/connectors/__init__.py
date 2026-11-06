"""Data source connectors for Deep Research."""

from tlow.connectors._stubs import (
    Attachment,
    BaseConnector,
    Document,
    SyncStatus,
)
from tlow.connectors.store import KnowledgeStore

__all__ = ["Attachment", "BaseConnector", "Document", "KnowledgeStore", "SyncStatus"]

# Auto-register built-in connectors
import tlow.connectors.obsidian  # noqa: F401

try:
    import tlow.connectors.gmail  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.gmail_imap  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.gdrive  # noqa: F401
except ImportError:
    pass  # httpx may not be installed

try:
    import tlow.connectors.notion  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.granola  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.gcontacts  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.imessage  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.apple_notes  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.apple_music  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.apple_contacts  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.slack_connector  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.outlook  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.gcalendar  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.dropbox  # noqa: F401
except ImportError:
    pass  # httpx may not be installed

try:
    import tlow.connectors.whatsapp  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.oura  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.apple_health  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.strava  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.spotify  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.google_tasks  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.weather  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.github_notifications  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.hackernews  # noqa: F401
except ImportError:
    pass

try:
    import tlow.connectors.news_rss  # noqa: F401
except ImportError:
    pass
