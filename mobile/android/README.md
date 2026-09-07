# TIWCG Android shell

This module wraps the existing tested POLITICS / Fifty-Three Days Python game rather than rewriting it. Chaquopy packages `engine/` and `render/` directly; `mobile_bridge.py` starts the same table server on `127.0.0.1`, and the Android WebView is only a shell.

SCARED SACRED remains Expansion Set 1 inside TIWCG; it is not the Android application identity.

## Store boundary

RevenueCat exists here to satisfy a real product boundary without selling game power, Witness Accounts, or access to the ruleset.

- entitlement: `sacred_table` by default
- product: configure one Google Play one-time product as **non-consumable**
- offering: place that product in the current RevenueCat offering
- effect: permanent cosmetic Sacred Table skin only
- restore: exposed in the native shell

Witness Accounts remain giver-owned, table-bound, and unsellable per base canon. All playable mechanics remain available without purchase.

## Android identity

- app label: `TIWCG — POLITICS`
- application ID: `org.theinterdependency.tiwcg`
- first public version: `1.0.0` / version code `1`

## Build

- Android Gradle Plugin 9.2.1
- Gradle 9.4.1
- Chaquopy 17.0.0
- Python 3.12
- compile/target API 36
- RevenueCat Android SDK 10.15.1

From `mobile/android`:

```sh
gradle --no-daemon :app:assembleDebug
gradle --no-daemon :app:bundleRelease
```

The public RevenueCat SDK key is injected at build time and is not committed:

```sh
gradle --no-daemon :app:bundleRelease \
  -PREVENUECAT_API_KEY=goog_xxx \
  -PREVENUECAT_ENTITLEMENT_ID=sacred_table
```

With no key, the game still builds and runs; the purchase controls remain visibly unconfigured rather than pretending monetization works.

## Shipaton handoff

See [`SHIPATON.md`](SHIPATON.md) for the exact playable demo path, release gates, Devpost deliverables, store-positioning copy, and two-minute video sequence.

A Shipaton-eligible release still requires external store configuration and publication: Google Play app, one-time product, RevenueCat project/offering/entitlement, signed AAB, store listing, judge access, icon, screenshot, and demo video.

hmmm — commerce belongs around the table, not between a witness and the room.
