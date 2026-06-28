# NextOpsAgent

> NextOpsAgent is a local-first AI workflow diagnosis agent for SME operations.

NextOpsAgent turns a messy plain-language business workflow into automation
priorities, ROI estimates, implementation roadmaps, and downloadable
consultant-style reports. It is built as a GitHub portfolio showcase project
with transparent rule-based logic and no external AI API requirement.

## Current Status

**NEXT-OPS-007-GITHUB-PUBLIC-SHOWCASE**

This public showcase version includes:

- Product-style Streamlit dashboard
- Markdown and HTML report exports
- A small public demo output pair copied into `portfolio/demo_outputs/`
- Screenshot instructions prepared in `portfolio/showcase_screenshots/`
- Public release checklist and showcase manifest
- GitHub public repository published on `main`

GitHub About/topics, screenshots, and profile pin are still pending manual setup.

## Value proposition

Small teams often know that a workflow feels slow, manual, or scattered, but
they may not know what to automate first. NextOpsAgent converts vague
operational pain into a structured diagnosis:

- What steps are happening?
- Where are the bottlenecks?
- Which automation opportunities are strongest?
- What ROI range is reasonable for planning?
- What should the business do in the next 7, 30, and 90 days?
- What report can be shared as a demo-ready diagnosis?

## Core features

- Product-style Streamlit dashboard
- Five-tab workflow diagnosis interface
- Workflow parsing and evidence extraction
- Bottleneck diagnosis for common SME operations issues
- Explainable weighted automation scoring
- Configurable ROI estimate using business size, hourly cost, and frequency
- Structured 7-day, 30-day, and 90-day roadmap
- Markdown report preview and download
- HTML report download with escaped user-provided content
- Fictional sample workflows for safe public demos

## Target users

- Small business owners exploring workflow automation
- Operations consultants and automation consultants
- Local service businesses with manual admin work
- Agencies, tutoring teams, clinics, ecommerce operators, and real estate teams
- Portfolio reviewers who want to see local-first agent design without API keys

## Dashboard workflow

1. Choose a fictional sample workflow from the sidebar or paste a safe anonymised workflow.
2. Adjust business size, hourly cost, and workflow frequency assumptions.
3. Click `Analyze Workflow`.
4. Review:
   - `Overview` for workflow summary and evidence
   - `Diagnosis` for detected steps and bottlenecks
   - `Scores & ROI` for priority scores and planning estimates
   - `Roadmap` for 7/30/90-day actions
   - `Report` for Markdown preview plus Markdown and HTML downloads

## Showcase Preview

Screenshots are pending and should be captured manually before final README
image links are enabled.

Planned screenshots will be stored in:

```text
portfolio/showcase_screenshots/
```

Planned screenshot set:

- `01_home_hero.png` - hero, input center, and metric cards
- `02_overview_summary.png` - workflow summary and evidence snippets
- `03_bottleneck_diagnosis.png` - detected steps and bottleneck cards
- `04_scores_roi.png` - score table and ROI cards
- `05_roadmap.png` - 7-day, 30-day, and 90-day roadmap
- `06_report_preview.png` - Markdown and HTML report download area

Screenshot instructions are documented in:

```text
docs/SCREENSHOTS_GUIDE.md
portfolio/showcase_screenshots/README.md
```

## Demo Outputs

A small tutoring-business demo output pair is included for portfolio preview:

- [nextops_tutoring_demo_report.md](portfolio/demo_outputs/nextops_tutoring_demo_report.md)
- [nextops_tutoring_demo_report.html](portfolio/demo_outputs/nextops_tutoring_demo_report.html)

These demo reports are generated from fictional sample workflows and do not
contain real client data.

Bulk generated demo reports are written under:

```text
outputs/demo_reports/
```

The `outputs/` folder is ignored by Git except `outputs/.gitkeep`, so bulk local
reports are not accidentally included in the public repository.

## How to generate demo assets

```powershell
cd F:\AIProjects\NextOpsAgent
python scripts/generate_demo_assets.py
```

The script creates:

- `outputs/demo_reports/{workflow_id}_report.md`
- `outputs/demo_reports/{workflow_id}_report.html`
- `outputs/demo_reports/README.md`

## Example workflow

```text
A tutoring business receives parent enquiries through WeChat, email, and phone.
Staff copy lead details into Excel and manually follow up with each parent.
Some leads wait days for a reply, and the owner prepares a weekly report manually.
```

Expected signals include manual follow-up, manual data entry, delayed response,
and reporting effort.

## Tech stack

- Python 3.11+
- Streamlit
- pandas
- pytest

No OpenAI API, hosted model, database, scraper, or external integration is used
in the current release candidate.

## Project structure

```text
NextOpsAgent/
|-- app.py
|-- next_ops/
|   |-- workflow_parser.py
|   |-- bottleneck_detector.py
|   |-- automation_scorer.py
|   |-- roi_estimator.py
|   |-- roadmap_builder.py
|   |-- report_builder.py
|   |-- export_utils.py
|   `-- ui_helpers.py
|-- data/
|   `-- sample_workflows.csv
|-- docs/
|   |-- PROJECT_PLAN.md
|   |-- PUBLIC_RELEASE_CHECKLIST.md
|   |-- PUBLIC_SHOWCASE_MANIFEST.md
|   `-- SCREENSHOTS_GUIDE.md
|-- portfolio/
|   |-- demo_outputs/
|   `-- showcase_screenshots/
|-- scripts/
|   `-- generate_demo_assets.py
|-- outputs/
|   `-- .gitkeep
|-- tests/
|-- PROJECT_STATUS.md
|-- README.md
`-- requirements.txt
```

## How to run

```powershell
cd F:\AIProjects\NextOpsAgent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest
streamlit run app.py
python scripts/generate_demo_assets.py
```

Streamlit normally opens at:

```text
http://localhost:8501
```

## Testing

```powershell
python -m pytest
python -m compileall .
python scripts/generate_demo_assets.py
```

The UI can also be smoke-tested by starting Streamlit and confirming the local
HTTP endpoint returns `200 OK`.

## Safety Boundary

- Local-first
- No API key required
- No `.env` required
- No real client data
- No private chats, emails, phone numbers, payment information, or personal identifiers
- No automated external actions
- Educational and workflow planning use only
- Not legal, financial, cybersecurity, or professional operational advice

## MVP boundary

This project intentionally does not include:

- OpenAI API integration
- API keys or `.env` files
- Website scraping
- Real customer data
- Autonomous business actions
- CRM, email, calendar, payment, or database integrations
- Deployment

## Roadmap

- NEXT-OPS-002: complete - local skeleton and testable MVP baseline
- NEXT-OPS-003: complete - evidence-rich engine, explainable scores, configurable ROI, and structured roadmaps
- NEXT-OPS-004: complete - product-style Streamlit dashboard polish and screenshot guide
- NEXT-OPS-005: complete - report exports, demo asset generator, and public showcase docs
- NEXT-OPS-006: complete - local commit, demo outputs, and release preparation
- NEXT-OPS-007: public showcase - GitHub remote setup and public push completed
- NEXT-OPS-008: GitHub profile pin and final showcase check
- Future: optional, explicit LLM-assisted analysis with privacy controls
- Future: optional CRM, email, calendar, and reporting integrations with human approval

## Disclaimer

This project is for educational and workflow planning purposes only. It does not
replace professional operational, legal, financial, or cybersecurity advice.

## Managed through AgentHubControlCenter

This project is part of my local-first AI Agent portfolio and can be managed through [AgentHubControlCenter](https://github.com/CHENXJC/AgentHubControlCenter), the central command center for agent manifests, safe actions, useful signals, workflow simulations, connector readiness, approval gates, and public-safe reporting.

NextOpsAgent is registered as an SME next-action recommendation module in AgentHubControlCenter.
