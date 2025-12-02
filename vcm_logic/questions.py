"""Question and pillar definitions for the VCM maturity assessment.

The prompts and pillars below are intentionally lightweight placeholders.
Replace them with domain-specific content when institutional guidance is
available.
"""

from dataclasses import dataclass
from typing import List, Sequence, Tuple


@dataclass(frozen=True)
class Question:
    """Represents a maturity question with pre-defined answer options."""

    id: str
    prompt: str
    options: Sequence[str]


@dataclass(frozen=True)
class Pillar:
    """Grouping of related questions for a maturity pillar."""

    id: str
    name: str
    description: str
    questions: List[Question]


def _default_options() -> List[str]:
    """Shared answer options across all questions.

    Using consistent options simplifies scoring and comparison across pillars.
    """

    return [
        "Not started",
        "Ad hoc or limited",
        "Defined and repeatable",
        "Managed with metrics",
        "Optimized and automated",
    ]


def option_explanations() -> List[Tuple[str, str]]:
    """Provide short guidance for each maturity choice.

    The narratives are intentionally concise placeholders so teams can
    substitute domain-specific language later without changing the UI layer.
    """

    return [
        (
            "Not started",
            "No consistent approach exists yet; activities are mostly informal.",
        ),
        (
            "Ad hoc or limited",
            "Some individual efforts happen but they are not coordinated or measured.",
        ),
        (
            "Defined and repeatable",
            "Processes are documented and followed with basic governance in place.",
        ),
        (
            "Managed with metrics",
            "Execution is tracked with quantitative measures and corrective actions.",
        ),
        (
            "Optimized and automated",
            "Practices are continuously improved, automated where possible, and scaled.",
        ),
    ]


def get_pillars() -> List[Pillar]:
    """Return the set of maturity pillars and their questions.

    The structure is intentionally data-driven to keep UI rendering simple.
    Update the questions here to evolve the assessment without touching UI code.
    """

    options = _default_options()

    return [
        Pillar(
            id="strategy",
            name="Strategy",
            description="How clearly the organization aligns value goals with execution.",
            questions=[
                Question(
                    id="strategy_alignment",
                    prompt="Value objectives are clearly articulated and communicated across teams.",
                    options=options,
                ),
                Question(
                    id="strategy_prioritization",
                    prompt="Initiatives are prioritized based on measurable impact and feasibility.",
                    options=options,
                ),
            ],
        ),
        Pillar(
            id="data",
            name="Data & Tooling",
            description="Readiness of data, models, and platforms supporting decisions.",
            questions=[
                Question(
                    id="data_quality",
                    prompt="Operational and financial data is trustworthy and regularly validated.",
                    options=options,
                ),
                Question(
                    id="tooling_modern",
                    prompt="Analytics and decision-support tooling are modern, scalable, and well adopted.",
                    options=options,
                ),
            ],
        ),
        Pillar(
            id="execution",
            name="Execution",
            description="Discipline around delivering initiatives and measuring outcomes.",
            questions=[
                Question(
                    id="execution_delivery",
                    prompt="Projects are delivered predictably with clear ownership and timelines.",
                    options=options,
                ),
                Question(
                    id="execution_measurement",
                    prompt="Benefits are tracked post-launch with feedback loops to improve future work.",
                    options=options,
                ),
            ],
        ),
        Pillar(
            id="culture",
            name="Culture & Change",
            description="Engagement, incentives, and behaviors that sustain value-centric thinking.",
            questions=[
                Question(
                    id="culture_adoption",
                    prompt="Teams embrace value-centric decision making in daily routines.",
                    options=options,
                ),
                Question(
                    id="culture_training",
                    prompt="Enablement programs build literacy in data, finance, and change management.",
                    options=options,
                ),
            ],
        ),
    ]
