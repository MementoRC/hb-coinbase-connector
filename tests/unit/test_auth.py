"""Tests for coinbase_connector.auth — Phase 1."""

import pytest
import jwt as pyjwt

from coinbase_connector.auth import _build_jwt, _normalize_pem


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


class TestBuildJwt:
    def test_includes_required_claims(self, ec_private_pem: str) -> None:
        token = _build_jwt(api_key="test-key", pem=ec_private_pem, uri="GET api.coinbase.com/v3/test")
        decoded = pyjwt.decode(token, options={"verify_signature": False})
        assert decoded["sub"] == "test-key"
        assert decoded["iss"] == "cdp"
        assert decoded["uri"] == "GET api.coinbase.com/v3/test"
        assert "nbf" in decoded and "exp" in decoded
        assert decoded["exp"] - decoded["nbf"] == 120

    def test_omits_uri_for_ws(self, ec_private_pem: str) -> None:
        token = _build_jwt(api_key="test-key", pem=ec_private_pem, uri=None)
        decoded = pyjwt.decode(token, options={"verify_signature": False})
        assert "uri" not in decoded

    def test_includes_kid_and_nonce(self, ec_private_pem: str) -> None:
        token = _build_jwt(api_key="test-key", pem=ec_private_pem, uri=None)
        headers = pyjwt.get_unverified_header(token)
        assert headers["kid"] == "test-key"
        assert "nonce" in headers and len(headers["nonce"]) > 0
