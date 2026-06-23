# Demo Outputs

These demo reports are generated from fictional sample workflows and do not
contain real client data.

## Included demo files

- `nextops_tutoring_demo_report.md` - Markdown diagnosis report generated from the fictional tutoring business sample workflow.
- `nextops_tutoring_demo_report.html` - HTML diagnosis report generated from the same fictional tutoring business sample workflow.

## Source

The source sample is `WF-001 - Tutoring business` from:

```text
data/sample_workflows.csv
```

The full local demo output set can be regenerated with:

```powershell
python scripts/generate_demo_assets.py
```

Generated bulk outputs are written to:

```text
outputs/demo_reports/
```

The `outputs/` folder remains ignored by Git except `outputs/.gitkeep`.

## Safety note

Do not include client data, private chats, emails, phone numbers, credentials,
payment information, or personal identifiers in this folder.
