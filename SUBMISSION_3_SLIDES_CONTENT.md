# Swarm Sentinel — 3-slide template fill

Paste this content into the organizer-provided 3-slide template.

## Slide 1 — Problem & idea
**Swarm Sentinel** — Continuity-aware resource auctions for autonomous edge nodes

- No central scheduler: each node allocates scarce compute, energy and security locally.
- Service-floor misses destroy round utility.
- Winning too much energy drains the node and creates zero-score resting rounds.
- **Idea:** market-aware allocation + floor protection + battery continuity control.
- **Goal:** optimize long-horizon useful participation, not one-round resource capture.

## Slide 2 — How it works
1. Read prices, capacities and device weights.
2. Estimate competing demand and protect compute/security floors.
3. Taper energy continuously with `battery^1.6`.
4. Reallocate saved energy budget to compute/security.
5. Keep organizer starter lifecycle/resilience logic unchanged.

`market signal → proportional allocation → floor guard → battery taper → legal full-budget bid`

## Slide 3 — Evidence & learning
- **12/12** better than shipped template; mean **+3.4323**, worst **+1.2553**.
- **12/12** better than strongest built-in baseline; mean **+2.8739**, worst **+0.2668**.
- `compileall`: PASS.
- Organizer conformance: PASS.
- Strategy fallback/exception: **0**.
- Earlier R017 candidate failed held-out validation; we rejected it and reset the architecture.
- No final swarm social-welfare measurement, so no unsupported welfare claim.

`TEAM_NAME: swarm-sentinel` · `github.com/kiencuongnguyen88/veleshack-cognets-2026`
