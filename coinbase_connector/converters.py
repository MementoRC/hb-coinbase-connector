"""Pure conversion functions: Coinbase schemas → market-connector primitives."""
from decimal import Decimal

from market_connector.primitives import (
    OpenOrder,
    OrderBookSnapshot,
    OrderBookUpdate,
    OrderType,
    TradeEvent,
    TradeType,
)

from coinbase_connector.schemas.rest import Account, Candle, Order, OrderBookResponse, OrderConfiguration
from coinbase_connector.schemas.ws import Level2Event, MarketTrade


# ---------------------------------------------------------------------------
# 4.1  Pair passthrough
# ---------------------------------------------------------------------------


def to_exchange_pair(trading_pair: str) -> str:
    """Convert a Hummingbot trading pair to a Coinbase product_id (identity)."""
    return trading_pair


def from_exchange_pair(product_id: str) -> str:
    """Convert a Coinbase product_id to a Hummingbot trading pair (identity)."""
    return product_id


# ---------------------------------------------------------------------------
# 4.2  Balance converter
# ---------------------------------------------------------------------------


def to_balance(account: Account) -> Decimal:
    """Extract the available balance as Decimal from an Account schema."""
    return Decimal(account.available_balance.value)
