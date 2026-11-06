"""Tests for speech configuration."""

from tlow.core.config import TLOWConfig, SpeechConfig


def test_speech_config_defaults():
    cfg = SpeechConfig()
    assert cfg.backend == "auto"
    assert cfg.model == "base"
    assert cfg.language == ""
    assert cfg.device == "auto"
    assert cfg.compute_type == "float16"


def test_tlow_config_has_speech():
    cfg = TLOWConfig()
    assert hasattr(cfg, "speech")
    assert isinstance(cfg.speech, SpeechConfig)
    assert cfg.speech.backend == "auto"


def test_tlow_system_has_speech_backend():
    """TLOWSystem has a speech_backend attribute."""
    from tlow.system import TLOWSystem

    assert "speech_backend" in TLOWSystem.__dataclass_fields__
