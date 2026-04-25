"""Tests for SubscriptionsMixin — Phase 6, Task 6.4."""
from unittest.mock import AsyncMock, MagicMock

import pytest
from market_connector.exceptions import GatewayNotStartedError

from coinbase_connector.mixins.subscriptions import SubscriptionsMixin


class _TestableSubs(SubscriptionsMixin):
    def __init__(self, ws, rest=None):
        self._ws = ws
        self._rest = rest
        self._started = True

    @property
    def ready(self) -> bool:
        return self._started


@pytest.mark.asyncio
async def test_subscribe_trades_invokes_callback():
    ws = MagicMock()
    received: list = []
    captured_cb: dict = {}

    async def subscribe(channel, callback):
        captured_cb["cb"] = callback
        sub = MagicMock()
        sub.cancel = AsyncMock()
        return sub

    ws.subscribe = subscribe

    mixin = _TestableSubs(ws)

    async with await mixin.subscribe_trades("BTC-USD", received.append):
        # Simulate WS message delivery
        captured_cb["cb"]({
            "events": [{
                "type": "update",
                "trades": [{"trade_id": "t1", "product_id": "BTC-USD",
                            "price": "50000", "size": "0.5", "side": "BUY",
                            "time": "2026-04-24T12:00:00Z"}],
            }],
        })

    assert len(received) == 1
    assert received[0].exchange_trade_id == "t1"


@pytest.mark.asyncio
async def test_subscribe_trades_not_ready_raises():
    ws = MagicMock()
    mixin = _TestableSubs(ws)
    mixin._started = False
    with pytest.raises(GatewayNotStartedError):
        await mixin.subscribe_trades("BTC-USD", lambda e: None)
