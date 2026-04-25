"""hb-coinbase-connector — Coinbase Advanced Trade gateway."""

from coinbase_connector.__about__ import __version__
from coinbase_connector.coinbase_gateway import CoinbaseGateway
from coinbase_connector.config import CoinbaseConfig

__all__ = ["CoinbaseConfig", "CoinbaseGateway", "__version__"]
