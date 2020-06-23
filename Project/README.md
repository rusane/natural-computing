# Project User Manual
This document contains information about the team's work on the TADPOLE Challenge. The project files include Jupyter notebooks which were used to conduct experiments and python scripts which were used to create global pipelines for model training and additional experiments

### Authors
Anna Gansen

Ajinkya Indulkar

Richard Li

### Packages Used:
* pandas (data manipulation)
* numpy (data manipulation)
* sklearn (model training)
* mlxtend (model training)
* matplotlib (visualization tool)
* seaborn (visualization tool)

## Project Description:
### Exploratory Data Analysis (EDA)
We initially conducted EDA on the TADPOLE dataset to observe relevant features, correlations and missing/corrupted data. We conducted this, including the correlation experiment, in [Exploratory Data Analysis.ipynb](https://github.com/rusane/natural-computing/blob/master/Project/Exploratory%20Data%20Analysis.ipynb). There also exists some discarded notebooks in the `legacy` folder of the project.

This notebook was used to create [tadpole.py](https://github.com/rusane/natural-computing/blob/master/Project/tadpole.py), a python script used for creating a pipeline for loading, cleaning and splitting dataset into train and test sets. It's also includes pipeline elements for grid search (including saving trained `sklearn` models).

### Base Learners + Grid Search
After EDA, we train our base learners in [Base Learners - Grid Search.ipynb](https://github.com/rusane/natural-computing/blob/master/Project/Base%20Learners%20-%20Grid%20Search.ipynb) and perform grid search to find optimal parameter grid.
We perform grid search of base learners using the data from correlation experiment in [Base Learners - Grid Search with Manual Feature Selection.ipynb](https://github.com/rusane/natural-computing/blob/master/Project/Base%20Learners%20-%20Grid%20Search%20with%20Manual%20Feature%20Selection.ipynb).
Finally, we perform grid search of base learners using the refit data from feature importance experiment in [Base Learners - Grid Search with Refit.ipynb](https://github.com/rusane/natural-computing/blob/master/Project/Base%20Learners%20-%20Grid%20Search%20with%20Refit.ipynb).

### Ensemble Learners + Grid Search
We performed the initial bagging experiments and later grid search in [Bagging.ipynb](https://github.com/rusane/natural-computing/blob/master/Project/Bagging.ipynb). We performed the initial boosting experiments and later grid search in [Boosting.ipynb](https://github.com/rusane/natural-computing/blob/master/Project/Boosting.ipynb). We performed the initial stacking experiments and later grid search in [Stacking.ipynb](https://github.com/rusane/natural-computing/blob/master/Project/Stacking.ipynb).

### Feature Importance Experiment
We performed feature selection via feature importance. We extract feature importance using Random Forests in [Feature Selection via Random Forests.ipynb](https://github.com/rusane/natural-computing/blob/master/Project/Feature%20Selection%20via%20Random%20Forests.ipynb). A `refit_data()` function is added to `tadpole.py` script to refit data based on `SelectFromModel` model created in this experiment, saved in the `models` folder of the project.

### Multiple Runs of Base and Ensemble Learners
So as to avoid any random seed bias, we perform the model training of base and ensemble learners (with their best parameters post-grid search) for 30 iterations. For base learners, we perform the runs on original dataset in [Base Learner Runs.ipynb](https://github.com/rusane/natural-computing/blob/master/Project/Base%20Learner%20Runs.ipynb), refit data from correlation experiment in [Base Learner Runs with Manual Feature Selection.ipynb](https://github.com/rusane/natural-computing/blob/master/Project/Base%20Learner%20Runs%20with%20Manual%20Feature%20Selection.ipynb) and refit data from feature importance experiment in [Base Learner Runs with Refit.ipynb](https://github.com/rusane/natural-computing/blob/master/Project/Base%20Learner%20Runs%20with%20Refit.ipynb).

We perform the same for bagging in [Bagging Runs.ipynb](https://github.com/rusane/natural-computing/blob/master/Project/Bagging%20Runs.ipynb), boosting in [Boosting Runs.ipynb](https://github.com/rusane/natural-computing/blob/master/Project/Boosting%20Runs.ipynb) and stacking in [Stacking Runs.ipynb](https://github.com/rusane/natural-computing/blob/master/Project/Stacking%20Runs.ipynb).

We created a few python scripts to act as pipeline elements for this experiment. [main.py](https://github.com/rusane/natural-computing/blob/master/Project/main.py) stores the best parameters from grid search experiments and contains the `run()` function which controls the number of iterations and returns the evaluation scores. [evaluator.py](https://github.com/rusane/natural-computing/blob/master/Project/evaluator.py) contains functions to perform evaluation of trained models and export results to a file of `CSV` format, saved in the `results` folder of the project. [classifier.py](https://github.com/rusane/natural-computing/blob/master/Project/classifier.py) defines the `Classifier` class which is an additional wrapper for training models and predicting results. 

### Comparative Analysis
We performed a comparative analysis between base learners trained on different datasets (original, refit from correlation and refit from feature importance) after the multiple runs experiment in [Comparative Analysis - Base Learners.ipynb](https://github.com/rusane/natural-computing/blob/master/Project/Comparative%20Analysis%20-%20Base%20Learners.ipynb).
Finally, we performed a comparative analysis between base learners and ensemble learners (with best parameters) after the multiple runs experiment in [Comparative Analysis - Base Learners vs Ensemble Methods.ipynb](https://github.com/rusane/natural-computing/blob/master/Project/Comparative%20Analysis%20-%20Base%20Learners%20vs%20Ensemble%20Methods.ipynb)