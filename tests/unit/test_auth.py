"""Tests for coinbase_connector.auth — Phase 1."""

import pytest

from coinbase_connector.auth import _normalize_pem


class TestNormalizePem:
    def test_accepts_multiline_pem(self, ec_private_pem: str) -> None:
        result = _normalize_pem(ec_private_pem)
        assert result.startswith("-----BEGIN EC PRIVATE KEY-----")
        assert result.endswith("-----END EC PRIVATE KEY-----")

    def test_accepts_raw_base64(self, ec_private_b64: str) -> None:
        result = _normalize_pem(ec_private_b64)
        assert "-----BEGIN EC PRIVATE KEY-----" in result

    def test_rejects_invalid(self) -> None:
        with pytest.raises(ValueError):
            _normalize_pem("not a key")
