# hb-coinbase-connector — ARCHIVED

> **This repository has been merged into [hb-market-connector](https://github.com/MementoRC/hb-market-connector) as `market_connector.exchanges.coinbase`.**
>
> Install with:
>
> ```bash
> pip install hb-market-connector[coinbase]
> ```
>
> The merge landed in [hb-market-connector#11](https://github.com/MementoRC/hb-market-connector/pull/11). This repository is preserved read-only for historical reference. The original 40-commit history with GPG-verified signatures is preserved at the tag [`archive/pre-merge-into-market-connector`](https://github.com/MementoRC/hb-coinbase-connector/releases/tag/archive/pre-merge-into-market-connector).
>
> **No further development happens here.** New issues, PRs, or contributions should go to [hb-market-connector](https://github.com/MementoRC/hb-market-connector).

---

## Why this was merged

`hb-coinbase-connector` was a specialization of `hb-market-connector` (rich behavioral inheritance from `RestConnectorBase`, `WsConnectorBase`, primitives, exceptions, testing infrastructure), not a sibling sub-package. Treating it as a separate repository required workarounds for cross-repo dependencies (path deps, git URL resolution, hatchling `allow-direct-references`) and duplicated CI overhead. The correct architectural placement is as a sub-package within `hb-market-connector/market_connector/exchanges/`, mirroring the multi-exchange layout used by ccxt and freqtrade.

The full migration plan and rationale lives at [`docs/superpowers/plans/2026-04-25-coinbase-merge-into-market-connector.md`](https://github.com/MementoRC/hummingbot/blob/ci-base/docs/superpowers/plans/2026-04-25-coinbase-merge-into-market-connector.md) in the parent hummingbot repo.

## Development (historical)

```bash
pixi install
pixi run check
```

## License

Apache-2.0
