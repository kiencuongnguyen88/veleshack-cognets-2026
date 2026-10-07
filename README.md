# Swarm Sentinel

**VelesHack 2026 — Challenge 4: CoGNETs / Smart Edge Resource Auctions**

Swarm Sentinel is a continuity-aware edge-auction agent that adapts to market conditions, protects compute/security service floors, and reduces energy demand as battery falls so the node remains useful across the run.

## Submission identity

- **TEAM_NAME:** `swarm-sentinel`
- **Entrant:** `@kiencuongnguyen88`
- **Challenge:** Challenge 4 — CoGNETs
- **Strategy file:** `agent-template/strategy.py`
- **Dockerfile:** `agent-template/Dockerfile`
- **Build:** `docker build -t swarm-sentinel agent-template`
- **Integrated run:** `make graded` then `make agent`
- **License:** Apache-2.0
- **Live pitch if selected:** Yes

## Strategy write-up (221 words)

Swarm Sentinel treats the challenge as a continuity problem, not a one-round bidding problem. Each round it first builds a market-aware allocation from the current prices, capacities and the device’s own preference weights. It then protects the minimum compute and security service floors so a good allocation is not destroyed by a 50% or 75% utility penalty.

The final continuity controller addresses the largest remaining loss: energy won from the market drains the node’s own battery. Swarm Sentinel tapers the energy bid continuously with battery state using a fixed battery^1.6 rule, then redistributes the freed budget to compute and security. This keeps the node useful for more of the run instead of maximizing immediate energy allocation and later losing whole rounds to recharge.

We did not keep the first candidate just because tuning looked positive. An earlier R017 strategy was rejected after its held-out batch turned negative. We reset the architecture, screened alternatives, froze the new candidate, and then validated it in 12 paired runs. The final candidate beat the shipped template in 12/12 runs (mean +3.4323, worst +1.2553) and beat the strongest built-in baseline in 12/12 (mean +2.8739, worst +0.2668). Compileall and the organizer conformance suite both passed, with zero strategy fallbacks.

We did not measure final swarm social-welfare impact, so we make no claim about improving the whole swarm.

## Validation evidence

| Evidence | Result |
|---|---:|
| Paired runs vs shipped template | **12/12 positive** |
| Mean delta vs shipped template | **+3.4323** |
| Worst delta vs shipped template | **+1.2553** |
| Paired runs vs strongest built-in baseline | **12/12 positive** |
| Mean delta vs strongest built-in baseline | **+2.8739** |
| Worst delta vs strongest built-in baseline | **+0.2668** |
| Strategy fallback / exception count | **0** |
| `compileall` | **PASS** |
| Organizer conformance | **PASS — rc=0** |

### Evidence note

The R023 receipt records that strict disjointness from every prior R017 held-out seed is not independently proven unless the complete earlier seed ledger is available. The paired R023 results above are real; this README does not overclaim strict seed novelty.

## What failed and what changed

The first strategy path looked promising on tuning seeds but failed its held-out R3 batch. We rejected it instead of tuning on that validation set. The redesign started from the organizer’s deeper problem: keep an autonomous node usefully participating under scarcity, service constraints and battery coupling. That reset led to the market + floor + continuity architecture used here.

## Reproduce

```bash
cp .env.example .env
sed -i 's/^TEAM_NAME=.*/TEAM_NAME=swarm-sentinel/' .env
make graded
make agent
make board
```

Before evaluation:

```bash
make check
# Docker-image variant:
# make check-docker IMAGE=<your-built-image>
```

## Repository contents

The organizer-provided arena, baselines, API documentation and conformance suite are preserved. The event strategy delta is in `agent-template/strategy.py`.
