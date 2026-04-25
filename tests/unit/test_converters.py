"""Tests for coinbase_connector.converters — pure conversion functions."""
from decimal import Decimal

from market_connector.primitives import OrderType, TradeType

from coinbase_connector.converters import from_exchange_pair, to_balance, to_exchange_pair, to_open_order
from coinbase_connector.schemas.rest import Account, Balance, LimitGTCConfig, Order, OrderConfiguration


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


# ---------------------------------------------------------------------------
# 4.3  Order converter
# ---------------------------------------------------------------------------


def test_to_open_order_from_limit():
    order = Order(
        order_id="o1",
        client_order_id="c1",
        product_id="BTC-USD",
        side="BUY",
        status="OPEN",
        order_configuration=OrderConfiguration(
            limit_limit_gtc=LimitGTCConfig(base_size="0.5", limit_price="50000"),
        ),
        filled_size="0.1",
        average_filled_price="50000",
    )
    result = to_open_order(order)
    assert result.exchange_order_id == "o1"
    assert result.client_order_id == "c1"
    assert result.trading_pair == "BTC-USD"
    assert result.side == TradeType.BUY
    assert result.amount == Decimal("0.5")
    assert result.price == Decimal("50000")
    assert result.filled_amount == Decimal("0.1")
    assert result.order_type == OrderType.LIMIT
