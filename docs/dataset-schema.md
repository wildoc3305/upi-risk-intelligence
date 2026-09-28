# Dataset Schema

This document defines the **initial logical schema** for the project. It is intentionally separated from a specific dataset so that the repository can adapt to a public or synthetic source without hiding assumptions.

## Core transaction fields

| Field | Type | Role |
|---|---|---|
| transaction_id | string | Unique transaction identifier |
| timestamp | datetime | Transaction time |
| amount | numeric | Transaction amount |
| sender_id | string | Sender/account identifier |
| receiver_id | string | Receiver/payee identifier |
| merchant_category | categorical | Merchant/payee category |
| device_id | string | Device identifier |
| location | categorical/geospatial | Transaction location or region |
| is_fraud | binary | Target label: 1 = fraudulent, 0 = legitimate |

## Behavioral fields

Depending on dataset availability, the pipeline may also use:

- transactions per user over a time window
- time since previous transaction
- deviation from a user's typical transaction amount
- new-device indicator
- new-payee indicator
- transaction velocity
- historical risk/fraud indicators

## Important distinction

The final implementation must use the **actual columns provided by the selected dataset**. Fields listed above are a project-level schema and are not a claim that every source dataset contains all of them.
