"""Tests for coinbase_connector.converters — pure conversion functions."""
from decimal import Decimal

from coinbase_connector.converters import from_exchange_pair, to_balance, to_exchange_pair
from coinbase_connector.schemas.rest import Account, Balance


def test_to_exchange_pair_passthrough():
    assert to_exchange_pair("BTC-USD") == "BTC-USD"


def test_from_exchange_pair_passthrough():
    assert from_exchange_pair("BTC-USD") == "BTC-USD"


# ---------------------------------------------------------------------------
# 4.2  Balance converter
# ---------------------------------------------------------------------------


def test_to_balance_extracts_available():
    account = Account(
        uuid="u1",
        name="BTC Wallet",
        currency="BTC",
        available_balance=Balance(value="1.5", currency="BTC"),
        hold=Balance(value="0.3", currency="BTC"),
    )
    assert to_balance(account) == Decimal("1.5")
