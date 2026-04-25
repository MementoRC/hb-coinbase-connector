from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from market_connector.transport.endpoint import Endpoint
    from market_connector.transport.rest_base import AuthCallable, RestConnectorBase
    from market_connector.transport.ws_base import WsConnectorBase

    from coinbase_connector.config import CoinbaseConfig


class HasRest(Protocol):
    # CoinbaseRestClient is a subclass of RestConnectorBase, so declaring the base
    # is sufficient for structural typing. Mixins only use .request() which is
    # inherited unchanged.
    _rest: RestConnectorBase


class HasWs(Protocol):
    _ws: WsConnectorBase


class HasAuth(Protocol):
    _auth: AuthCallable


class HasEndpoints(Protocol):
    _endpoints: dict[str, Endpoint]


class HasConfig(Protocol):
    _config: CoinbaseConfig


class HasReady(Protocol):
    @property
    def ready(self) -> bool: ...
