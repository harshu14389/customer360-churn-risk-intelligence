from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs'
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(42)
n = 6000
# Distinct synthetic customers at three historical observation dates.
dates = pd.to_datetime(rng.choice(['2024-06-30', '2024-12-31', '2025-06-30'], n))
tenure = rng.integers(2, 49, n)
previous = rng.poisson(15, n)
current = np.maximum(0, np.round(previous * rng.uniform(.1, 1.6, n))).astype(int)
tickets = rng.poisson(1.2, n)
unresolved = np.array([rng.binomial(x, .35) for x in tickets])
spend = np.round(rng.uniform(10, 150, n), 2)
recency = np.minimum(90, rng.geometric(.08, n))
trend = (current - previous) / np.maximum(previous, 1)
# Simulated labels are generated after snapshot; patterns are assumptions, not real findings.
logit = -2.4 - .9 * np.clip(trend, -1, 1) + .32 * unresolved + .015 * recency - .008 * tenure
prob = 1 / (1 + np.exp(-logit))
labels = rng.binomial(1, prob)
df = pd.DataFrame({'customer_id': ['C%05d' % i for i in range(1,n+1)], 'snapshot_date': dates, 'signup_date': dates - pd.to_timedelta(tenure*30, unit='D'), 'segment': rng.choice(['Consumer','Small Business','Enterprise'], n), 'region': rng.choice(['North','South','East','West'], n), 'plan': rng.choice(['Basic','Plus','Premium'], n), 'tenure_months': tenure, 'activity_previous_30d': previous, 'activity_last_30d': current, 'usage_trend': trend, 'days_since_activity': recency, 'tickets_last_90d': tickets, 'unresolved_tickets': unresolved, 'spend_last_90d': spend, 'churn_next_90d': labels})
# Placeholder synthetic source snapshots, with precomputed features, not raw event histories.
df['label_window_end'] = df.snapshot_date + pd.Timedelta(days=90)
features = ['tenure_months','activity_previous_30d','activity_last_30d','usage_trend','days_since_activity','tickets_last_90d','unresolved_tickets','spend_last_90d']
train = df.snapshot_date < pd.Timestamp('2025-06-30')
test = ~train
assert df.customer_id.is_unique and (df.signup_date <= df.snapshot_date).all()
assert df.loc[train, 'label_window_end'].max() < df.loc[test, 'snapshot_date'].min()
assert (df.unresolved_tickets <= df.tickets_last_90d).all()
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=42))
model.fit(df.loc[train, features], df.loc[train, 'churn_next_90d'])
pred = model.predict_proba(df.loc[test, features])[:,1]
y = df.loc[test, 'churn_next_90d']
base = float(df.loc[train, 'churn_next_90d'].mean())
metrics = {'training_rows': int(train.sum()), 'test_rows': int(test.sum()), 'train_through': '2024-12-31', 'test_snapshot': '2025-06-30', 'test_churn_rate': float(y.mean()), 'model_roc_auc': float(roc_auc_score(y,pred)), 'model_average_precision': float(average_precision_score(y,pred)), 'baseline_average_precision': float(y.mean()), 'model_brier': float(brier_score_loss(y,pred)), 'baseline_brier': float(brier_score_loss(y,np.full(len(y),base))), 'baseline': 'constant training-set churn prevalence'}
test_df = df.loc[test].copy()
test_df['risk_score'] = pred.round(4)
test_df['action_category'] = np.select([(test_df.usage_trend < -.3) & (test_df.unresolved_tickets > 0),test_df.unresolved_tickets > 0,test_df.usage_trend < -.3],['Support and usage follow-up','Support follow-up','Product education'],default='Routine check-in')
test_df['action_rule'] = np.select([(test_df.usage_trend < -.3) & (test_df.unresolved_tickets > 0),test_df.unresolved_tickets > 0,test_df.usage_trend < -.3],['Usage down over 30% and unresolved ticket','At least one unresolved ticket','Usage down over 30%'],default='No priority rule triggered')
df.to_csv(OUT / 'synthetic_customer_snapshots.csv', index=False)
test_df.drop(columns=['churn_next_90d','label_window_end']).to_csv(OUT / 'customer_scores_test.csv', index=False)
with open(OUT / 'evaluation.json','w') as f: json.dump(metrics,f,indent=2)
coef = pd.DataFrame({'feature': features, 'standardized_logistic_coefficient': model.named_steps['logisticregression'].coef_[0]})
coef.to_csv(OUT / 'model_coefficients.csv',index=False)
print(json.dumps(metrics, indent=2))
print('Checks passed. Files saved in outputs/. Synthetic data only.')
