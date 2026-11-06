"""Smoke test that the tmp_tlow_home fixture works."""

from __future__ import annotations

from pathlib import Path

from tlow.core import config as config_mod


def test_fixture_redirects_default_config_dir(tmp_tlow_home: Path) -> None:
    assert config_mod.DEFAULT_CONFIG_DIR == tmp_tlow_home
    assert tmp_tlow_home.exists()
    assert (tmp_tlow_home / ".state").exists()
    assert (tmp_tlow_home / ".state" / "models").exists()


def test_fixture_redirects_config_path(tmp_tlow_home: Path) -> None:
    assert config_mod.DEFAULT_CONFIG_PATH == tmp_tlow_home / "config.toml"
