"""Markdown report generation for the VCM maturity assessment."""

from __future__ import annotations

from typing import Dict, Iterable, Mapping

from .initiatives import Initiative
from .questions import Pillar
from .scoring import PillarScore


def _format_pillar_section(
    pillar: Pillar, score: PillarScore, initiatives: Iterable[Initiative]
) -> str:
    lines = [f"## {pillar.name}", f"**Average score:** {score.average:.1f}"]

    if initiatives:
        lines.append("**Recommended initiatives:**")
        for item in initiatives:
            lines.append(f"- **{item.title}** — {item.description}")

    return "\n".join(lines)


def build_markdown_report(
    *,
    pillars: Iterable[Pillar],
    pillar_scores: Mapping[str, PillarScore],
    maturity_level: str,
    overall_score: float,
    value_at_stake: float | None,
    initiatives: Mapping[str, Iterable[Initiative]],
) -> str:
    """Create a markdown summary that can be downloaded from the UI."""

    sections = ["# Value-Centered Maturity Assessment", ""]
    sections.append(f"**Overall score:** {overall_score:.1f}")
    sections.append(f"**Maturity level:** {maturity_level}")

    if value_at_stake is not None:
        sections.append(f"**Estimated value at stake:** ₱{value_at_stake:,.0f} (PHP)")

    sections.append("\n---\n")

    for pillar in pillars:
        pillar_score = pillar_scores[pillar.id]
        pillar_initiatives = initiatives.get(pillar.id, [])
        sections.append(_format_pillar_section(pillar, pillar_score, pillar_initiatives))
        sections.append("")

    sections.append("\n---\n")
    sections.append("These recommendations are illustrative placeholders. Replace them with your organization's guidance before sharing broadly.")

    return "\n".join(sections)
