# Dataset Contract

## Purpose

The dataset layer provides a stable contract between raw transaction data and the ML pipeline.

### Required outcome

A selected dataset must provide:

1. A transaction-level record.
2. A binary fraud/risk target, or enough information to construct one responsibly.
3. Features that can support transaction and/or behavioral risk analysis.
4. A documented source and license/usage condition.

### Validation rules

The ingestion workflow should check:

- file exists and is readable
- expected columns are present
- target values are valid
- transaction identifiers are not unexpectedly duplicated
- numeric fields contain parseable values
- timestamps can be parsed when supplied
- missing-value counts are reported
- class distribution is reported before modeling

### Data leakage guardrail

Features that directly reveal the target or depend on future information must not be used as model inputs.

### Privacy guardrail

Do not commit real financial records, personally identifiable information, payment credentials, or private customer data.
