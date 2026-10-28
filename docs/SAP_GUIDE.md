# SAP implementation plan — not yet deployed

1. After running the script, inspect outputs/synthetic_customer_snapshots.csv and customer_scores_test.csv. Labels exist only in the first file; avoid exposing future outcomes to the scoring view.
2. In Datasphere, confirm your space and CSV import options. Import the snapshot and score files as separate local tables if supported. Customer ID is unique in these synthetic exports; for a real recurring snapshot, use customer ID plus snapshot date as the key. Check data types and row counts.
3. Build a customer/snapshot view and a separate score/action view, then join on customer ID and snapshot date with a verified one-to-one relationship. Do not include outcome labels in a live scoring view. Put matured outcomes in a separate restricted evaluation view.
4. This starter does not yet provide separate purchase, support, activity or subscription fact tables. Create timestamped facts and dimensions as a subsequent phase, and validate no event after the cutoff enters features. Document refresh, access and reconciliation.
5. Check whether your tenant supports the desired analytic model and SAC connection. Use a supported import/export if direct connection is unavailable; document the actual route. Validate row counts and measures before building visuals.
6. Create SAC pages: customer overview, risk distribution, signals and action categories. Label synthetic data and model date. Use aggregated views and restrict individual records. Do not claim action effectiveness.
7. Export your own screenshots and record actual configuration and checks. Do not represent the starter as SAP deployment evidence.
