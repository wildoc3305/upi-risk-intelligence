# Project Structure

```text
upi-risk-intelligence/
├── data/
│   ├── raw/          # Original datasets (not committed)
│   ├── processed/    # Cleaned/feature-ready datasets
│   └── README.md
├── notebooks/
│   ├── 01_data_overview.ipynb
│   ├── 02_eda.ipynb
│   └── 03_feature_engineering.ipynb
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── scoring/
│   └── api/
├── models/           # Saved model artifacts (local; ignored by git)
├── tests/
├── docs/
├── .gitignore
├── requirements.txt
└── README.md
```

The directory layout will grow as functionality is implemented.
