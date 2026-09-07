# TIWCG — RevenueCat Shipaton release path

Status: first-public-release preparation for RevenueCat Shipaton 2026.

The release slice is deliberately narrow. **POLITICS / Fifty-Three Days is the playable game.** Do not block first publication on the generalized TIWCG turn law, AHBG territory mode, UCNS integration, new knowledge kits, or other planned layers.

## What ships

- App: **TIWCG — POLITICS**
- Android application ID: `org.theinterdependency.tiwcg`
- Version: `1.0.0` / version code `1`
- Game: POLITICS / Fifty-Three Days
- Human seat: playable in the Android WebView
- Other seats: current engine-supported agents
- RevenueCat: one permanent cosmetic entitlement
- Entitlement ID: `sacred_table` unless deliberately changed before store creation
- Gameplay, rules, and Witness Accounts are not paywalled

## Playable demo loop

The existing game is the Shipaton demo. A judge/player can:

1. enter the live POLITICS table;
2. observe the Machine reveal a historical beat;
3. inspect the dealt hand, agenda, and Arcanum;
4. lay a static or play an action;
5. discard where required by hand law;
6. use a legal reflex in a reaction window or pass;
7. play the dealt Arcanum;
8. watch the population / E / M state register consequences;
9. continue until the Machine deck empties above population 50 (win) or population reaches 50 or below (loss).

No separate hackathon-only match should be fabricated.

## Build gates

CI must pass both:

```sh
gradle --no-daemon :app:assembleDebug
gradle --no-daemon :app:bundleRelease
```

A real RevenueCat-key build can be produced with:

```sh
REVENUECAT_API_KEY='goog_...' \
REVENUECAT_ENTITLEMENT_ID='sacred_table' \
gradle --no-daemon :app:bundleRelease
```

CI intentionally builds an unsigned release AAB. Store upload signing credentials remain external secrets and must not be committed.

## External release gates

These cannot be completed by repository code alone:

- [ ] Create the Android app in Google Play (or another qualifying store) using `org.theinterdependency.tiwcg`.
- [ ] Create the RevenueCat project/app and connect the real store application.
- [ ] Create one one-time, non-consumable cosmetic product.
- [ ] Attach that product to entitlement `sacred_table`.
- [ ] Put the product into the Current Offering.
- [ ] Build/install with the real public RevenueCat Android key.
- [ ] Complete a sandbox/test purchase and restore test.
- [ ] Create and protect the upload-signing key.
- [ ] Sign the release AAB and upload it to the store.
- [ ] Complete store content/privacy/data-safety declarations accurately.
- [ ] Publish the first public version during the Shipaton eligibility window.
- [ ] Provide judge premium access by the method accepted by the Shipaton rules (promo code or qualifying free access mechanism).

## Store-positioning copy

### App name

TIWCG — POLITICS

### Short description

A card game where human intervention changes the course of a historical Machine.

### Core description

POLITICS is the first playable game inside TIWCG. History advances through an automated Machine deck. Players respond with cards, statics, reactions, Arcana, and coordinated intervention while a population field registers the consequences.

The game does not ask whether a card sounds persuasive. The engine resolves legal actions and records what changed. Survive the Machine with more than half the population remaining to win.

The optional Sacred Table purchase changes presentation only. It does not sell stronger cards, rule access, Witness Accounts, or competitive power.

## Shipaton demo video — maximum two minutes

Record the real Android build running on the target device.

Suggested sequence:

1. **0:00–0:10** — launch `TIWCG — POLITICS`; show the live table.
2. **0:10–0:30** — Machine reveals a beat; show population / E / M and the human hand.
3. **0:30–0:55** — play a real action or static and show the registered change.
4. **0:55–1:15** — show a reaction/reflex window or Arcanum.
5. **1:15–1:35** — show continued Machine/player interleaving and the win/loss objective.
6. **1:35–1:55** — show the RevenueCat Sacred Table purchase/entitlement and resulting cosmetic change.
7. **1:55–2:00** — identify it as the first TIWCG game and end.

Do not spend the video explaining unimplemented future architecture. Demonstrate what runs.

## Devpost minimum package

- [ ] Text description of features/functionality.
- [ ] Public YouTube or Vimeo demo, no longer than two minutes of essential footage.
- [ ] Published Android store URL.
- [ ] 1024×1024 app icon.
- [ ] At least one 1179×2556 screenshot with no device frame.
- [ ] RevenueCat project ID.
- [ ] Android selected as app type.
- [ ] Judge premium-access method.

Recommended award targets for this release:

- **Best Game Award** — primary.
- **RevenueCat Peace Prize** — compatible with the game's intervention/repair purpose if the submission describes only implemented behavior and actual intended social benefit.
- **HAMM Award** — only if the monetization explanation is strong enough; the current first-release purchase is intentionally modest and non-pay-to-win.

## Not release blockers

The following remain valid TIWCG work, but are not prerequisites for first Shipaton publication:

- generalized 7-card / draw-2 / drop-2 / METAPAT turn system;
- Base Survival Kit;
- emergent menagerie creation;
- logical-fallacy Instants;
- Paradigm Shift Closure;
- generalized identity coupling;
- UCNS relation adapter;
- first-class generalized EDCM conflict interface beyond current POLITICS behavior;
- AHBG territory mode;
- Discord/social adapters;
- knowledge-kit marketplace;
- user artwork overrides.

Ship the working game first. Extend the containing system without rewriting the demonstrated match.

## hmmm

Store signing, RevenueCat dashboard state, published listing, judge-access code, icon, screenshot, and video are external release artifacts. Repository CI can prove the code builds; it cannot truthfully mark those external gates complete.
