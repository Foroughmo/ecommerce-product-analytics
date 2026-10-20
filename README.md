# E-commerce Product Analytics & Experimentation

A product data science case study connecting conversion-funnel analysis, A/B test design, and uplift modeling to product and advertising decisions.

**[Explore the Streamlit report](https://ecommerce-appuct-analytics-k3rcqkx59s8qbgt7f7yhqf.streamlit.app/)**

## Business questions

- Where do shoppers drop off between viewing a product and purchasing?
- Could clearer shipping and return information improve purchase conversion?
- Does advertising increase conversion, and can a model identify users with a larger incremental response?

The project uses two independent datasets. **GA4 supports product analysis and a proposed product-page experiment. Criteo supports a separate advertising experiment analysis and uplift model.** The Criteo results do not evaluate the proposed GA4 change.

## Key findings

### Product analytics: the largest drop-off occurs before cart addition

An ordered, session-level funnel tracks **product view → add to cart → checkout → purchase**. Only **17.88%–18.93%** of product-view sessions reach the cart across devices.

| Device | Product-view sessions | View-to-cart rate | Full-funnel purchase sessions | Journey completion rate |
| --- | ---: | ---: | ---: | ---: |
| Desktop | 44,819 | 18.53% | 1,567 | 3.50% |
| Mobile | 30,501 | 18.93% | 1,150 | 3.77% |
| Tablet | 1,700 | 17.88% | 61 | 3.59% |

**Recommendation:** Test clearer shipping estimates and return information near **Add to Cart** for first-time product viewers. The funnel identifies an opportunity for investigation; it does not establish shipping or return uncertainty as the cause of drop-off.

### Experiment design: a proposed test of clearer product-page information

| Design component | Specification |
| --- | --- |
| Status | Proposed; not run |
| Eligible population | First-time visitors who view a product |
| Control / treatment | Current page / clearer shipping and return information near Add to Cart |
| Randomization | User-level, 50/50 allocation; persistent assignment |
| Primary metric | Purchase conversion among assigned users |
| Planning baseline | 3.36%: 1,713 purchasers among 50,940 eligible users |
| Minimum detectable effect | 20% relative lift: 3.36% → 4.032%, or +0.672 percentage points |
| Statistical settings | Two-sided test; α = 0.05; 80% power |
| Required sample | 24,696 users total; 12,348 per group |
| Enrollment estimate | Approximately 45 days at 553.6 eligible users per day, plus purchase follow-up |

### Advertising experiment: a positive overall conversion difference

The Criteo analysis compares users by treatment assignment, regardless of actual ad exposure: an **intention-to-treat** comparison.

| Metric | Result |
| --- | ---: |
| Sample | 1,000,000 users |
| Control conversion | 0.1876% |
| Treatment conversion | 0.2988% |
| Absolute lift | +0.1112 percentage points |
| Relative lift | +59.3% |
| 95% confidence interval for absolute lift | +0.0864 to +0.1360 percentage points |
| Two-sided two-proportion z-test p-value | Approximately 7.24 × 10⁻¹⁴ |

The difference corresponds to approximately **111 incremental conversions per 100,000 users assigned to treatment** (95% CI: approximately 86–136).

**Business decision:** Statistical significance alone does not justify rollout. Validate the effect in production, then assess whether incremental contribution exceeds campaign costs and meets the business return threshold while maintaining guardrails. Campaign costs and contribution margins are unavailable in this analysis, so profitability remains unresolved.

### Uplift modeling: evaluating a candidate targeting segment

A **T-learner** fits separate logistic regressions for treatment and control users using 12 anonymized numeric features. Both models predict conversion for each test user; the difference between those predictions determines the predicted-uplift ranking.

- **Training / test split:** 700,000 / 300,000 users, jointly stratified by treatment assignment and conversion.
- **Preprocessing:** Separate StandardScaler pipelines fitted on training data only.
- **Selection:** Highest predicted-uplift decile: 30,000 test users.
- **Evaluation:** Observed treatment–control conversion difference within the selected segment.

| Top-decile metric | Result |
| --- | ---: |
| Control conversion | 1.6793% |
| Treatment conversion | 2.5027% |
| Observed lift | +0.8234 percentage points |
| 95% confidence interval | +0.3917 to +1.2552 percentage points |
| Two-sided two-proportion z-test p-value | Approximately 0.00115 |

**Recommendation:** Evaluate this segment in a follow-up targeting experiment. The within-segment result does not establish that its effect is significantly greater than other users' effects, that the 10% cutoff is optimal, or that targeting improves profitability. Model or cutoff changes informed by these results require fresh evaluation data.

## Data and methodology

| Dataset | Role | Scope |
| --- | --- | --- |
| [Google GA4 sample e-commerce data](https://developers.google.com/analytics/bigquery/web-ecommerce-demo-dataset) | Shopping behavior, funnel analysis, and experiment planning | Google Merchandise Store events analyzed in BigQuery |
| [Criteo uplift dataset](https://huggingface.co/datasets/criteo/criteo-uplift) | Advertising experiment analysis and uplift modeling | Reproducible 1-million-user sample of the public benchmark; sampling seed 42 |

**Funnel definition:** Events must occur strictly in order within the same user/session. Steps may involve different products. Journey completion is full-funnel purchase sessions divided by product-view sessions; it is not the overall store purchase conversion rate.

**Statistical inference:** Treatment–control rate differences use two-sided two-proportion z-tests and approximate 95% confidence intervals with unpooled standard errors. Rates and interval endpoints displayed in the report are rounded.

**Criteo limitation:** The public data was non-uniformly subsampled to conceal the original advertising incrementality. Estimates describe the released benchmark under the analysis assumptions, rather than original advertiser lift or production ROI. Anonymized features also limit interpretation of the selected segment's business characteristics.

## Tools

**SQL / BigQuery** for behavioral analysis; **Python, pandas, NumPy, scipy, statsmodels, and scikit-learn** for statistical analysis and modeling; **Streamlit and Matplotlib** for the interactive report.

## Repository contents

| Path | Purpose |
| --- | --- |
| [app.py](app.py) | Streamlit entry point and navigation |
| [views/](views/) | Overview, product analytics, experiment design, experiment results, and uplift pages |
| [shared/data.py](shared/data.py) | Cached loaders for exported analysis results |
| [shared/styling.py](shared/styling.py) | Shared report styling and components |
| [data/funnel_by_device.csv](data/funnel_by_device.csv) | Device-level ordered funnel results |
| [data/experiment_results.csv](data/experiment_results.csv) | Overall and top-decile conversion estimates and confidence intervals |
| [requirements.txt](requirements.txt) | Dependencies for running the Streamlit report |

---

**Author:** [Forough](https://github.com/Foroughmo) · Independent portfolio project
