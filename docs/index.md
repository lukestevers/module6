# MLB Batting Average and Regular-Season Wins

## Can batting average help predict how many games an MLB team will win?

This project applies a linear regression workflow to Major League Baseball team-season data to investigate whether a team's **batting average** can help predict its number of **regular-season wins**.

The analysis uses MLB team-season observations from **2000 through 2025**, excluding the shortened 2020 season.

---

## The Question

**Can a team's batting average predict the number of regular-season wins it will have?**

For each team-season, I calculated batting average as:

```text
Batting Average = Hits / At-Bats
```

I then used batting average as the single feature in a linear regression model with regular-season wins as the target.

The project follows this workflow:

```text
OBSERVE
   ↓
PREPARE
   ↓
SPLIT
   ↓
BASELINE
   ↓
TRAIN
   ↓
PREDICT
   ↓
EVALUATE
   ↓
VISUALIZE
   ↓
ASSESS
```

---

## Dataset

The original dataset contains **3,614 MLB team-season records**.

For this analysis, I selected:

- Seasons from **2000–2025**
- Excluded **2020** because it was a shortened 60-game season
- **750 team-season observations** remained for modeling

Each modeling observation represents **one MLB team in one season**.

The main variables are:

| Variable | Description |
|---|---|
| `yearID` | MLB season |
| `name` | Team name |
| `H` | Hits |
| `AB` | At-bats |
| `batting_avg` | Hits divided by at-bats |
| `W` | Regular-season wins |

---

## Modeling Approach

I divided the 750 modeling observations into:

- **600 training observations**
- **150 test observations**

The model uses:

**Feature:** Team batting average

**Target:** Regular-season wins

I first established a baseline that predicts the average number of wins from the training data. I then trained a `LinearRegression` model using batting average.

---

## Results

| Model | RMSE | R² |
|---|---:|---:|
| Baseline | 11.78 | -0.002 |
| Linear Regression | **10.61** | **0.186** |

The linear regression model reduced the prediction error compared with the baseline.

The model equation was approximately:

```text
Wins = 315.710 × Batting Average + 0.138
```

The model's R² of **0.186** means that batting average alone explained about **18.6% of the variation in wins in the test data**.

---

## Prediction Results

The scatterplot shows a positive relationship between team batting average and regular-season wins.

However, the observations are fairly spread out around the regression line. This indicates that batting average contains useful information about wins, but it does not explain most of the variation in team success.

![Batting Average and Regular-Season Wins](images/baseball-batting-average-wins.png)

### What the graph shows

The regression line slopes upward, meaning that teams with higher batting averages tended to have more regular-season wins in this dataset.

At the same time, teams with similar batting averages could have noticeably different numbers of wins.

That suggests that other factors contribute substantially to a team's win total.

---

## Residual Analysis

I also examined the residuals, which represent the difference between the actual number of wins and the model's predicted number of wins.

![Regression Residuals](images/baseball-regression-residuals.png)

The residual plot shows substantial variation above and below zero.

This supports the conclusion that the model does not capture all of the factors that influence regular-season wins.

---

## What I Learned

This project helped me better understand the complete machine learning workflow:

1. Load and inspect real-world data.
2. Select an appropriate feature and target.
3. Prepare the modeling dataset.
4. Split data into training and test sets.
5. Establish a baseline.
6. Train a linear regression model.
7. Generate predictions.
8. Evaluate the predictions with RMSE and R².
9. Visualize the results.
10. Interpret what the model can and cannot tell us.

One important lesson was that finding a relationship between two variables does not necessarily mean that one variable is sufficient for accurate prediction.

---

## Conclusion

Team batting average has **some predictive value** for regular-season wins, but batting average alone is not enough to accurately predict how many games an MLB team will win.

The model performed better than the baseline, but its R² of 0.186 shows that much of the variation in wins remains unexplained.

A natural next step would be to investigate whether adding other offensive statistics improves the predictions.

---

## Explore the Project

- [Project Instructions](project-instructions/)
- [Concepts](concepts/)
- [Data Card](data-card/)
- [API Reference](api/)

The complete source code and data are available in the [GitHub repository](https://github.com/lukestevers/module6).

---

## Project Technologies

This project uses:

- Python
- pandas
- NumPy
- scikit-learn
- Matplotlib
- uv
- Zensical
- GitHub Actions
- GitHub Pages
