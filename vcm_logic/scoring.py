"""Scoring helpers for the VCM maturity assessment."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Mapping

from .questions import Pillar, Question


@dataclass(frozen=True)
class PillarScore:
    """Aggregated score for a single pillar."""

    pillar_id: str
    average: float
    responses: Dict[str, int]


def _option_to_score(option: str, question: Question) -> int:
    """Convert an answer option to a numeric score.

    The scoring is ordinal: the first option scores 1, the last scores 5.
    Raise a clear error if the option is unexpected to keep UI/logic in sync.
    """

    try:
        position = question.options.index(option)
    except ValueError as exc:
        raise ValueError(f"Unknown option '{option}' for question {question.id}") from exc
    return position + 1


def score_responses(
    answers: Mapping[str, str], pillars: Iterable[Pillar]
) -> Dict[str, PillarScore]:
    """Compute per-pillar scores from raw answers.

    The function assumes answers cover every question presented in the UI.
    Missing answers would raise a KeyError to avoid silently under-scoring.
    """

    pillar_scores: Dict[str, PillarScore] = {}
    for pillar in pillars:
        numeric_responses: Dict[str, int] = {}
        for question in pillar.questions:
            option = answers[question.id]
            numeric_responses[question.id] = _option_to_score(option, question)

        average_score = sum(numeric_responses.values()) / len(numeric_responses)
        pillar_scores[pillar.id] = PillarScore(
            pillar_id=pillar.id, average=average_score, responses=numeric_responses
        )

    return pillar_scores


def compute_maturity_level(overall_score: float) -> str:
    """Translate an overall numeric score into a maturity level label."""

    if overall_score < 2:
        return "Nascent"
    if overall_score < 3:
        return "Emerging"
    if overall_score < 4:
        return "Established"
    return "Leading"


def overall_average(pillar_scores: Mapping[str, PillarScore]) -> float:
    """Calculate the overall average score across pillars."""

    if not pillar_scores:
        return 0.0
    return sum(score.average for score in pillar_scores.values()) / len(pillar_scores)
