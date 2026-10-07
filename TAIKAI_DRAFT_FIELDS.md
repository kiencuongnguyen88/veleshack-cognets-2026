# TAIKAI submission draft fields

- Project: **Swarm Sentinel**
- Challenge: **Challenge 4 — COGNETS**
- TEAM_NAME: `swarm-sentinel`
- Repository: `https://github.com/kiencuongnguyen88/veleshack-cognets-2026`
- Dockerfile: `agent-template/Dockerfile`
- Build: `docker build -t swarm-sentinel agent-template`
- Live pitch if selected: **Yes**

## Short description
Swarm Sentinel is a continuity-aware edge-auction agent that combines market-aware resource allocation, compute/security floor protection, and battery-aware energy tapering so an autonomous node stays useful across volatile, resource-constrained swarm runs.

## Full description
Swarm Sentinel treats Smart Edge Resource Auctions as a continuity problem rather than a one-round bidding problem. The agent reads current market prices and capacities, allocates toward high-value resources, protects minimum compute and security service floors, and continuously tapers energy demand as battery falls. Freed budget is reallocated to compute and security.

The final R023 candidate was frozen and tested in 12 paired runs. It beat the shipped template in 12/12 runs (mean +3.4323; worst +1.2553) and beat the strongest built-in baseline in 12/12 (mean +2.8739; worst +0.2668). Compileall passed, organizer conformance passed, and the strategy produced zero fallbacks/exceptions.

An earlier candidate was deliberately rejected after held-out validation turned negative. That failure drove an architecture reset toward continuity-aware operation rather than local patching.

We make no unsupported claim about swarm-wide social-welfare improvement because that metric was not measured in the final validation.

**DO NOT PUBLISH/SUBMIT WITHOUT H1.**
