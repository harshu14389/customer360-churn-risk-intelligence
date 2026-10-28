# Project guide

## Business case
A retention analyst reviews customers with declining usage or unresolved support issues. The score ranks risk; rules suggest a follow-up hypothesis. Track outcomes through a controlled experiment before asserting impact.

## Prediction boundary
At the end of the snapshot date, predict cancellation in the following 90 days. Only features available by that date may be used. Training snapshots are June and December 2024; test is June 2025, with a gap ensuring every training label is mature. Each synthetic customer appears once. This is a temporal evaluation of generated data, not evidence of performance on real customers. No current-production scoring or calibration is implemented.

## Data dictionary
- customer_id: fictional unique identifier; snapshot_date: feature cutoff; signup_date: approximate synthetic date; segment, region, plan: simulated attributes.
- tenure_months: simulated months; activity_previous_30d and activity_last_30d: counts for successive windows; usage_trend: difference divided by max(previous, 1).
- days_since_activity: simulated days; tickets_last_90d: ticket count; unresolved_tickets: count unresolved at cutoff; spend_last_90d: simulated currency units.
- churn_next_90d: simulated binary cancellation outcome in the next 90 days; label_window_end: date labels become observable. Labels are excluded from the score export.
- risk_score: logistic model output; action_category and action_rule: deterministic suggestions, not causal predictions.

The individual input features are generated directly and are not reconstructed from event records. Some generated fields need not be internally realistic. There are no real people, actual cancellations, privacy-sensitive fields, or real monetary amounts.

## Evaluation
The test is the latest snapshot. Compare ROC-AUC, average precision and Brier score with the prevalence baseline. Average precision baseline equals test-set prevalence; Brier baseline uses training prevalence. Coefficients describe model associations after scaling, not causal effects or customer-specific explanations. Action rules do not depend on the score threshold and have not been tested. A real implementation needs event-time validation, cohort drift checks, missingness, calibration, fair-use review, and customer-level leakage checks.

## Next build
Generate or obtain separate dated purchase, activity, support, subscription and feedback records; derive features with SQL at each cutoff, check reconciliation and prevent future events leaking into features. Then validate supported SAP import and SAC connection options in your own environment. See SAP_GUIDE.md.

## Experiment idea
Among eligible customers, randomly assign a support/education follow-up or the usual process. Measure 90-day churn and response rates, document sample size, consent and limitations, and compare outcomes by group. This is a proposal, not evidence of effect.
