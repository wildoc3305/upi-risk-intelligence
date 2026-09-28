# UPI Risk Intelligence

> An AI-powered framework for detecting suspicious UPI transactions and communicating transaction risk in a user- and analyst-friendly way.

[![Status](https://img.shields.io/badge/status-in%20development-orange)](https://github.com/wildoc3305/upi-risk-intelligence)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![ML](https://img.shields.io/badge/ML-scikit--learn-yellow)](https://scikit-learn.org/)
[![Backend](https://img.shields.io/badge/API-FastAPI-009688)](https://fastapi.tiangolo.com/)

## Project overview

UPI Risk Intelligence is a portfolio and academic project focused on transaction-risk detection for UPI-style digital payments.

The goal is to build an end-to-end risk intelligence pipeline that can:

- preprocess transaction data
- engineer behavioral and transaction-risk features
- train and evaluate fraud/risk detection models
- convert model outputs into an understandable risk score and risk level
- provide explanations for flagged transactions
- expose the scoring system through an API
- present different information to payment users and risk analysts

The project is being developed incrementally so that the Git history documents the reasoning, experiments, implementation, and improvements.

## Planned architecture

```text
Transaction
    |
    v
Data Validation
    |
    v
Preprocessing
    |
    v
Feature Engineering
    |
    v
ML Risk Model
    |
    v
Risk Probability
    |
    v
Risk Score + Risk Level
    |
    +--------------------+
    |                    |
    v                    v
User Alert         Analyst Dashboard
    |
    v
Decision / Action
```

The supporting project report describes a modular architecture with real-time monitoring, low-latency inference, layered defenses, and separate user/admin-oriented components.

## Repository roadmap

| Phase | Focus |
|---|---|
| 1 | Project structure and documentation |
| 2 | Dataset and preprocessing |
| 3 | Exploratory data analysis |
| 4 | Feature engineering |
| 5 | Baseline and advanced ML models |
| 6 | Model evaluation |
| 7 | Risk scoring and explainability |
| 8 | FastAPI inference service |
| 9 | User and analyst interface |
| 10 | Fraud simulation and deployment |

## Current status

**Day 1 — Repository foundation**

Completed:
- project positioning and scope
- initial architecture
- development roadmap
- repository documentation baseline

Next:
- establish the ML project structure
- document the dataset schema
- add reproducible environment/dependency setup

## Important note

This repository is a research/academic prototype. It is not a production UPI security service and does not connect to live payment rails.

## License

License to be added once the project scope and contribution model are finalized.
