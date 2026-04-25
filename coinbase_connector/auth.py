"""Authentication utilities for the Coinbase Advanced Trade API."""

from __future__ import annotations

import binascii
import textwrap

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def _normalize_pem(secret_key: str) -> str:
    """Normalize secret_key to a valid PEM string.

    Accepts either a full PEM string (with headers and newlines) or a raw
    base64-encoded key body (without headers).  Raises ValueError if the
    input cannot be parsed as a valid EC private key.
    """
    key = secret_key.strip().replace("\\n", "\n")

    if key.startswith("-----") and "\n" in key:
        # Validate it's actually loadable before returning
        serialization.load_pem_private_key(key.encode(), password=None, backend=default_backend())
        return key

    # Strip headers if present but newlines were lost
    key = (
        key.replace("-----BEGIN EC PRIVATE KEY-----", "")
        .replace("-----END EC PRIVATE KEY-----", "")
        .strip()
    )

    try:
        binascii.a2b_base64(key)
    except binascii.Error as exc:
        raise ValueError("The secret key is not a valid base64 string.") from exc

    wrapped = textwrap.wrap(key, width=64)
    pem = (
        "-----BEGIN EC PRIVATE KEY-----\n"
        + "\n".join(wrapped)
        + "\n-----END EC PRIVATE KEY-----"
    )
    serialization.load_pem_private_key(pem.encode(), password=None, backend=default_backend())
    return pem
