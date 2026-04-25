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


# ---------------------------------------------------------------------------
# 4.3  Order converter
# ---------------------------------------------------------------------------

_SIDE_MAP: dict[str, TradeType] = {
    "BUY": TradeType.BUY,
    "SELL": TradeType.SELL,
}


def _extract_order_details(cfg: OrderConfiguration) -> tuple[OrderType, Decimal, Decimal]:
    """Return (order_type, amount, price) from an OrderConfiguration."""
    if cfg.limit_limit_gtc is not None:
        c = cfg.limit_limit_gtc
        ot = OrderType.LIMIT_MAKER if c.post_only else OrderType.LIMIT
        return ot, Decimal(c.base_size), Decimal(c.limit_price)
    if cfg.limit_limit_gtd is not None:
        c = cfg.limit_limit_gtd
        return OrderType.LIMIT, Decimal(c.base_size), Decimal(c.limit_price)
    if cfg.market_market_ioc is not None:
        c = cfg.market_market_ioc
        size = c.base_size or c.quote_size or "0"
        return OrderType.MARKET, Decimal(size), Decimal("0")
    raise ValueError("Unsupported order configuration")


def to_open_order(order: Order) -> OpenOrder:
    """Convert a Coinbase REST Order schema to a market-connector OpenOrder primitive."""
    if order.order_configuration is not None:
        ot, amount, price = _extract_order_details(order.order_configuration)
    else:
        ot, amount, price = OrderType.LIMIT, Decimal("0"), Decimal("0")

    return OpenOrder(
        client_order_id=order.client_order_id,
        exchange_order_id=order.order_id,
        trading_pair=from_exchange_pair(order.product_id),
        order_type=ot,
        side=_SIDE_MAP[order.side.value],
        amount=amount,
        price=price,
        filled_amount=Decimal(order.filled_size),
        status=order.status.value,
    )
