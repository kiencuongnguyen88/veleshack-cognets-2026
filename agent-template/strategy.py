"""
VelesHack 2026 C4 — R021/R022 selected local-validation candidate.
Market-aware proportional allocator + service-floor guard + bounded battery continuity control.
Candidate only. No commit/push or TAIKAI authority.
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations
from typing import Any, Dict, List

RESOURCES = ("compute", "energy", "security")
FLOOR_MARGIN = 1.20
BATTERY_TAPER_ALPHA = 1.60

def _floor_target(floor: Any, capacity: Any) -> float:
    return min(float(floor) * FLOOR_MARGIN, 0.95 * float(capacity))

def _estimate_others(history: List[Dict[str, Any]]) -> Dict[str, float]:
    if not history:
        return {k: 1.0 for k in RESOURCES}
    last = history[-1]
    prices = last.get("prices") or {}
    caps = last.get("capacities") or {}
    mine = last.get("bid") or {}
    out: Dict[str, float] = {}
    for k in RESOURCES:
        if k in prices and k in caps:
            out[k] = max(1e-4, float(prices[k]) * float(caps[k]) - float(mine.get(k, 0.0)))
        else:
            out[k] = 1.0
    return out

def _buy_floors(bid, budget, capacities, q_min, s_min, others):
    bid = dict(bid)
    for k, floor in (("compute", q_min), ("security", s_min)):
        cap = float(capacities.get(k, 1.0))
        s_k = max(float(others.get(k, 1.0)), 1e-9)
        if floor <= 0.0 or floor >= cap:
            continue
        needed = s_k * floor / (cap - floor)
        if needed <= bid.get(k, 0.0):
            continue
        deficit = needed - bid[k]
        donors = [r for r in RESOURCES if r != k and bid.get(r, 0.0) > 0.0]
        available = sum(bid[r] for r in donors)
        headroom = max(0.0, budget - sum(bid.values()))
        take = min(deficit, headroom + available)
        if take <= 0.0:
            continue
        from_donors = take - min(take, headroom)
        if from_donors > 0.0 and available > 1e-9:
            for r in donors:
                bid[r] -= from_donors * (bid[r] / available)
        bid[k] += take
    total = sum(bid.values())
    if total > budget and total > 1e-9:
        bid = {k: v * (budget / total) for k, v in bid.items()}
    return {k: max(0.0, v) for k, v in bid.items()}

def _market_floor_base(budget, prices, capacities, profile, history):
    weights = profile.get("weights", {})
    scores = {}
    for k in RESOURCES:
        price = max(float(prices.get(k, 1.0)), 0.05)
        cap = float(capacities.get(k, 1.0))
        weight = float(weights.get(k, 1.0 / 3.0))
        scores[k] = weight * weight * cap / price
    total = sum(scores.values()) or 1.0
    bid = {k: budget * value / total for k, value in scores.items()}
    others = _estimate_others(history)
    return _buy_floors(
        bid, budget, capacities,
        _floor_target(profile.get("q_min", 0.0), capacities.get("compute", 1.0)),
        _floor_target(profile.get("s_min", 0.0), capacities.get("security", 1.0)),
        others,
    )

def _redistribute_energy_cut(bid, new_energy, budget):
    bid = dict(bid)
    old = float(bid["energy"])
    new = max(0.0, min(old, float(new_energy)))
    freed = old - new
    bid["energy"] = new
    cs = bid["compute"] + bid["security"]
    if freed > 0.0:
        if cs > 1e-12:
            bid["compute"] += freed * bid["compute"] / cs
            bid["security"] += freed * bid["security"] / cs
        else:
            bid["compute"] += freed / 2.0
            bid["security"] += freed / 2.0
    total = sum(bid.values())
    if total > budget and total > 1e-12:
        bid = {k: v * budget / total for k, v in bid.items()}
    return bid

def decide_bid(
    budget: float,
    prices: Dict[str, float],
    capacities: Dict[str, float],
    profile: Dict[str, Any],
    history: List[Dict[str, Any]],
) -> Dict[str, float]:
    base = _market_floor_base(budget, prices, capacities, profile, history)
    battery = float((profile.get("features") or {}).get("battery", 1.0))
    battery = max(0.0, min(1.0, battery))
    keep = max(0.05, min(1.0, battery ** BATTERY_TAPER_ALPHA))
    bid = _redistribute_energy_cut(base, base["energy"] * keep, budget)
    others = _estimate_others(history)
    return _buy_floors(
        bid, budget, capacities,
        _floor_target(profile.get("q_min", 0.0), capacities.get("compute", 1.0)),
        _floor_target(profile.get("s_min", 0.0), capacities.get("security", 1.0)),
        others,
    )
