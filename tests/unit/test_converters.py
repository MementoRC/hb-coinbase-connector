"""Tests for coinbase_connector.converters — pure conversion functions."""
from decimal import Decimal

from coinbase_connector.converters import from_exchange_pair, to_exchange_pair


def test_to_exchange_pair_passthrough():
    assert to_exchange_pair("BTC-USD") == "BTC-USD"


def test_from_exchange_pair_passthrough():
    assert from_exchange_pair("BTC-USD") == "BTC-USD"
