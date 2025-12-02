"""Initiative suggestions keyed by pillar and maturity band.

The content is illustrative; replace with organization-specific playbooks when
available.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Mapping, Sequence, Tuple


@dataclass(frozen=True)
class Initiative:
    """A concise initiative recommendation."""

    title: str
    description: str


# Score bands are inclusive of the lower bound and exclusive of the upper bound.
BANDS: Tuple[Tuple[float, float], ...] = (
    (0, 2.0),
    (2.0, 3.0),
    (3.0, 4.0),
    (4.0, 5.1),  # allow slight rounding over 5
)

# Placeholder initiatives. Tailor these to the organization's capabilities and priorities.
_INITIATIVES: Mapping[str, Mapping[Tuple[float, float], Sequence[Initiative]]] = {
    "strategy": {
        BANDS[0]: [
            Initiative(
                title="Define value north star",
                description="Document 3-5 measurable value outcomes and circulate them across leadership.",
            ),
            Initiative(
                title="Decision cadence",
                description="Establish a monthly forum to prioritize work by value and risk.",
            ),
        ],
        BANDS[1]: [
            Initiative(
                title="Roadmap by value",
                description="Score backlog items by impact vs. effort and publish a quarterly roadmap.",
            ),
        ],
        BANDS[2]: [
            Initiative(
                title="KPIs with ownership",
                description="Assign accountable owners for value KPIs and track progress in a shared dashboard.",
            ),
        ],
        BANDS[3]: [
            Initiative(
                title="Adaptive capital allocation",
                description="Rebalance funding each quarter based on realized benefits and new opportunities.",
            ),
        ],
    },
    "data": {
        BANDS[0]: [
            Initiative(
                title="Data inventory",
                description="List critical datasets, owners, and known gaps to inform remediation priorities.",
            ),
        ],
        BANDS[1]: [
            Initiative(
                title="Quality baselines",
                description="Implement basic data quality checks on the most used tables or reports.",
            ),
            Initiative(
                title="Tooling uplift",
                description="Pilot a modern analytics stack with one high-value use case.",
            ),
        ],
        BANDS[2]: [
            Initiative(
                title="Model governance",
                description="Introduce versioning, testing, and monitoring for key analytical models.",
            ),
        ],
        BANDS[3]: [
            Initiative(
                title="Self-service enablement",
                description="Broaden governed data access and training for power users across teams.",
            ),
        ],
    },
    "execution": {
        BANDS[0]: [
            Initiative(
                title="Delivery playbook",
                description="Standardize intake templates, stage gates, and RACI to reduce ambiguity.",
            ),
        ],
        BANDS[1]: [
            Initiative(
                title="Pilot value tracking",
                description="Run a small project with explicit benefit hypotheses and simple tracking.",
            ),
        ],
        BANDS[2]: [
            Initiative(
                title="Benefits realization",
                description="Embed benefit tracking into project close-out and post-launch reviews.",
            ),
        ],
        BANDS[3]: [
            Initiative(
                title="Portfolio optimization",
                description="Continuously reprioritize initiatives based on realized vs. forecast benefits.",
            ),
        ],
    },
    "culture": {
        BANDS[0]: [
            Initiative(
                title="Narrative for change",
                description="Share success stories linking value outcomes to daily work to build momentum.",
            ),
        ],
        BANDS[1]: [
            Initiative(
                title="Targeted enablement",
                description="Offer short trainings on value framing, data literacy, and change management.",
            ),
        ],
        BANDS[2]: [
            Initiative(
                title="Incentives alignment",
                description="Align performance goals and recognition with value-centric behaviors.",
            ),
        ],
        BANDS[3]: [
            Initiative(
                title="Communities of practice",
                description="Sustain peer-led forums to share learnings and continuously improve.",
            ),
        ],
    },
}


def _band_for_score(score: float) -> Tuple[float, float]:
    for band in BANDS:
        lower, upper = band
        if lower <= score < upper:
            return band
    return BANDS[-1]


def get_top_initiatives(pillar_id: str, score: float, limit: int = 3) -> List[Initiative]:
    """Return initiative ideas for the pillar that match the given score.

    The recommendations are intentionally capped to avoid overwhelming readers.
    """

    pillar_bands = _INITIATIVES.get(pillar_id, {})
    band = _band_for_score(score)
    initiatives = pillar_bands.get(band, [])
    return list(initiatives[:limit])
