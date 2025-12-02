# VCM Value Lab

VCM Value Lab is a Streamlit application that guides teams through a Value-Centered Maintenance (VCM) maturity assessment. It helps surface where an organization stands today, which initiatives to pursue next, and how to communicate recommendations in a lightweight report.

## Purpose
- **Maturity focus:** Evaluate maintenance maturity across Strategy, Data & Tooling, Execution, and Culture & Change pillars.
- **Value orientation:** Frame findings around value creation by linking scores to potential initiatives and optional value-at-stake estimates.
- **Decision support:** Provide a transparent, repeatable flow teams can run together or asynchronously.

## How it works
1. **Answer questions:** Respond to predefined prompts under each pillar using consistent ordinal options (Not started → Optimized and automated).
2. **Score the responses:** The app converts options to numeric scores, rolls them up per pillar, and computes an overall maturity level.
3. **Recommend initiatives:** Each pillar’s score maps to a small set of initiative ideas to advance maturity.
4. **Download the report:** A markdown summary captures scores, maturity level, and initiatives for sharing or further editing.

## Privacy
- Inputs are session-scoped only; nothing is persisted on the server.
- Optional value-at-stake entries remain in-memory and are not stored externally.

## Attribution
The app operationalizes the Value-Centered Maintenance (VCM) framework. Replace the placeholder questions and initiative ideas in `vcm_logic/questions.py` and `vcm_logic/initiatives.py` with organization-specific guidance as it becomes available.

## Local development
1. Create and activate a virtual environment (recommended).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
4. Open the provided local URL in your browser to interact with the assessment.

## Deployment
The app runs on [Streamlit Community Cloud](https://streamlit.io/cloud) without extra configuration. Point the deployment at this repository, and set the entrypoint to `app.py`.

## Repository structure
- `app.py`: Streamlit UI that collects answers, calculates scores, and renders results/downloads.
- `vcm_logic/questions.py`: Pillar and question definitions with shared options.
- `vcm_logic/scoring.py`: Helpers to translate options into scores and derive maturity levels.
- `vcm_logic/initiatives.py`: Initiative suggestions grouped by pillar and score bands.
- `vcm_logic/report_builder.py`: Markdown report generator used by the download button.
- `requirements.txt`: Python dependencies required to run the app.
