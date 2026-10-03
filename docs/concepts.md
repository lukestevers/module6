# Concepts

This project uses a simple machine learning workflow to investigate whether **team batting average can help predict regular-season wins**.

The goal is not just to build a model, but to understand what the model tells us, how well it performs, and what its limitations are.

---

## Linear Regression

**Linear regression** is a supervised machine learning method used to model the relationship between a numeric feature and a numeric target.

In this project:

- The **feature** is team batting average.
- The **target** is regular-season wins.

The model attempts to find a line that describes the relationship between batting average and wins.

The regression equation produced by this project was approximately:

```text
W = 315.710 × batting_avg + 0.138
```

The slope of the line is positive, which means that higher batting averages are associated with higher predicted win totals in the model.

---

## Feature and Target

A machine learning model needs to know what information it will use to make predictions and what value it is trying to predict.

### Feature

The **feature** is the input variable used by the model.

This project uses:

```text
batting_avg
```

Batting average was calculated as:

```text
Batting Average = Hits / At-Bats
```

In the original dataset:

```text
batting_avg = H / AB
```

### Target

The **target** is the value the model attempts to predict.

This project uses:

```text
W
```

The `W` column represents the team's number of regular-season wins.

---

## Why Batting Average?

Batting average was selected because it provides a simple measure of team hitting performance.

The project does not assume that batting average will accurately predict wins before testing the model.

Instead, the model evaluation provides evidence about how much predictive information batting average contains.

The results showed a positive relationship, but also substantial variation that batting average alone could not explain.

---

## Training and Test Data

A machine learning model should be evaluated using data that was not used to train it.

The project divided the 750 modeling observations into:

- **600 training observations**
- **150 test observations**

The training data was used to fit the regression model.

The test data was held aside and used to evaluate how well the model predicted observations it had not seen during training.

This separation helps provide a more realistic measure of predictive performance.

---

## Baseline Model

Before evaluating the regression model, the project establishes a **baseline**.

The baseline provides a simple reference point against which the machine learning model can be compared.

In this project, the baseline predicts the average number of wins from the training data for every observation in the test set.

The baseline produced:

```text
RMSE = 11.78 wins
R² = -0.002
```

A useful predictive model should provide evidence that it improves upon this simple reference.

---

## Linear Regression Model

The project uses scikit-learn's `LinearRegression` model.

The model learns a relationship between:

```text
batting_avg → W
```

The fitted equation was:

```text
W = 315.710 × batting_avg + 0.138
```

The model's positive slope indicates that higher team batting averages correspond to higher predicted win totals.

However, the regression line is only an estimate. Individual teams can have substantially more or fewer wins than the line predicts.

---

## Predictions

After training the model, the project uses it to generate predicted win totals for the test observations.

Each prediction represents the number of wins the model expects based only on the team's batting average.

For example, two teams with similar batting averages may receive similar predicted win totals even if their actual win totals are quite different.

This difference between predicted and actual values is important when evaluating the model.

---

## Root Mean Squared Error (RMSE)

**Root Mean Squared Error**, or **RMSE**, measures the typical size of prediction errors.

The error for an observation is the difference between the actual value and the predicted value.

RMSE gives greater weight to larger errors because the errors are squared before being averaged.

For this project, RMSE is measured in **wins**.

The results were:

| Model | RMSE |
|---|---:|
| Baseline | 11.78 wins |
| Linear Regression | 10.61 wins |

The regression model's lower RMSE indicates that its predictions were closer to the actual test-set win totals than the baseline predictions.

---

## R²

**R²**, or the coefficient of determination, describes how much of the variation in the target is explained by the model.

For this project, the linear regression model produced:

```text
R² = 0.186
```

This means that batting average explained about **18.6% of the variation in wins in the test data**.

The remaining variation is associated with other factors that are not included in this single-feature model.

R² should therefore be interpreted together with the other evidence rather than by itself.

---

## Residuals

A **residual** is the difference between an actual value and the value predicted by the model.

In this project:

```text
Residual = Actual Wins - Predicted Wins
```

A positive residual means the model predicted too few wins.

A negative residual means the model predicted too many wins.

The residual plot helps show whether the model's errors are small, large, or distributed in a particular pattern.

The project found substantial variation in residuals above and below zero, indicating that the model does not capture all of the factors associated with team win totals.

---

## Interpreting the Regression Line

The regression line slopes upward.

This indicates a positive relationship between batting average and regular-season wins in the selected data.

In general, teams with higher batting averages tended to have more wins.

However, the individual observations were spread out around the regression line.

This distinction is important:

> A relationship between two variables does not mean that one variable is sufficient to accurately predict the other.

The model provides useful information, but batting average alone does not provide a complete explanation of team wins.

---

## Correlation and Prediction

The project found a positive correlation between batting average and wins.

The correlation was approximately:

```text
0.360
```

This provides additional evidence of a positive relationship.

However, correlation and prediction are not the same thing.

A variable can have a measurable relationship with a target while still producing predictions with substantial error.

The regression results demonstrate this in the project: batting average provided useful information, but the model still left much of the variation in wins unexplained.

---

## Visualization

The project uses two primary visualizations.

### Prediction Plot

The prediction plot shows the relationship between batting average and regular-season wins along with the regression line.

It helps illustrate:

- The direction of the relationship.
- The spread of the observations.
- How closely observations follow the regression line.

### Residual Plot

The residual plot shows prediction errors.

It helps identify how much the actual observations differ from the model's predictions.

Together, these visualizations provide information that numerical metrics alone do not show.

---

## Model Limitations

This project uses only one feature:

```text
batting_avg
```

A team's win total depends on many aspects of baseball performance.

For example, additional offensive statistics, pitching, defense, baserunning, and other team characteristics may contain information about wins.

Because those variables are not included in this model, the regression should not be treated as a complete model of team success.

The relatively modest R² value provides quantitative evidence of this limitation.

---

## Relationship Does Not Mean Causation

The regression model describes a relationship in the historical data.

It does not establish that changing a team's batting average would necessarily cause a specific change in its number of wins.

The analysis is predictive and descriptive rather than a controlled experiment.

This distinction is important when interpreting machine learning results.

---

## Extending the Model

A natural next step would be to add additional team statistics as features.

Possible variables to investigate include:

- Runs
- Home runs
- Walks
- Stolen bases
- On-base percentage
- Slugging percentage

A multiple-feature regression model could then be compared with the current single-feature model.

The goal would be to determine whether additional information improves prediction accuracy.

---

## Key Takeaways

The main concepts demonstrated by this project are:

1. **Feature:** the input used for prediction.
2. **Target:** the value being predicted.
3. **Training data:** observations used to fit the model.
4. **Test data:** observations used to evaluate the model.
5. **Baseline:** a simple reference model.
6. **Linear regression:** a model that estimates a linear relationship between variables.
7. **Prediction:** the model's estimated target value.
8. **RMSE:** a measure of prediction error.
9. **R²:** a measure of variation explained by the model.
10. **Residuals:** differences between actual and predicted values.
11. **Visualization:** a way to examine relationships and errors.
12. **Model limitations:** factors that the selected features do not explain.

The overall result is that **batting average provides some predictive information about regular-season wins, but batting average alone is not enough to accurately predict a team's win total**.
