# Customer 360, Churn Prediction & Next-Best-Action

A standalone synthetic customer analytics prototype for a subscription business. It ranks customers by estimated probability of cancellation in the next 90 days and suggests rule-based follow-up categories for human review. Actions are hypotheses, not personalised treatment effects.

Start with START_HERE_WINDOWS.md. Run the script to generate reproducible snapshots, a chronological holdout evaluation, scores and coefficients. Requirements are ranges; results may differ slightly across package versions.

Data flow: synthetic customer snapshots → feature checks → logistic regression → holdout scores and rules → planned Datasphere and SAC build. No SAP deployment or connection is claimed. SAP SQL in this starter is a draft to adapt and validate in your tenant.

The generator creates pre-aggregated snapshots, not transactional event data. Therefore the SQL is a starting point for these snapshot exports, not a demonstrated multi-fact customer 360 integration. The later build needs separately timestamped purchase, usage and support tables. See docs/PROJECT_GUIDE.md.

The reported results are from intentionally generated data with known simulated relationships. They do not demonstrate real-world performance. Scores are uncalibrated and should not be used to make real customer decisions. Do not put real personal data into this demo.
