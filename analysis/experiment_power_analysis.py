
import math
import pandas as pd
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

# Inputs from GA4 SQL analysis
baseline = 0.0336
daily_traffic = 553.6

# Experiment assumptions
alpha = 0.05
power = 0.80
relative_lifts = [0.10, 0.15, 0.20, 0.25]

results = []
power_analysis = NormalIndPower()

for lift in relative_lifts:
    treatment_rate = baseline * (1 + lift)

    effect_size = proportion_effectsize(
        baseline, treatment_rate
    )

    n_per_group = math.ceil(
        power_analysis.solve_power(
            effect_size=abs(effect_size),
            alpha=alpha,
            power=power,
            ratio=1,
            alternative="two-sided"
        )
    )

    total_sample = n_per_group * 2
    duration_days = total_sample / daily_traffic

    results.append({
        "MDE": f"{lift:.0%}",
        "Target conversion (%)": round(treatment_rate * 100, 3),
        "Users per group": n_per_group,
        "Total users": total_sample,
        "Duration (weeks)": round(duration_days / 7, 1)
    })

results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))
