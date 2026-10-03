"""src/datafun/app.py - Project script.

Author: Luke Stevers
Date: 2026-10

HOW TO RUN THIS FILE:

From the VS Code menu (with only this project open in VS Code),
click "Terminal" / New Terminal to
open an integrated Terminal in the root project folder.
Paste the following command and press ENTER or RETURN
to run this file as a script:

uv run python -m datafun.app

DOMAIN:

A dataset of penguins.
See docs/data-card.md for more information about the dataset.

EXPLORE:

Earlier analysis showed relationships among
numeric penguin measurements.

In this project, we use one numeric feature
to predict one numeric target
with a simple linear regression model.

A standard predictive modeling process is:

1. OBSERVE the data and prior findings.
2. DECLARE the target and feature.
3. PREPARE the modeling data.
4. SPLIT into training and test data.
5. BASELINE with a simple reference model.
6. TRAIN a LinearRegression model.
7. PREDICT on X_test.
8. EVALUATE baseline vs model on y_test.
9. VISUALIZE predictions and residuals.
10. ASSESS the results.

DESIGN:

Use this file to declare the data-specific choices
and the reasoning behind them,
then orchestrate the work.

Scikit-learn provides the machine learning tools.

The target, feature, split, baseline,
and model choices stay here because they are
analytical decisions specific to this project.
"""

# === DECLARE IMPORTS (BRING IN FREE CODE) ===

import logging
from pathlib import Path
from typing import Final

from datafun_toolkit.logger import get_logger, log_header, log_path
import matplotlib.pyplot as plt
from ml_vizkit import save_chart
import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split

# === CONFIGURE LOGGER ONCE FOR THE APPLICATION ===

LOG: logging.Logger = get_logger("P06", level="DEBUG")

# === DECLARE GLOBAL CONSTANTS ===

# Some global variables are CONSTANT.
# They do NOT change while the program runs.
# By convention, constants use UPPERCASE_WITH_UNDERSCORES.
# Final indicates that the value should not be reassigned.

# === LOCATE THE DATA FILE ===

DATA_FILE_PATH: Final[Path] = Path("data") / "raw" / "Teams.csv"

# === LOCATE THE CHART OUTPUT ===

CHART_DIR: Final[Path] = Path("docs") / "images"

PREDICTION_CHART_PATH: Final[Path] = CHART_DIR / "baseball-batting-average-wins.png"

RESIDUAL_CHART_PATH: Final[Path] = CHART_DIR / "baseball-regression-residuals.png"

# === DETERMINE WHAT ONE ROW REPRESENTS ===

GRAIN: Final[str] = "one MLB team-season"

# === DECLARE THE TARGET ===

# CUSTOM: Choose one NUMERIC target value to predict.
# This must match a numeric column name EXACTLY
# as it appears in the data file.

TARGET_COLUMN: Final[str] = "W"

# === DECLARE THE FEATURE ===

# CUSTOM: Choose one NUMERIC feature
# that might help predict the target.
# This must match a numeric column name EXACTLY
# as it appears in the data file.

FEATURE_COLUMN: Final[str] = "batting_avg"

# === DOCUMENT WHY THE FEATURE MIGHT HELP ===

# CUSTOM: Document the reasoning behind the feature choice.
# Do not assume the feature will work well.
# The model and evaluation will provide evidence.

FEATURE_DECISION: Final[str] = r"""
I want to predict the number of regular-season wins
for an MLB team.

I selected team batting average as the feature.

Batting average is calculated as hits divided by at-bats:

batting average = H / AB

A team that gets more hits relative to its at-bats
may score more runs and potentially win more games.

I want to investigate how useful batting average is
for predicting the number of wins a team has in a season.

I do not know yet how well batting average will predict wins.
The modeling process will provide evidence.
"""

# === DECLARE THE TRAIN / TEST SPLIT ===

# CUSTOM: Decide how much data should be held back for testing.
# The test data should NOT be used to train the model.

TEST_FRACTION: Final[float] = 0.20

# CUSTOM: Choose whether the random split should be reproducible.
# A fixed random seed makes the same split each time the script runs.

RANDOM_SEED: Final[int] = 42

# === DOCUMENT THE SPLIT DECISION ===

# CUSTOM: Document the reasoning behind BOTH choices.
# The fraction and random seed should not be unexplained numbers.

SPLIT_DECISION: Final[str] = r"""
I will use 80% of the modeling rows for training
and hold back 20% for testing.

I want most of the available data to be available
for learning the model,
while still keeping a separate set of observations
that the model did not see during training.

The test rows will be used later
to evaluate how the trained model performs
on unseen observations.

I will use a random seed of 42.

The specific value 42 is not analytically important.
I use a fixed seed so the random split is reproducible.
Running the project again will produce the same
training and test observations,
which makes results easier to reproduce and compare.
"""

# === DECLARE THE BASELINE ===

BASELINE_STRATEGY: Final[str] = "mean"

# === DOCUMENT THE BASELINE DECISION ===

BASELINE_DECISION: Final[str] = r"""
Before evaluating the LinearRegression model,
I need a simple baseline for comparison.

The baseline will ignore batting average
and predict the average number of wins
from the training data for every test observation.

A useful predictive model should improve
on this simple reference prediction.
"""

# === DOCUMENT THE MODEL DECISION ===

MODEL_DECISION: Final[str] = r"""
I will use LinearRegression.

Linear regression fits a straight-line relationship
between team batting average and regular-season wins.

This gives a simple and interpretable model that allows
me to investigate how much information batting average
provides about team wins.

Fitting a line does not prove that batting average
is a strong predictor of wins.

The evaluation metrics and visualizations will provide
evidence about the usefulness of the model.
"""


# === DEFINE THE MAIN FUNCTION ===


def main() -> None:
    """Entry point when running this file as a Python script.

    This is where the instructions begin.

    Arguments: None.
    Returns: None.
    """
    log_header(LOG, "P06 - LINEAR REGRESSION")

    LOG.info("===================================")
    LOG.info("START main()")
    LOG.info("===================================")

    # ============================================================
    # 01. OBSERVE
    # ============================================================

    LOG.info("-------------------------------")
    LOG.info("01. OBSERVE the data and prior findings.")
    LOG.info("-------------------------------")

    log_path(LOG, "data file", path=DATA_FILE_PATH)

    df: pd.DataFrame = pd.read_csv(DATA_FILE_PATH)

    LOG.info("Data loaded successfully.")
    LOG.info(f"Grain: {GRAIN}")
    LOG.info(f"Rows: {df.shape[0]}")
    LOG.info(f"Columns: {df.shape[1]}")
    LOG.info(f"Column names: {df.columns.tolist()}")

    # ============================================================
    # 02. DECLARE
    # ============================================================

    LOG.info("-------------------------------")
    LOG.info("02. DECLARE the target and feature.")
    LOG.info("-------------------------------")

    LOG.info(f"Target:  {TARGET_COLUMN}")
    LOG.info(f"Feature: {FEATURE_COLUMN}")
    LOG.info(FEATURE_DECISION)

    # ============================================================
    # 03. PREPARE
    # ============================================================

    LOG.info("-------------------------------")
    LOG.info("03. PREPARE the modeling data.")
    LOG.info("-------------------------------")

    # Keep only modern MLB seasons with comparable regular-season
    # schedules. Exclude 2020 because it was a shortened season.
    df_model: pd.DataFrame = df[
        (df["yearID"] >= 2000) & (df["yearID"] <= 2025) & (df["yearID"] != 2020)
    ].copy()

    # Calculate team batting average.
    df_model["batting_avg"] = df_model["H"] / df_model["AB"]

    # Keep only rows with complete feature and target values.
    required_columns: list[str] = [
        FEATURE_COLUMN,
        TARGET_COLUMN,
    ]

    df_model = df_model.dropna(subset=required_columns).copy()

    # Log row counts.
    count_original: int = df.shape[0]
    count_model: int = df_model.shape[0]
    count_dropped: int = count_original - count_model

    LOG.info(f"Original rows: {count_original}")
    LOG.info(f"Modeling rows: {count_model}")
    LOG.info(f"Rows dropped: {count_dropped}")
    LOG.info("Years included: 2000-2025, excluding 2020")

    # scikit-learn expects X to be a 2-dimensional
    # feature matrix and y to be a 1-dimensional target.
    X: pd.DataFrame = df_model[[FEATURE_COLUMN]]
    y: pd.Series = df_model[TARGET_COLUMN]

    LOG.info(f"X shape: {X.shape}")
    LOG.info(f"y shape: {y.shape}")

    # ============================================================
    # 04. SPLIT
    # ============================================================

    LOG.info("-------------------------------")
    LOG.info("04. SPLIT into training and test data.")
    LOG.info("-------------------------------")

    LOG.info(SPLIT_DECISION)

    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_FRACTION,
        random_state=RANDOM_SEED,
    )

    LOG.info(f"Training rows: {X_train.shape[0]}")
    LOG.info(f"Test rows: {X_test.shape[0]}")

    # ============================================================
    # 05. BASELINE
    # ============================================================

    LOG.info("-------------------------------")
    LOG.info("05. BASELINE with a simple reference model.")
    LOG.info("-------------------------------")

    LOG.info(BASELINE_DECISION)

    baseline_model = DummyRegressor(
        strategy=BASELINE_STRATEGY,
    )

    baseline_model.fit(
        X_train,
        y_train,
    )

    baseline_predictions: np.ndarray = baseline_model.predict(X_test)

    baseline_rmse: float = float(
        root_mean_squared_error(
            y_test,
            baseline_predictions,
        )
    )

    baseline_r_squared: float = float(
        r2_score(
            y_test,
            baseline_predictions,
        )
    )

    LOG.info(f"Baseline strategy: {BASELINE_STRATEGY}")
    LOG.info(f"Baseline RMSE: {baseline_rmse:.2f}")
    LOG.info(f"Baseline R-squared: {baseline_r_squared:.3f}")

    # ============================================================
    # 06. TRAIN
    # ============================================================

    LOG.info("-------------------------------")
    LOG.info("06. TRAIN a LinearRegression model.")
    LOG.info("-------------------------------")

    LOG.info(MODEL_DECISION)

    model = LinearRegression()

    model.fit(
        X_train,
        y_train,
    )

    slope: float = float(model.coef_[0])
    intercept: float = float(model.intercept_)

    LOG.info("The model learned this line:")
    LOG.info(f"{TARGET_COLUMN} = {slope:.3f} * {FEATURE_COLUMN} + {intercept:.3f}")

    # ============================================================
    # 07. PREDICT
    # ============================================================

    LOG.info("-------------------------------")
    LOG.info("07. PREDICT on X_test.")
    LOG.info("-------------------------------")

    # The model has never trained on X_test.
    # Use the trained model to predict target values
    # for these held-back observations.
    model_predictions: np.ndarray = model.predict(X_test)

    LOG.info(f"Predictions created: {len(model_predictions)}")

    # ============================================================
    # 08. EVALUATE
    # ============================================================

    LOG.info("-------------------------------")
    LOG.info("08. EVALUATE baseline vs model on y_test.")
    LOG.info("-------------------------------")

    # RMSE measures prediction error
    # in the same units as the target.
    # Lower RMSE is better.
    model_rmse: float = float(
        root_mean_squared_error(
            y_test,
            model_predictions,
        )
    )

    # R-squared describes how much of the variation
    # in the test target is accounted for by the model.
    model_r_squared: float = float(
        r2_score(
            y_test,
            model_predictions,
        )
    )

    LOG.info("BASELINE RESULTS")
    LOG.info(f"RMSE:      {baseline_rmse:.2f}")
    LOG.info(f"R-squared: {baseline_r_squared:.3f}")

    LOG.info("LINEAR REGRESSION RESULTS")
    LOG.info(f"RMSE:      {model_rmse:.2f}")
    LOG.info(f"R-squared: {model_r_squared:.3f}")

    # ============================================================
    # 09. VISUALIZE
    # ============================================================

    LOG.info("-------------------------------")
    LOG.info("09. VISUALIZE predictions and residuals.")
    LOG.info("-------------------------------")

    CHART_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # === PREDICTIONS CHART ===

    # Plot the actual test observations.
    _prediction_figure, prediction_ax = plt.subplots()

    x_test_values: np.ndarray = X_test[FEATURE_COLUMN].to_numpy()

    y_test_values: np.ndarray = y_test.to_numpy()

    prediction_ax.scatter(
        x_test_values,
        y_test_values,
        label="Actual",
    )

    # Sort x values so the regression line
    # is drawn from left to right.
    prediction_order: np.ndarray = np.argsort(x_test_values)

    prediction_ax.plot(
        x_test_values[prediction_order],
        model_predictions[prediction_order],
        label="Predicted",
    )

    prediction_ax.set_title("Team Batting Average vs. Regular-Season Wins")
    prediction_ax.set_xlabel("Team Batting Average")
    prediction_ax.set_ylabel("Regular-Season Wins")
    prediction_ax.legend()

    save_chart(
        prediction_ax,
        PREDICTION_CHART_PATH,
    )

    LOG.info(f"Chart saved successfully at {PREDICTION_CHART_PATH}.")

    # === RESIDUAL CHART ===

    # A residual is:
    # actual value - predicted value
    #
    # Residuals near zero indicate predictions
    # close to the observed target values.

    residuals: np.ndarray = y_test_values - model_predictions

    _, residual_ax = plt.subplots()

    residual_ax.scatter(
        x_test_values,
        residuals,
    )

    # Draw a horizontal reference line at zero.
    residual_ax.axhline(0)

    residual_ax.set_title("Residuals for Batting Average Model")
    residual_ax.set_xlabel("Team Batting Average")
    residual_ax.set_ylabel("Residual (Actual - Predicted Wins)")

    save_chart(
        residual_ax,
        RESIDUAL_CHART_PATH,
    )

    LOG.info(f"Chart saved successfully at {RESIDUAL_CHART_PATH}.")

    # ============================================================
    # 10. ASSESS
    # ============================================================

    LOG.info("-------------------------------")
    LOG.info("10. ASSESS the results.")
    LOG.info("-------------------------------")

    LOG.info(
        r"""CUSTOM OBSERVATIONS:
I used team batting average to predict regular-season wins.

The dataset includes 750 MLB team-season observations
from 2000 through 2025, excluding the shortened 2020 season.

The baseline RMSE was 11.78 wins.

The LinearRegression RMSE was 10.61 wins.

Compared with the baseline, the LinearRegression model
had a lower RMSE, meaning batting average provided useful
information for predicting wins.

The model R-squared was 0.186, meaning the model explained
about 18.6% of the variation in wins in the test data.

The prediction plot showed a positive relationship between
team batting average and regular-season wins, but the points
were fairly spread out around the regression line.

The residual plot showed substantial variation in prediction
errors, with residuals occurring both above and below zero.

Based on this evidence, I conclude that team batting average
has some predictive value for regular-season wins, but
batting average alone is not enough to accurately predict
a team's total wins.

Next, I would like to investigate whether adding other
offensive statistics improves the predictions."""
    )

    # ============================================================
    # DISPLAY
    # ============================================================

    LOG.info("In a script, call plt.show() at the end to display all charts.")
    LOG.info("Close all chart windows (with the close button) to continue.")

    plt.show()

    LOG.info("===================================")
    LOG.info("END main() - Executed successfully!")
    LOG.info("===================================")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    main()
