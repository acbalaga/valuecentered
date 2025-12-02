"""Streamlit UI for the Value-Centered Maturity assessment."""

from __future__ import annotations

from typing import Dict, Tuple

import pandas as pd
import streamlit as st

from vcm_logic import (
    Pillar,
    compute_maturity_level,
    get_pillars,
    get_top_initiatives,
    overall_average,
    score_responses,
)
from vcm_logic.initiatives import Initiative
from vcm_logic.report_builder import build_markdown_report
from vcm_logic.scoring import PillarScore


st.set_page_config(page_title="VCM Maturity", page_icon="📈", layout="wide")


def _init_session() -> None:
    """Ensure session-scoped storage exists for calculations and answers."""

    if "results" not in st.session_state:
        st.session_state.results = None


def _collect_answers(pillars: list[Pillar]) -> Dict[str, str]:
    """Read question answers from the Streamlit widget state."""

    answers: Dict[str, str] = {}
    for pillar in pillars:
        for question in pillar.questions:
            answers[question.id] = st.session_state[f"resp_{question.id}"]
    return answers


def _render_questions(pillars: list[Pillar]) -> Tuple[bool, float | None]:
    """Render the questionnaire form and capture submission state."""

    with st.form("assessment_form", clear_on_submit=False):
        st.markdown("## Maturity questions")
        for pillar in pillars:
            with st.expander(f"{pillar.name}: {pillar.description}", expanded=True):
                for question in pillar.questions:
                    st.radio(
                        question.prompt,
                        options=list(question.options),
                        index=0,
                        key=f"resp_{question.id}",
                        horizontal=False,
                    )

        value_input = st.number_input(
            "Optional value-at-stake estimate ($)",
            min_value=0.0,
            step=100000.0,
            key="value_input",
            help=(
                "Enter a rough estimate of the potential financial upside. "
                "This is session-only and not persisted."
            ),
        )

        submitted = st.form_submit_button("Calculate maturity")

    value_at_stake = value_input if value_input > 0 else None
    return submitted, value_at_stake


def _calculate_results(pillars: list[Pillar], value_at_stake: float | None) -> None:
    """Score responses, derive initiatives, and cache results in session state."""

    answers = _collect_answers(pillars)
    pillar_scores = score_responses(answers, pillars)
    overall_score = overall_average(pillar_scores)
    maturity_level = compute_maturity_level(overall_score)

    initiatives: Dict[str, list[Initiative]] = {}
    for pillar in pillars:
        initiatives[pillar.id] = get_top_initiatives(
            pillar_id=pillar.id, score=pillar_scores[pillar.id].average
        )

    st.session_state.results = {
        "pillar_scores": pillar_scores,
        "overall_score": overall_score,
        "maturity_level": maturity_level,
        "initiatives": initiatives,
        "value_at_stake": value_at_stake,
    }


def _pillar_score_chart(pillars: list[Pillar], pillar_scores: Dict[str, PillarScore]) -> None:
    """Display a bar chart of scores by pillar."""

    data = pd.DataFrame(
        {
            "Pillar": [pillar.name for pillar in pillars],
            "Average score": [pillar_scores[pillar.id].average for pillar in pillars],
        }
    )
    st.bar_chart(data.set_index("Pillar"))


def _render_pillar_details(
    pillars: list[Pillar],
    pillar_scores: Dict[str, PillarScore],
    initiatives: Dict[str, list[Initiative]],
) -> None:
    """Show per-pillar scores and recommended initiatives."""

    for pillar in pillars:
        with st.expander(pillar.name, expanded=False):
            st.markdown(f"**Description:** {pillar.description}")
            st.markdown(f"**Average score:** {pillar_scores[pillar.id].average:.1f}")
            st.markdown("**Recommended initiatives:**")
            if initiatives[pillar.id]:
                for item in initiatives[pillar.id]:
                    st.markdown(f"- **{item.title}** — {item.description}")
            else:
                st.info("No initiatives configured for this score band yet.")


def _render_results(pillars: list[Pillar]) -> None:
    """Render the results section if calculations exist."""

    if not st.session_state.results:
        return

    results = st.session_state.results
    pillar_scores: Dict[str, PillarScore] = results["pillar_scores"]

    st.success(
        f"Overall score: {results['overall_score']:.1f} — Maturity level: {results['maturity_level']}"
    )

    if results["value_at_stake"] is not None:
        st.markdown(f"**Estimated value at stake:** ${results['value_at_stake']:,.0f}")

    _pillar_score_chart(pillars, pillar_scores)
    _render_pillar_details(pillars, pillar_scores, results["initiatives"])

    report_md = build_markdown_report(
        pillars=pillars,
        pillar_scores=pillar_scores,
        maturity_level=results["maturity_level"],
        overall_score=results["overall_score"],
        value_at_stake=results["value_at_stake"],
        initiatives=results["initiatives"],
    )
    st.download_button(
        "Download markdown report", data=report_md, file_name="vcm_assessment.md"
    )


def main() -> None:
    """Entry point for the Streamlit application."""

    _init_session()
    st.title("Value-Centered Maturity (VCM) Assessment")
    st.markdown(
        "Use this questionnaire to gauge your organization's maturity across key value pillars. "
        "All inputs stay within your session; nothing is persisted."
    )

    pillars = get_pillars()
    submitted, value_at_stake = _render_questions(pillars)

    if submitted:
        _calculate_results(pillars, value_at_stake)

    # Results render once available; avoids showing empty placeholders.
    _render_results(pillars)


if __name__ == "__main__":
    main()
