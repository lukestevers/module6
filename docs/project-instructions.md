# Project-Specific Instructions

## Project Overview

This project applies a simple linear regression workflow to Major League Baseball team-season data.

The project investigates the question:

> **Can a team's batting average help predict the number of regular-season wins it will have?**

The analysis uses team-season observations from **2000 through 2025**, excluding the shortened 2020 season.

The final modeling dataset contains **750 observations**.

---

## Project Requirements

To reproduce the analysis, you need:

- Python 3.14+
- `uv`
- The project source code
- The MLB team-season data file

The project uses several Python packages, including:

- pandas
- NumPy
- scikit-learn
- Matplotlib
- project-specific visualization and logging tools

The dependencies are defined in:

```text
pyproject.toml
```

---

## Project Structure

The important project files and folders are:

```text
module6/
├── data/
│   └── raw/
│       └── Teams.csv
├── docs/
│   ├── images/
│   │   ├── baseball-batting-average-wins.png
│   │   └── baseball-regression-residuals.png
│   ├── concepts.md
│   ├── data-card.md
│   ├── project-instructions.md
│   └── index.md
├── src/
│   └── datafun/
│       └── app.py
├── .github/
│   └── workflows/
├── project.log
├── pyproject.toml
├── README.md
└── zensical.toml
```

The local project folder may have a different name from the GitHub repository. The important part is that commands are run from the project root.

---

## Step 1: Obtain the Data

The analysis uses:

```text
data/raw/Teams.csv
```

The file contains historical MLB team-season statistics.

The original dataset contains **3,614 rows and 48 columns**.

The analysis does not use every row or every column.

---

## Step 2: Select the Analysis Period

The application filters the data to MLB seasons from:

```text
2000 through 2025
```

The 2020 season is excluded because MLB played a shortened 60-game regular season that year.

This produces a more consistent set of full-season observations.

After filtering and preparing the data, **750 team-season observations** are available for modeling.

---

## Step 3: Calculate Batting Average

The project creates a new feature called:

```text
batting_avg
```

It is calculated using:

```text
batting_avg = H / AB
```

where:

- `H` = hits
- `AB` = at-bats

This calculated value becomes the single feature used by the regression model.

---

## Step 4: Define the Target

The target variable is:

```text
W
```

The `W` column represents the team's number of regular-season wins.

The modeling relationship is therefore:

```text
batting_avg → W
```

The model attempts to use batting average to predict regular-season wins.

---

## Step 5: Split the Data

The 750 modeling observations are divided into training and test data.

The project uses:

- **600 training observations**
- **150 test observations**

The training data is used to fit the model.

The test data is held aside for evaluation.

This allows the model to be evaluated on observations that were not used during training.

---

## Step 6: Establish the Baseline

Before training the regression model, the project establishes a simple baseline.

The baseline predicts the mean number of wins from the training data for each test observation.

The baseline results are:

```text
RMSE = 11.78
R² = -0.002
```

This provides a reference point for evaluating the regression model.

---

## Step 7: Train the Regression Model

The project uses scikit-learn's `LinearRegression`.

The model is trained using:

```text
Feature: batting_avg
Target: W
```

The resulting regression equation is approximately:

```text
W = 315.710 × batting_avg + 0.138
```

The positive coefficient indicates a positive relationship between batting average and predicted wins.

---

## Step 8: Generate Predictions

After training, the model generates predictions for the test data.

The predictions represent the number of wins estimated from each team's batting average.

The project compares these predictions with the actual number of wins.

---

## Step 9: Evaluate the Model

The model is evaluated using:

- RMSE
- R²

The final test results are:

| Model | RMSE | R² |
|---|---:|---:|
| Baseline | 11.78 | -0.002 |
| Linear Regression | 10.61 | 0.186 |

The regression model has a lower RMSE than the baseline.

The R² value of **0.186** means that batting average explains about **18.6% of the variation in wins in the test data**.

---

## Step 10: Review the Visualizations

The application generates two charts.

### Batting Average and Wins

```text
docs/images/baseball-batting-average-wins.png
```

This visualization shows the relationship between team batting average and regular-season wins.

The regression line slopes upward, showing a positive relationship.

However, the observations are spread out around the line, showing that batting average alone does not explain most of the variation in wins.

### Regression Residuals

```text
docs/images/baseball-regression-residuals.png
```

The residual plot shows the difference between actual wins and predicted wins.

Residuals above zero indicate that the model predicted too few wins.

Residuals below zero indicate that the model predicted too many wins.

The substantial variation in the residuals demonstrates that the model does not capture all of the factors associated with team win totals.

---

## Step 11: Run the Project

Open a terminal in the project root.

First synchronize the project environment:

```shell
uv sync
```

Then run the application:

```shell
uv run python -m datafun.app
```

The application loads the data, prepares the modeling dataset, trains the model, evaluates the predictions, creates the charts, and records information in the project log.

---

## Step 12: Build the Documentation

The project documentation is built using Zensical.

Run:

```shell
uv run python -m zensical build
```

A successful build should complete without documentation errors.

The generated documentation can then be deployed through the project's GitHub Actions workflow.

---

## Development Checks

Several development checks can be run locally.

### Format the Code

```shell
uv run ruff format .
```

### Check the Code

```shell
uv run ruff check . --fix
```

### Run Tests

```shell
uv run python -m pytest
```

### Run Type Checking

```shell
uv run ty check
```

### Build Documentation

```shell
uv run python -m zensical build
```

---

## Git Workflow

After making changes, check the repository status:

```shell
git status
```

Stage changes:

```shell
git add -A
```

Create a commit:

```shell
git commit -m "Describe the changes"
```

Push the changes:

```shell
git push
```

GitHub Actions will then run the project's automated checks and documentation deployment workflow.

---

## Expected Results

A successful run of the application should produce results approximately like these:

```text
Modeling rows: 750
Training rows: 600
Test rows: 150

Baseline RMSE: 11.78
Regression RMSE: 10.61

Regression R²: 0.186

W = 315.710 * batting_avg + 0.138
```

The exact formatting of the console output may vary.

The important results are that the regression model produces a lower RMSE than the baseline and that the test-set R² is approximately **0.186**.

---

## Interpreting the Results

The analysis found a positive relationship between team batting average and regular-season wins.

However, batting average alone is not enough to accurately predict a team's total number of wins.

The model explains about 18.6% of the variation in test-set wins, leaving substantial variation unexplained.

This suggests that additional team statistics could improve the model.

---

## Reproducing the Analysis

The complete workflow is:

```text
Load Teams.csv
      ↓
Select 2000–2025
      ↓
Exclude 2020
      ↓
Calculate batting_avg
      ↓
Select batting_avg and W
      ↓
Split into training/test data
      ↓
Create baseline
      ↓
Train LinearRegression
      ↓
Generate predictions
      ↓
Calculate RMSE and R²
      ↓
Create visualizations
      ↓
Interpret results
```

Following these steps should reproduce the main analysis and results documented on this site.

---

## Possible Extensions

The current project uses only batting average as a feature.

A future version could investigate additional variables such as:

- Runs
- Home runs
- Walks
- Stolen bases
- On-base percentage
- Slugging percentage

These additional features could be used to build a multiple-feature regression model and determine whether prediction accuracy improves.

---

## Related Documentation

- [Project Homepage](index.md)
- [Concepts](concepts.md)
- [Data Card](data-card.md)
- [API Reference](api.md)
