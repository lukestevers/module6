# API Reference

This page documents the main configuration values and application workflow used by the MLB batting average and regular-season wins analysis.

The primary application is:

```text
src/datafun/app.py
```

The application loads MLB team-season data, prepares the modeling dataset, trains a linear regression model, evaluates the predictions, and creates visualizations.

---

## Application Overview

The main analysis follows this sequence:

```text
Load Data
    ↓
Prepare Data
    ↓
Calculate Batting Average
    ↓
Select Feature and Target
    ↓
Split Training/Test Data
    ↓
Create Baseline
    ↓
Train Linear Regression
    ↓
Generate Predictions
    ↓
Evaluate Model
    ↓
Create Visualizations
    ↓
Record Observations
```

---

## Imports

The application uses the following major libraries and modules:

```python
import logging
from pathlib import Path
from typing import Final

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split
```

The project also uses project-specific logging and visualization utilities.

---

# Configuration Constants

The application keeps important project decisions in named constants near the top of `app.py`.

This makes the data-specific choices easy to identify and change.

---

## `DATA_FILE_PATH`

```python
DATA_FILE_PATH: Final[Path] = Path("data") / "raw" / "Teams.csv"
```

Specifies the location of the MLB team-season dataset.

The expected file is:

```text
data/raw/Teams.csv
```

---

## `CHART_DIR`

```python
CHART_DIR: Final[Path] = Path("docs") / "images"
```

Specifies the directory where the project visualizations are saved.

---

## `PREDICTION_CHART_PATH`

```python
PREDICTION_CHART_PATH: Final[Path] = (
    CHART_DIR / "baseball-batting-average-wins.png"
)
```

Specifies the output path for the batting-average and wins visualization.

The generated file is:

```text
docs/images/baseball-batting-average-wins.png
```

---

## `RESIDUAL_CHART_PATH`

```python
RESIDUAL_CHART_PATH: Final[Path] = (
    CHART_DIR / "baseball-regression-residuals.png"
)
```

Specifies the output path for the regression residual visualization.

The generated file is:

```text
docs/images/baseball-regression-residuals.png
```

---

## `GRAIN`

```python
GRAIN: Final[str] = "one MLB team-season"
```

Describes what one row of the modeling dataset represents.

Each observation represents one MLB team during one season.

---

## `TARGET_COLUMN`

```python
TARGET_COLUMN: Final[str] = "W"
```

Specifies the numeric target that the model attempts to predict.

The `W` column represents regular-season wins.

---

## `FEATURE_COLUMN`

```python
FEATURE_COLUMN: Final[str] = "batting_avg"
```

Specifies the feature used by the regression model.

The feature is calculated from hits and at-bats:

```text
batting_avg = H / AB
```

---

## Feature Selection

The project uses batting average as its single predictive feature.

The reasoning behind the choice is that batting average provides a simple measure of team hitting performance.

The project does not assume that batting average will be sufficient for accurate prediction. The model evaluation is used to determine how much predictive information the feature provides.

---

# Data Preparation

The application loads the complete `Teams.csv` dataset and then selects the period used for modeling.

The analysis includes:

```text
2000–2025
```

The 2020 season is excluded because it was a shortened MLB season.

The resulting modeling dataset contains:

```text
750 observations
```

---

## Calculating Batting Average

The application creates the `batting_avg` feature using:

```python
df["batting_avg"] = df["H"] / df["AB"]
```

This produces the ratio:

```text
Hits / At-Bats
```

The resulting value is used as the model's input feature.

---

# Train/Test Split

The prepared observations are divided into training and test sets using scikit-learn's `train_test_split`.

The project uses:

```text
600 training observations
150 test observations
```

The training data is used to fit the models.

The test data is used to evaluate predictions.

---

# Baseline Model

The project establishes a baseline using scikit-learn's `DummyRegressor`.

The baseline predicts the mean number of wins from the training data.

The purpose of the baseline is to provide a simple reference point.

The baseline results were:

```text
RMSE = 11.78
R² = -0.002
```

---

# Linear Regression

The primary model is scikit-learn's:

```python
LinearRegression
```

The model uses:

```text
Feature: batting_avg
Target: W
```

The fitted equation was approximately:

```text
W = 315.710 × batting_avg + 0.138
```

The positive coefficient indicates a positive relationship between batting average and predicted wins.

---

# Predictions

After training, the model generates predictions for the test data.

Conceptually:

```python
y_pred = model.predict(X_test)
```

The predictions are then compared with the actual values in `y_test`.

---

# Model Evaluation

The application evaluates the model using two primary metrics:

- Root Mean Squared Error (RMSE)
- R²

---

## `root_mean_squared_error`

RMSE measures the typical size of the model's prediction errors.

For this project, RMSE is expressed in wins.

The final results were:

| Model | RMSE |
|---|---:|
| Baseline | 11.78 |
| Linear Regression | 10.61 |

The regression model produced a lower RMSE than the baseline.

---

## `r2_score`

R² measures the proportion of variation in the target explained by the model.

The regression model produced:

```text
R² = 0.186
```

This means that batting average explained approximately **18.6% of the variation in wins in the test data**.

---

# Prediction Visualization

The application creates a visualization showing batting average and regular-season wins.

Output:

```text
docs/images/baseball-batting-average-wins.png
```

The chart illustrates the positive relationship between batting average and wins and shows the regression line.

The observations remain fairly spread out around the line, demonstrating that batting average alone does not explain most of the variation in wins.

---

# Residual Visualization

The application also creates a residual plot.

Output:

```text
docs/images/baseball-regression-residuals.png
```

A residual represents:

```text
Actual Wins - Predicted Wins
```

Positive residuals indicate that the model predicted too few wins.

Negative residuals indicate that the model predicted too many wins.

The residual plot shows substantial variation in prediction errors.

---

# `main()`

The `main()` function orchestrates the complete analysis.

Its responsibilities include:

1. Starting the project logging.
2. Loading the MLB team-season data.
3. Inspecting the dataset.
4. Filtering the analysis period.
5. Excluding the 2020 season.
6. Calculating batting average.
7. Preparing the feature and target.
8. Splitting the data.
9. Creating the baseline.
10. Training the linear regression model.
11. Generating predictions.
12. Calculating RMSE and R².
13. Creating the prediction visualization.
14. Creating the residual visualization.
15. Recording the custom observations.
16. Displaying the final results.

The application is run with:

```shell
uv run python -m datafun.app
```

---

# Custom Observations

The application records project-specific observations after the model evaluation.

The main conclusions are:

- The analysis uses 750 MLB team-season observations from 2000 through 2025, excluding 2020.
- The baseline RMSE was 11.78 wins.
- The linear regression RMSE was 10.61 wins.
- The regression model had an R² of 0.186.
- The model showed a positive relationship between batting average and wins.
- The observations were spread around the regression line.
- The residuals showed substantial prediction error.
- Batting average provides useful information for predicting wins.
- Batting average alone is not sufficient to accurately predict a team's total wins.
- Additional offensive statistics could be investigated in a future version.

---

# Expected Model Results

A successful run should produce results approximately equal to:

```text
Modeling observations: 750
Training observations: 600
Test observations: 150

Baseline RMSE: 11.78
Regression RMSE: 10.61
Regression R²: 0.186

W = 315.710 × batting_avg + 0.138
```

Minor differences in formatting may occur, but the main results should remain consistent when using the same data and project configuration.

---

# Running the Application

From the project root:

```shell
uv sync
```

Then:

```shell
uv run python -m datafun.app
```

The application will generate or update the project visualizations and execution log.

---

# Documentation Build

The documentation can be built locally with:

```shell
uv run python -m zensical build
```

A successful build should report that the documentation was built without issues.

---

# Development Commands

Format the project:

```shell
uv run ruff format .
```

Check the project:

```shell
uv run ruff check . --fix
```

Run type checking:

```shell
uv run ty check
```

Run tests:

```shell
uv run python -m pytest
```

Build documentation:

```shell
uv run python -m zensical build
```

---

# Related Documentation

- [Project Homepage](index.md)
- [Concepts](concepts.md)
- [MLB Team-Season Data Card](data-card.md)
- [Project-Specific Instructions](project-instructions.md)

---

# Summary

The API documented here corresponds to the project's actual MLB regression application.

The central modeling relationship is:

```text
Team Batting Average → Regular-Season Wins
```

The project uses a single-feature linear regression model, compares it with a mean baseline, evaluates the predictions using RMSE and R², and uses visualizations to examine the relationship and residual errors.

The resulting evidence shows that batting average contains some predictive information about team wins, while also demonstrating the limitations of using a single offensive statistic to predict overall team performance.
