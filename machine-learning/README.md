# Results

## Train
| Model|Accuracy|Precision|Recall|
|---|---|---|---|
| Support Vector Machine|0.34|0.48|0.34|
| K-Nearest Neighbors|0.39|0.42|0.39|
| Decision Tree|0.35|0.40|0.35|
| Random Forests|0.34|0.52|0.34|

## Test
| Model|Accuracy|Precision|Recall|
|---|---|---|---|
| Support Vector Machine|0.25|0.41|0.25|
| K-Nearest Neighbors|0.19|0.19|0.19|
| Decision Tree|0.30|0.38|0.30|
| Random Forests|0.25|0.42|0.25|

## Prediction on custom data
Given the following:
Maintenance = High
Number of doors = 4
Lug Boot Size = Big
Safety = High
Class Value = Good

**Decision Tree Model predicts 'med' buying_price!**

# Prerequisites
- Anaconda

# Technologies
- pandas
- scikit-learn

# Setup
1. Create new Conda environment
    ```
    conda env create -f environment.yml
    ```
2. Activate Conda environment
    ```
    conda activate cars
    ```

# Run
1. Start Jupyter Notebook server
    ```
    jupyter notebook
    ```