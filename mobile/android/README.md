# SCARED SACRED Android shell

This module wraps the existing tested Python game rather than rewriting it.
Chaquopy packages `engine/` and `render/` directly; `mobile_bridge.py` starts
the same table server on `127.0.0.1`, and the Android WebView is only a shell.

## Store boundary

RevenueCat exists here to satisfy a real product boundary without selling game
power, Witness Accounts, or access to the ruleset.

- entitlement: `sacred_table` by default
- product: configure one Google Play one-time product as **non-consumable**
- offering: place that product in the current RevenueCat offering
- effect: permanent cosmetic Sacred Table skin only
- restore: exposed in the native shell

Witness Accounts remain giver-owned, table-bound, and unsellable per base canon.
All playable mechanics remain available without purchase.

## Build

The build intentionally pins the newest combination currently claimed compatible
by both Android and Chaquopy rather than using incompatible latest versions:

- Android Gradle Plugin 9.2.1
- Gradle 9.4.1
- Chaquopy 17.0.0
- Python 3.12
- compile/target API 36
- RevenueCat Android SDK 10.15.1

From `mobile/android`:

```sh
gradle :app:assembleDebug
```

The public RevenueCat SDK key is injected at build time and is not committed:

```sh
gradle :app:assembleDebug \
  -PREVENUECAT_API_KEY=goog_xxx \
  -PREVENUECAT_ENTITLEMENT_ID=sacred_table
```

With no key, the game still builds and runs; the purchase controls remain
visibly unconfigured rather than pretending monetization works.

## Store release boundary

A Shipaton-eligible release still requires the external store configuration:
Google Play app, one-time product, RevenueCat project/offering/entitlement,
signed AAB, store listing, judge access, icon, screenshot, and demo video.

hmmm — commerce belongs around the table, not between a witness and the room.
