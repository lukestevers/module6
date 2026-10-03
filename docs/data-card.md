# MLB Team-Season Data Card

## Dataset Overview

This project uses team-season data from the **Lahman Baseball Database**.

The dataset contains historical Major League Baseball team statistics. Each row represents the performance of one MLB team during one season.

For this project, the data is used to investigate the question:

> **Can a team's batting average help predict the number of regular-season wins it will have?**

---

## Data Source

**Dataset:** Lahman Baseball Database — Team Statistics

**File used in this project:**

```text
data/raw/Teams.csv
```

The original dataset contains **3,614 team-season records** and **48 columns**.

The project uses a subset of the available data for the regression analysis.

---

## Unit of Observation

The **grain** of the dataset is:

> **One MLB team-season**

For example, one row represents a particular team during a particular MLB season.

The dataset contains multiple observations for the same franchise because a team appears once for each season in which it has a record.

---

## Time Period

The original dataset contains team-season records from many different periods of MLB history.

For this project, I limited the analysis to:

**2000 through 2025**

This provides a more modern period of MLB history for the analysis.

### 2020 Season

The 2020 MLB season was excluded from the modeling data.

The 2020 season was shortened to a 60-game regular season, making it substantially different from the surrounding full seasons.

Including it would make comparisons of total regular-season wins less consistent with the other seasons in the analysis.

After selecting the 2000–2025 period and excluding 2020, the modeling dataset contains:

**750 team-season observations**

---

## Variables Used

The original `Teams.csv` file contains many team statistics.

The primary variables used in this project are:

| Variable | Description | Role |
|---|---|---|
| `yearID` | MLB season | Time identifier |
| `name` | Team name | Team identifier |
| `AB` | At-bats | Used to calculate batting average |
| `H` | Hits | Used to calculate batting average |
| `W` | Regular-season wins | Target |

A new variable called `batting_avg` was calculated from the original data.

---

## Feature: Batting Average

The primary feature used in the regression model is **team batting average**.

It was calculated as:

```text
Batting Average = Hits / At-Bats
```

In terms of the dataset columns:

```text
batting_avg = H / AB
```

Batting average was selected because it provides a simple measure of how frequently a team's at-bats resulted in hits.

The project does not assume that batting average will be a strong predictor. The regression model and evaluation metrics are used to determine how useful the feature actually is.

---

## Target: Regular-Season Wins

The target variable is:

```text
W
```

This represents the number of regular-season games won by the team during that season.

The goal of the model is to predict this value using team batting average.

---

## Modeling Dataset

After filtering and preparation:

- **750** team-season observations were used.
- **600** observations were used for training.
- **150** observations were used for testing.

The feature used by the model was:

```text
batting_avg
```

The target was:

```text
W
```

---

## Data Preparation

The analysis followed these preparation steps:

1. Load the `Teams.csv` dataset.
2. Select MLB seasons from 2000 through 2025.
3. Exclude the shortened 2020 season.
4. Calculate team batting average using hits divided by at-bats.
5. Remove observations that cannot be used for the selected variables.
6. Separate the feature and target.
7. Split the observations into training and test sets.

The resulting data was then used for a simple linear regression model.

---

## Data Quality Considerations

Several considerations are important when interpreting this dataset.

### Different Season Lengths

The 2020 MLB season was substantially shorter than a normal regular season. It was therefore excluded from the modeling dataset.

### Team-Season Data

Each observation represents a team during a particular season. The data is not individual-player data.

### Batting Average Is Only One Statistic

Batting average represents only one aspect of offensive performance.

It does not capture every way a team can produce runs or contribute to winning games.

Other statistics in the original dataset could potentially provide additional information.

---

## Modeling Results

The project compared a simple mean baseline with a linear regression model.

| Model | RMSE | R² |
|---|---:|---:|
| Baseline | 11.78 | -0.002 |
| Linear Regression | 10.61 | 0.186 |

The linear regression model produced a lower RMSE than the baseline.

The regression equation was approximately:

```text
W = 315.710 × batting_avg + 0.138
```

The model's R² value of **0.186** means that batting average explained about **18.6% of the variation in wins in the test data**.

---

## Interpretation

The analysis showed a **positive relationship** between team batting average and regular-season wins.

However, the observations were fairly spread out around the regression line.

This means that teams with higher batting averages tended to have more wins, but batting average alone did not explain most of the differences in team win totals.

The results therefore suggest that batting average provides **some useful predictive information**, but it is not sufficient by itself to accurately predict a team's total number of regular-season wins.

---

## Limitations

This project uses only one feature to predict wins.

A team's regular-season record can be influenced by many different factors, including offensive, defensive, pitching, baserunning, and other team-level statistics.

Because this model uses only batting average, it should not be interpreted as a complete model of team performance.

The model also describes relationships in the selected historical data. It does not establish that changing a team's batting average would necessarily cause a particular change in its number of wins.

---

## Possible Extensions

A future version of this project could investigate whether adding additional team statistics improves the predictions.

Possible additional features include:

- Runs
- Home runs
- Walks
- Stolen bases
- On-base percentage
- Slugging percentage

A multiple-feature regression model could then be compared with the single-feature model used in this project.

---

## Summary

This dataset provides team-level MLB statistics that can be used to investigate relationships between offensive performance and regular-season success.

For this project:

- The unit of observation is **one MLB team-season**.
- The analysis covers **2000–2025**, excluding 2020.
- **750 observations** were used for modeling.
- **Batting average** was calculated as `H / AB`.
- **Regular-season wins (`W`)** were used as the target.
- A simple linear regression model was used to make predictions.
- The regression model performed better than the mean baseline.
- Batting average alone explained about **18.6% of the variation in test-set wins**.

The results provide evidence that batting average contains useful information about team wins while also showing why additional variables would be needed for a more complete predictive model.
