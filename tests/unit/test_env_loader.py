import os
import pytest
from utils import env_loader

def test_safe_get_env_local(monkeypatch):
    monkeypatch.setenv("MY_TEST_KEY", "test_value")
    assert env_loader.safe_get_env("MY_TEST_KEY") == "test_value"

def test_safe_get_env_default(monkeypatch):
    monkeypatch.delenv("MY_MISSING_KEY", raising=False)
    assert env_loader.safe_get_env("MY_MISSING_KEY", default="fallback") == "fallback"

def test_using_streamlit_secrets_false(tmp_path, monkeypatch):
    monkeypatch.setattr(env_loader, "os", os)
    assert not env_loader.using_streamlit_secrets()