# Model optimization

The scripts in this folder are used for model optimization: feature selection and hyperparameter tuning. Here, I describe them in the order they should be used.

1. ```corr_matrix``` creates correlation matrices for airborne, tower and merged datasets
2. ```corr_pearson``` computes the pearson correlation for every feature with response variable CO2 flux, and produces a plot visualizing this.
3. ```xgboost_feature_importance``` computes the XGBoost feauture importances of the features in all three datasets, and produces a plot visualizing this.

Based on the correlation and the XGBoost feature importance, a pre-selection of features is chosen that continues to the next step: sequential backward floating selection (SBFS).

4. ```seq_backw_feat_sel_sbfs``` performs SBFS on the pre-selected features, for all three datasets. This results in a dataframe with all obtained metrics, for every subset of features that was run.
5. ```analyse_metrics_sbfs``` analyses these metrics, and creates a plot visualizing the results. Based on this, the optimal features are chosen. 
6. ```hyperparam_tuning``` uses these optimal features to perform hyperparameter tuning in a grid-mannered way, with GridSearchCV. Again, this is done for all models separately. This results in the optimal hyperparameters.

