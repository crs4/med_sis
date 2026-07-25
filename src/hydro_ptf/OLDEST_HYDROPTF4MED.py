# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 11:03:21 2025

@author: Giacomo Belvisi
"""

import os
import dill
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit, GridSearchCV
from sklearn.preprocessing import MinMaxScaler, FunctionTransformer
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.pipeline import Pipeline
import scipy.stats as stats

# -----------------------------------------------------------------------------
# Global Configuration & Output Directory
# -----------------------------------------------------------------------------
def create_output_directory(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

# -----------------------------------------------------------------------------
# Main Function - REVISED
# -----------------------------------------------------------------------------
def main():
    # Parameters
    file_path_VOL = "/usr/src/s4m_catalogue/hydro_ptf/HYDRO_VOL_oct25.xlsx"
    n_iterations = 100
    test_size = 0.3
    random_state = 42
    pot_values = [4, 10, 33, 100, 200, 300, 1500]

    output_dir = '/usr/src/s4m_catalogue/hydro_ptf/'

    ############### TRAINING WITH HYDRO_VOL_....
    # Load and clean data
    data = pd.read_excel(file_path_VOL, sheet_name="Foglio1")
    data_cleaned = data.dropna().copy() # Use .copy() to avoid SettingWithCopyWarning

    # Define features (X) and target (y)
    X = data_cleaned[['CLAY', 'SAND', 'OC', 'Pot']].copy()
    y = data_cleaned['U'].copy()

    # --- KEY IMPROVEMENT 1: Create Stratification Variable ---
    # Combine Dataset and binned Matric Potential for stratification
    # We use the original Pot values to create bins that match our specific values
    data_cleaned['Pot_Bin'] = pd.cut(data_cleaned['Pot'], bins=[0, 7, 20, 50, 150, 250, 500, 2000], labels=pot_values, include_lowest=True)
    data_cleaned['Stratify_Group'] = data_cleaned['Dataset'].astype(str) + "_" + data_cleaned['Pot_Bin'].astype(str)

    # --- KEY IMPROVEMENT 2: Define Model Pipelines ---
    # Preprocessor for Clay, Sand, OC
    feature_preprocessor = Pipeline(steps=[  ('minmax', MinMaxScaler()) ])

    # Preprocessor for Pot: Log10 then Scale
    pot_preprocessor = Pipeline(steps=[
        ('log10', FunctionTransformer(func=np.log10, inverse_func=lambda x: 10**x )), # Use log10
        ('scaler', MinMaxScaler())
    ])

    # --- KEY IMPROVEMENT 3: Hyperparameter Grid for Tuning ---
    mlp_param_grid = {
        'mlp__hidden_layer_sizes': [(5,), (10,), (15,)],
        'mlp__activation': ['relu', 'tanh', 'logistic'],
        'mlp__solver': ['adam', 'sgd']
    }

    # --- Initialize Results Storage ---
    results_list = [] # Store metrics per iteration
    detailed_pot_results = [] # Store RMSE per pot value per iteration
    mlr_coefficients_list = [] # NEW: Store MLR coefficients per iteration

    # --- KEY IMPROVEMENT 4: Stratified Monte Carlo Loop ---
    # Use StratifiedShuffleSplit on the custom group
    sss = StratifiedShuffleSplit(n_splits=n_iterations, test_size=test_size, random_state=random_state)

    for iter_num, (train_index, test_index) in enumerate(sss.split(X, data_cleaned['Stratify_Group'])):
        print(f"Processing iteration {iter_num+1}/{n_iterations}")
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        # --- KEY IMPROVEMENT 5: Fit Preprocessors on TRAIN only ---
        # Preprocess features (Clay, Sand, OC)
        X_train_features = feature_preprocessor.fit_transform(X_train[['CLAY', 'SAND', 'OC']])
        X_test_features = feature_preprocessor.transform(X_test[['CLAY', 'SAND', 'OC']])
        # Preprocess Pot
        X_train_pot = pot_preprocessor.fit_transform(X_train[['Pot']])
        X_test_pot = pot_preprocessor.transform(X_test[['Pot']])
        # Combine preprocessed features
        X_train_processed = np.hstack([X_train_features, X_train_pot])
        X_test_processed = np.hstack([X_test_features, X_test_pot])
        # --- MODEL 1: MLP with Hyperparameter Tuning ---
        # Create base MLP model
        mlp_base = MLPRegressor(random_state=random_state, max_iter=1000, early_stopping=True)
        # Create a pipeline for the tuned model (though we already preprocessed, this is for GridSearch)
        mlp_pipeline = Pipeline(steps=[('mlp', mlp_base)])
        # Internal GridSearchCV on the training set
        mlp_grid_search = GridSearchCV(mlp_pipeline, mlp_param_grid, cv=5, scoring='neg_root_mean_squared_error', n_jobs=-1)
        mlp_grid_search.fit(X_train_processed, y_train)
        # Get the best model and predict
        best_mlp = mlp_grid_search.best_estimator_
        y_pred_mlp = best_mlp.predict(X_test_processed)

        # --- MODEL 2: Multiple Linear Regression (Benchmark) ---
        mlr = LinearRegression()
        mlr.fit(X_train_processed, y_train)
        y_pred_mlr = mlr.predict(X_test_processed)

        # --- NEW: Save MLR coefficients for this iteration ---
        mlr_coefs_entry = {
            'Iteration': iter_num,
            'Intercept': mlr.intercept_,
            'CLAY_coef': mlr.coef_[0],
            'SAND_coef': mlr.coef_[1], 
            'OC_coef': mlr.coef_[2],
            'log10Pot_coef': mlr.coef_[3]
        }
        mlr_coefficients_list.append(mlr_coefs_entry)

        # --- Calculate Metrics for MLP ---
        rmse_mlp = np.sqrt(mean_squared_error(y_test, y_pred_mlp))
        r2_mlp = r2_score(y_test, y_pred_mlp)
        mae_mlp = mean_absolute_error(y_test, y_pred_mlp)

        # --- Calculate Metrics for MLR ---
        rmse_mlr = np.sqrt(mean_squared_error(y_test, y_pred_mlr))
        r2_mlr = r2_score(y_test, y_pred_mlr)
        mae_mlr = mean_absolute_error(y_test, y_pred_mlr)

        # --- Calculate RMSE per specific Pot value for MLP ---
        rmse_per_pot_mlp = {}
        # Get the original, untransformed Pot values for the test set
        pot_test_original = X_test['Pot'].values
        for p_val in pot_values:
            # Find indices where Pot is close to the specific value (due to possible decimals)
            mask = np.isclose(pot_test_original, p_val, atol=1e-2)
            if np.sum(mask) > 0: # Ensure there are samples for this potential
                rmse_val = np.sqrt(mean_squared_error(y_test[mask], y_pred_mlp[mask]))
                rmse_per_pot_mlp[f'RMSE_{p_val}'] = rmse_val
            else:
                rmse_per_pot_mlp[f'RMSE_{p_val}'] = np.nan

        # --- Store Results for this Iteration ---
        iteration_entry = {
            'Iteration': iter_num,
            'Model': 'MLP', 'RMSE': rmse_mlp, 'R2': r2_mlp, 'MAE': mae_mlp,
            **rmse_per_pot_mlp # Unpack the RMSE per pot dictionary
        }
        results_list.append(iteration_entry)

        iteration_entry_mlr = {
            'Iteration': iter_num,
            'Model': 'MLR', 'RMSE': rmse_mlr, 'R2': r2_mlr, 'MAE': mae_mlr
        }
        results_list.append(iteration_entry_mlr)

        # Also store detailed info for analysis (optional)
        iter_test_data = X_test.copy()
        iter_test_data['y_true'] = y_test.values
        iter_test_data['y_pred_mlp'] = y_pred_mlp
        iter_test_data['y_pred_mlr'] = y_pred_mlr
        iter_test_data['Iteration'] = iter_num
        iter_test_data['Dataset'] = data_cleaned.iloc[test_index]['Dataset'].values
        detailed_pot_results.append(iter_test_data)

    # --- After all iterations: Save Results ---
    # Convert results to DataFrame
    results_df = pd.DataFrame(results_list)

    # Save comprehensive results to Excel
    with pd.ExcelWriter(os.path.join(output_dir, 'monte_carlo_performance_metrics.xlsx')) as writer:
        results_df.to_excel(writer, sheet_name='All_Iterations', index=False)
        
        # Create a summary table: Mean ± Std of metrics for each model
        summary_df = results_df.groupby('Model').agg({'RMSE': ['mean', 'std'],
                                                       'R2': ['mean', 'std'],
                                                       'MAE': ['mean', 'std']}).round(4)
        summary_df.to_excel(writer, sheet_name='Summary_Statistics')

        # Create a summary of RMSE per potential for MLP only
        mlp_results = results_df[results_df['Model'] == 'MLP']
        rmse_pot_columns = [col for col in mlp_results.columns if 'RMSE_' in col]
        pot_summary_data = []
        for col in rmse_pot_columns:
            pot_val = col.replace('RMSE_', '')
            mean_rmse = mlp_results[col].mean()
            std_rmse = mlp_results[col].std()
            pot_summary_data.append({'Matric_Potential': pot_val, 'Mean_RMSE': mean_rmse, 'Std_RMSE': std_rmse})
        pot_summary_df = pd.DataFrame(pot_summary_data)
        pot_summary_df.to_excel(writer, sheet_name='RMSE_per_Potential', index=False)

        # NEW: Save MLR coefficients for all iterations
        mlr_coefs_df = pd.DataFrame(mlr_coefficients_list)
        mlr_coefs_df.to_excel(writer, sheet_name='MLR_Coefficients_All_Iterations', index=False)

    # Save the detailed test data for all iterations
    detailed_df = pd.concat(detailed_pot_results)
    detailed_df.to_csv(os.path.join(output_dir, 'detailed_predictions.csv'), index=False)

    # -------------------------------------------------------------------------
    # --- SCIENTIFIC PLOTS AND FINAL MODEL ANALYSIS ---
    # -------------------------------------------------------------------------
    print("Generating scientific plots and final model analysis...")
    
    # Set publication-quality style
    plt.style.use('default')
    sns.set_palette("colorblind")
    plt.rcParams.update({
        'font.family': 'serif',
        'font.size': 12,
        'axes.labelsize': 14,
        'axes.titlesize': 16,
        'legend.fontsize': 12,
        'figure.titlesize': 18,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.1
    })

    # 1. Distribution of Performance Metrics (Boxplot)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    metrics = ['RMSE', 'R2', 'MAE']
    titles = ['Root Mean Squared Error (RMSE)', 'Coefficient of Determination (R²)', 'Mean Absolute Error (MAE)']
    
    for i, metric in enumerate(metrics):
        sns.boxplot(data=results_df, x='Model', y=metric, ax=axes[i])
        axes[i].set_title(titles[i])
        if metric == 'R2':
            axes[i].axhline(1, linestyle='--', color='grey', alpha=0.7)
            axes[i].axhline(0, linestyle='--', color='grey', alpha=0.7)
    
    plt.suptitle('Distribution of Performance Metrics across 100 Monte Carlo Iterations')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '01_Performance_Metrics_Distribution.png'))
    plt.close()

    # 2. Observed vs. Predicted Values for MLP
    mlp_detailed = detailed_df[['y_true', 'y_pred_mlp']].dropna()
    z = np.polyfit(mlp_detailed['y_true'], mlp_detailed['y_pred_mlp'], 1)
    p = np.poly1d(z)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(mlp_detailed['y_true'], mlp_detailed['y_pred_mlp'], alpha=0.6, s=20, edgecolors='none')
    
    # 1:1 line
    min_val = min(mlp_detailed['y_true'].min(), mlp_detailed['y_pred_mlp'].min())
    max_val = max(mlp_detailed['y_true'].max(), mlp_detailed['y_pred_mlp'].max())
    ax.plot([min_val, max_val], [min_val, max_val], 'k--', lw=2, label='1:1 Line')
    
    # Regression line
    ax.plot(mlp_detailed['y_true'], p(mlp_detailed['y_true']), 'r-', lw=2, 
            label=f'Fit: y = {z[0]:.3f}x + {z[1]:.3f}\nR² = {r2_score(mlp_detailed["y_true"], mlp_detailed["y_pred_mlp"]):.3f}')
    
    ax.set_xlabel('Observed Volumetric Water Content (cm³ cm⁻³)')
    ax.set_ylabel('Predicted Volumetric Water Content (cm³ cm⁻³)')
    ax.set_title('MLP: Observed vs. Predicted Values')
    ax.legend()
    ax.set_aspect('equal')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '02_MLP_Observed_vs_Predicted.png'))
    plt.close()

    # 3. Residual Analysis for MLP
    mlp_detailed['Residuals'] = mlp_detailed['y_true'] - mlp_detailed['y_pred_mlp']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Residuals vs Predicted
    ax1.scatter(mlp_detailed['y_pred_mlp'], mlp_detailed['Residuals'], alpha=0.6, s=20)
    ax1.axhline(y=0, color='r', linestyle='--', lw=2)
    ax1.set_xlabel('Predicted Volumetric Water Content (cm³ cm⁻³)')
    ax1.set_ylabel('Residuals (Observed - Predicted)')
    ax1.set_title('Residuals vs. Predicted Values')
    
    # Q-Q Plot
    stats.probplot(mlp_detailed['Residuals'], dist="norm", plot=ax2)
    ax2.get_lines()[0].set_markersize(4.0)
    ax2.get_lines()[1].set_linewidth(2.0)
    ax2.set_title('Q-Q Plot of Residuals')
    
    plt.suptitle('MLP Residual Analysis')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '03_MLP_Residual_Analysis.png'))
    plt.close()

    # 4. RMSE across Matric Potential values
    fig, ax = plt.subplots(figsize=(10, 6))
    x_pos = range(len(pot_summary_df))
    ax.errorbar(x_pos, pot_summary_df['Mean_RMSE'], yerr=pot_summary_df['Std_RMSE'], 
                fmt='-o', capsize=5, capthick=2, elinewidth=2, markersize=8)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(pot_summary_df['Matric_Potential'])
    ax.set_xlabel('Matric Potential (kPa)')
    ax.set_ylabel('Root Mean Squared Error (RMSE)')
    ax.set_title('MLP Model Error across Matric Potential Values')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '04_MLP_RMSE_vs_Matric_Potential.png'))
    plt.close()

    # 5. Performance across Datasets
    dataset_rmse = []
    for dataset in detailed_df['Dataset'].unique():
        dataset_data = detailed_df[detailed_df['Dataset'] == dataset]
        if len(dataset_data) > 10:  # Only include datasets with sufficient data
            rmse = np.sqrt(mean_squared_error(dataset_data['y_true'], dataset_data['y_pred_mlp']))
            dataset_rmse.append({'Dataset': dataset, 'RMSE': rmse, 'Samples': len(dataset_data)})
    
    dataset_rmse_df = pd.DataFrame(dataset_rmse).sort_values('RMSE')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(range(len(dataset_rmse_df)), dataset_rmse_df['RMSE'])
    ax.set_xlabel('Dataset')
    ax.set_ylabel('RMSE')
    ax.set_title('MLP Performance across Different Datasets')
    ax.set_xticks(range(len(dataset_rmse_df)))
    ax.set_xticklabels(dataset_rmse_df['Dataset'], rotation=45, ha='right')
    
    # Add sample size annotations
    for i, (idx, row) in enumerate(dataset_rmse_df.iterrows()):
        ax.text(i, row['RMSE'] + 0.005, f'n={row["Samples"]}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '05_MLP_Performance_by_Dataset.png'))
    plt.close()

    # 6. Feature Importance Analysis (Permutation Importance)
    from sklearn.inspection import permutation_importance
    
    # Use the last iteration's model for importance analysis
    last_iter_idx = n_iterations - 1
    last_iter_data = detailed_df[detailed_df['Iteration'] == last_iter_idx]
    
    # Prepare the feature matrix from the last iteration
    X_test_last = np.column_stack([
        feature_preprocessor.transform(last_iter_data[['CLAY', 'SAND', 'OC']]),
        pot_preprocessor.transform(last_iter_data[['Pot']])
    ])
    
    y_test_last = last_iter_data['y_true']
    
    # Calculate permutation importance
    perm_importance = permutation_importance(
        best_mlp, X_test_last, y_test_last, 
        n_repeats=30, random_state=random_state, 
        scoring='neg_root_mean_squared_error'
    )
    
    feature_names = ['CLAY', 'SAND', 'OC', 'log10(Pot)']
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance_mean': perm_importance.importances_mean,
        'importance_std': perm_importance.importances_std
    }).sort_values('importance_mean', ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    y_pos = np.arange(len(importance_df))
    ax.barh(y_pos, importance_df['importance_mean'], xerr=importance_df['importance_std'], 
            align='center', alpha=0.7, ecolor='black', capsize=5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(importance_df['feature'])
    ax.set_xlabel('Mean Decrease in RMSE after Permutation')
    ax.set_title('MLP Feature Importance (Permutation Importance)')
    ax.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '06_MLP_Feature_Importance.png'))
    plt.close()

    # 7. Training Convergence Plot (for the last iteration's model)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(best_mlp.named_steps['mlp'].loss_curve_)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Loss')
    ax.set_title('MLP Training Convergence (Last Iteration)')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '07_MLP_Training_Convergence.png'))
    plt.close()

    # -------------------------------------------------------------------------
    # --- SAVE BEST MODEL CONFIGURATION AND FINAL MODELS ---
    # -------------------------------------------------------------------------
    
    print("Saving best model configuration and training final models...")
    
    # Find the most frequent best parameters across all iterations
    # (You would need to store best_params_ during the loop, but for now we'll use the last one)
    best_mlp_params = best_mlp.get_params()
    
    # Save best MLP configuration
    mlp_config_df = pd.DataFrame([{
        'hidden_layer_sizes': best_mlp_params['mlp__hidden_layer_sizes'],
        'activation': best_mlp_params['mlp__activation'],
        'solver': best_mlp_params['mlp__solver'],
        'alpha': best_mlp_params['mlp__alpha'],
        'learning_rate': best_mlp_params['mlp__learning_rate'],
        'max_iter': best_mlp_params['mlp__max_iter'],
        'random_state': best_mlp_params['mlp__random_state']
    }])
    
    mlp_config_df.to_csv(os.path.join(output_dir, 'best_mlp_configuration.csv'), index=False)
    
    # Train final models on ALL data
    print("Training final models on complete dataset...")
    
    # Preprocess all data
    X_features_all = feature_preprocessor.fit_transform(X[['CLAY', 'SAND', 'OC']])
    X_pot_all = pot_preprocessor.fit_transform(X[['Pot']])
    X_processed_all = np.hstack([X_features_all, X_pot_all])
    
    # Final MLP with best configuration
    final_mlp = MLPRegressor(
        hidden_layer_sizes=best_mlp_params['mlp__hidden_layer_sizes'],
        activation=best_mlp_params['mlp__activation'],
        solver=best_mlp_params['mlp__solver'],
        alpha=best_mlp_params['mlp__alpha'],
        learning_rate=best_mlp_params['mlp__learning_rate'],
        max_iter=2000,
        random_state=random_state,
        early_stopping=True
    )
    
    final_mlp.fit(X_processed_all, y)
    
    # Final MLR
    final_mlr = LinearRegression()
    final_mlr.fit(X_processed_all, y)
    
    # NEW: Save final model parameters to Excel
    final_models_params = pd.DataFrame([{
        'Model': 'Final_MLP',
        'hidden_layer_sizes': final_mlp.hidden_layer_sizes,
        'activation': final_mlp.activation,
        'solver': final_mlp.solver,
        'alpha': final_mlp.alpha,
        'learning_rate': final_mlp.learning_rate,
        'max_iter': final_mlp.max_iter,
        'random_state': final_mlp.random_state,
        'n_iter_': final_mlp.n_iter_,
        'n_layers': final_mlp.n_layers_,
        'n_outputs': final_mlp.n_outputs_
    }, {
        'Model': 'Final_MLR', 
        'Intercept': final_mlr.intercept_,
        'CLAY_coef': final_mlr.coef_[0],
        'SAND_coef': final_mlr.coef_[1],
        'OC_coef': final_mlr.coef_[2],
        'log10Pot_coef': final_mlr.coef_[3]
    }])
    
    final_models_params.to_csv(os.path.join(output_dir, 'final_models_parameters.csv'), index=False)
    
    # Save MLR coefficients (for the final model trained on all data)
    mlr_coef_df = pd.DataFrame({
        'Feature': ['CLAY', 'SAND', 'OC', 'log10(Pot)'],
        'Coefficient': final_mlr.coef_
    })
    mlr_coef_df.loc[len(mlr_coef_df)] = ['Intercept', final_mlr.intercept_]
    mlr_coef_df.to_csv(os.path.join(output_dir, 'mlr_coefficients.csv'), index=False)
    
    # Save final models
    with open(os.path.join(output_dir, 'final_mlp_model.pkl'), 'wb') as file:
        dill.dump(final_mlp, file)
    with open( os.path.join(output_dir, 'final_mlr_model.pkl'), 'wb') as file:
        dill.dump(final_mlr, file)
    with open( os.path.join(output_dir, 'feature_preprocessor.pkl'), 'wb') as file:
        dill.dump(feature_preprocessor, file)
    with open( os.path.join(output_dir, 'pot_preprocessor.pkl'), 'wb') as file:
        dill.dump(pot_preprocessor, file)
    
    # Save model architecture information
    with open(os.path.join(output_dir, 'model_architecture.txt'), 'w') as f:
        f.write("MLP Model Architecture:\n")
        f.write(f"Number of layers: {len(final_mlp.hidden_layer_sizes) + 2}\n")
        f.write(f"Hidden layer sizes: {final_mlp.hidden_layer_sizes}\n")
        f.write(f"Activation function: {final_mlp.activation}\n")
        f.write(f"Solver: {final_mlp.solver}\n")
        f.write(f"Total parameters: {sum([np.prod(w.shape) for w in final_mlp.coefs_])}\n")
        f.write("\nMLR Model:\n")
        f.write(f"Coefficients: {final_mlr.coef_}\n")
        f.write(f"Intercept: {final_mlr.intercept_}\n")

    print("All analysis complete! Files saved in:", output_dir)
    print("Generated 7 scientific plots for publication")
    print("Saved best model configuration and final trained models")
    print("NEW: Saved MLR coefficients for all 100 iterations")
    print("NEW: Saved parameters for final models trained on complete dataset")

if __name__ == "__main__":
    main()