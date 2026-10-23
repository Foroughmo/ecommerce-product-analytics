
"""Criteo randomized advertising experiment and uplift modeling analysis."""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from huggingface_hub import hf_hub_download
from scipy.stats import norm
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.proportion import proportions_ztest


SAMPLE_SIZE = 1_000_000
SAMPLE_FRACTION = 0.075
RANDOM_STATE = 42
FEATURE_COLS = [f"f{i}" for i in range(12)]


def main():
    file_path = hf_hub_download(
        repo_id="criteo/criteo-uplift",
        filename="criteo-research-uplift-v2.1.csv.gz",
        repo_type="dataset",
    )

    rng = np.random.default_rng(RANDOM_STATE)
    chunks = []
    for chunk in pd.read_csv(file_path, compression="gzip", chunksize=500_000):
        seed = int(rng.integers(0, 1_000_000))
        chunks.append(chunk.sample(frac=SAMPLE_FRACTION, random_state=seed))

    df = pd.concat(chunks, ignore_index=True)
    df = df.sample(n=SAMPLE_SIZE, random_state=RANDOM_STATE).reset_index(drop=True)
    print(f"Sample: {len(df):,} users")

    # Overall randomized experiment
    group_summary = df.groupby("treatment").agg(
        users=("conversion", "size"),
        conversions=("conversion", "sum"),
        conversion_rate=("conversion", "mean"),
        visits=("visit", "sum"),
        visit_rate=("visit", "mean"),
    )
    control_rate = group_summary.loc[0, "conversion_rate"]
    treatment_rate = group_summary.loc[1, "conversion_rate"]
    absolute_lift = treatment_rate - control_rate
    relative_lift = absolute_lift / control_rate

    successes = np.array([
        group_summary.loc[1, "conversions"],
        group_summary.loc[0, "conversions"],
    ])
    nobs = np.array([
        group_summary.loc[1, "users"],
        group_summary.loc[0, "users"],
    ])
    overall_z, overall_p = proportions_ztest(successes, nobs, alternative="two-sided")
    overall_se = np.sqrt(
        treatment_rate * (1 - treatment_rate) / nobs[0]
        + control_rate * (1 - control_rate) / nobs[1]
    )
    overall_ci_low = absolute_lift - 1.96 * overall_se
    overall_ci_high = absolute_lift + 1.96 * overall_se

    print("\n=== Overall experiment ===")
    print(group_summary.to_string())
    print(f"Control conversion: {control_rate:.4%}")
    print(f"Treatment conversion: {treatment_rate:.4%}")
    print(f"Absolute lift: {absolute_lift * 100:+.4f} pp")
    print(f"Relative lift: {relative_lift:.2%}")
    print(f"Z-statistic: {overall_z:.3f}; p-value: {overall_p:.6g}")
    print(f"95% CI: [{overall_ci_low * 100:+.4f}, {overall_ci_high * 100:+.4f}] pp")
    print(f"Incremental conversions per 100,000 users: {absolute_lift * 100_000:.1f}")
    print(
        "95% CI per 100,000 users: "
        f"[{overall_ci_low * 100_000:.1f}, {overall_ci_high * 100_000:.1f}]"
    )

    treated = df.loc[df["treatment"] == 1, "conversion"]
    control = df.loc[df["treatment"] == 0, "conversion"]
    ate_itt = treated.mean() - control.mean()
    print(f"ATE / ITT (assignment effect): {ate_itt * 100:+.4f} pp")

    # Exploratory heterogeneity check using f0
    print("\n=== Feature checks ===")
    print(df[FEATURE_COLS].describe().T.to_string())
    print("\nMissing values:")
    print(df[FEATURE_COLS].isna().sum().to_string())

    df["f0_group"] = pd.qcut(df["f0"], q=5, duplicates="drop")
    f0_effects = (
        df.groupby(["f0_group", "treatment"], observed=True)["conversion"]
        .agg(["mean", "count"])
        .reset_index()
    )
    f0_pivot = f0_effects.pivot(
        index="f0_group", columns="treatment", values="mean"
    )
    f0_pivot.columns = ["control_rate", "treatment_rate"]
    f0_pivot["absolute_effect"] = (
        f0_pivot["treatment_rate"] - f0_pivot["control_rate"]
    )
    f0_pivot["relative_lift"] = (
        f0_pivot["absolute_effect"] / f0_pivot["control_rate"]
    )
    print("\n=== f0 group effects ===")
    print(f0_pivot.to_string())

    df["f0_group_cat"] = df["f0_group"].astype(str)
    f0_model = smf.glm(
        formula="conversion ~ treatment * C(f0_group_cat)",
        data=df,
        family=sm.families.Binomial(),
    ).fit()
    print("\n=== f0 interaction model ===")
    print(f0_model.summary())

    # T-learner: two logistic regression models
    stratify_key = (
        df["treatment"].astype(str) + "_" + df["conversion"].astype(str)
    )
    train_df, test_df = train_test_split(
        df,
        test_size=0.30,
        random_state=RANDOM_STATE,
        stratify=stratify_key,
    )
    treated_train = train_df[train_df["treatment"] == 1]
    control_train = train_df[train_df["treatment"] == 0]

    treatment_model = make_pipeline(
        StandardScaler(), LogisticRegression(max_iter=1000)
    )
    control_model = make_pipeline(
        StandardScaler(), LogisticRegression(max_iter=1000)
    )
    treatment_model.fit(treated_train[FEATURE_COLS], treated_train["conversion"])
    control_model.fit(control_train[FEATURE_COLS], control_train["conversion"])

    test_df = test_df.copy()
    test_df["p_treatment"] = treatment_model.predict_proba(
        test_df[FEATURE_COLS]
    )[:, 1]
    test_df["p_control"] = control_model.predict_proba(
        test_df[FEATURE_COLS]
    )[:, 1]
    test_df["predicted_uplift"] = test_df["p_treatment"] - test_df["p_control"]

    test_df["uplift_decile"] = pd.qcut(
        test_df["predicted_uplift"], q=10, labels=False, duplicates="drop"
    ) + 1
    decile_results = (
        test_df.groupby(["uplift_decile", "treatment"], observed=True)["conversion"]
        .agg(["mean", "count"])
        .reset_index()
    )
    decile_pivot = decile_results.pivot(
        index="uplift_decile", columns="treatment", values="mean"
    )
    decile_pivot.columns = ["control_rate", "treatment_rate"]
    decile_pivot["observed_uplift"] = (
        decile_pivot["treatment_rate"] - decile_pivot["control_rate"]
    )
    print(f"\nTraining users: {len(train_df):,}; test users: {len(test_df):,}")
    print("\n=== Observed uplift by predicted-uplift decile ===")
    print(decile_pivot.to_string())

    # Evaluation of the top 10% vs the remaining 90%
    test_df["high_uplift"] = np.where(
        test_df["uplift_decile"] == 10, "Top 10%", "Other 90%"
    )
    targeting_results = (
        test_df.groupby(["high_uplift", "treatment"])["conversion"]
        .agg(["mean", "count", "sum"])
        .reset_index()
    )
    targeting_pivot = targeting_results.pivot(
        index="high_uplift", columns="treatment", values="mean"
    )
    targeting_pivot.columns = ["control_rate", "treatment_rate"]
    targeting_pivot["absolute_effect"] = (
        targeting_pivot["treatment_rate"] - targeting_pivot["control_rate"]
    )
    targeting_pivot["relative_lift"] = (
        targeting_pivot["absolute_effect"] / targeting_pivot["control_rate"]
    )
    print("\n=== Selected segments (counts and conversions) ===")
    print(targeting_results.to_string(index=False))
    print("\n=== Treatment effects by segment ===")
    print(targeting_pivot.to_string())

    # Test 1: treatment effect within the top 10%
    top10 = test_df[test_df["high_uplift"] == "Top 10%"]
    top_treat = top10.loc[top10["treatment"] == 1, "conversion"]
    top_control = top10.loc[top10["treatment"] == 0, "conversion"]
    top_effect = top_treat.mean() - top_control.mean()
    top_se = np.sqrt(
        top_treat.mean() * (1 - top_treat.mean()) / len(top_treat)
        + top_control.mean() * (1 - top_control.mean()) / len(top_control)
    )
    top_ci_low = top_effect - 1.96 * top_se
    top_ci_high = top_effect + 1.96 * top_se
    top_z, top_p = proportions_ztest(
        np.array([top_treat.sum(), top_control.sum()]),
        np.array([len(top_treat), len(top_control)]),
        alternative="two-sided",
    )
    print("\n=== Test 1: treatment effect within top 10% ===")
    print(f"Selected test users: {len(top10):,}")
    print(f"Observed lift: {top_effect * 100:+.4f} pp")
    print(f"Z-statistic: {top_z:.3f}; p-value: {top_p:.6g}")
    print(f"95% CI: [{top_ci_low * 100:+.4f}, {top_ci_high * 100:+.4f}] pp")

    # Test 2: difference in treatment effects (top 10% minus other 90%)
    groups = {}
    for segment in ["Top 10%", "Other 90%"]:
        subset = test_df[test_df["high_uplift"] == segment]
        segment_treat = subset.loc[subset["treatment"] == 1, "conversion"]
        segment_control = subset.loc[subset["treatment"] == 0, "conversion"]
        rate_treat = segment_treat.mean()
        rate_control = segment_control.mean()
        groups[segment] = {
            "effect": rate_treat - rate_control,
            "variance": (
                rate_treat * (1 - rate_treat) / len(segment_treat)
                + rate_control * (1 - rate_control) / len(segment_control)
            ),
        }

    effect_difference = groups["Top 10%"]["effect"] - groups["Other 90%"]["effect"]
    difference_se = np.sqrt(
        groups["Top 10%"]["variance"] + groups["Other 90%"]["variance"]
    )
    difference_z = effect_difference / difference_se
    difference_p = 2 * norm.sf(abs(difference_z))
    difference_ci_low = effect_difference - 1.96 * difference_se
    difference_ci_high = effect_difference + 1.96 * difference_se

    print("\n=== Test 2: top 10% vs other 90% ===")
    print(f"Top 10% uplift: {groups['Top 10%']['effect'] * 100:+.4f} pp")
    print(f"Other 90% uplift: {groups['Other 90%']['effect'] * 100:+.4f} pp")
    print(f"Difference in lift: {effect_difference * 100:+.4f} pp")
    print(f"Z-statistic: {difference_z:.3f}; p-value: {difference_p:.6g}")
    print(
        f"95% CI: [{difference_ci_low * 100:+.4f}, "
        f"{difference_ci_high * 100:+.4f}] pp"
    )


if __name__ == "__main__":
    main()
