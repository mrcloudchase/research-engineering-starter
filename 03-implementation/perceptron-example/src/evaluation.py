"""
Evaluation utilities for perceptron research experiments.

Provides functions for systematic evaluation and statistical analysis.
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional
import time
from scipy import stats


def evaluate_model(model: Any, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
    """
    Evaluate a model's performance on given data.
    
    Args:
        model: Trained model with predict method
        X: Input data
        y: Target labels
        
    Returns:
        Dictionary of evaluation metrics
    """
    predictions = model.predict(X)
    
    # Calculate metrics
    accuracy = np.mean(predictions == y)
    
    # Calculate confusion matrix elements
    true_positives = np.sum((predictions == 1) & (y == 1))
    true_negatives = np.sum((predictions == 0) & (y == 0))
    false_positives = np.sum((predictions == 1) & (y == 0))
    false_negatives = np.sum((predictions == 0) & (y == 1))
    
    # Calculate additional metrics
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'true_positives': true_positives,
        'true_negatives': true_negatives,
        'false_positives': false_positives,
        'false_negatives': false_negatives
    }


def run_experiment(model_class: type,
                  model_params: dict,
                  X_train: np.ndarray,
                  y_train: np.ndarray,
                  X_test: np.ndarray,
                  y_test: np.ndarray,
                  training_params: dict,
                  n_runs: int = 10,
                  random_seeds: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    Run multiple experimental trials with different random seeds.
    
    Args:
        model_class: Class of the model to instantiate
        model_params: Parameters for model initialization
        X_train: Training data
        y_train: Training labels
        X_test: Test data
        y_test: Test labels
        training_params: Parameters for fit method
        n_runs: Number of experimental runs
        random_seeds: Optional list of random seeds
        
    Returns:
        Dictionary containing experimental results and statistics
    """
    if random_seeds is None:
        random_seeds = list(range(42, 42 + n_runs))
    
    results = {
        'accuracies': [],
        'precisions': [],
        'recalls': [],
        'f1_scores': [],
        'training_times': [],
        'final_epochs': [],
        'converged': [],
        'histories': []
    }
    
    for seed in random_seeds[:n_runs]:
        # Initialize model with seed
        params = model_params.copy()
        params['random_seed'] = seed
        model = model_class(**params)
        
        # Train model
        start_time = time.time()
        model.fit(X_train, y_train, **training_params)
        training_time = time.time() - start_time
        
        # Evaluate on test set
        metrics = evaluate_model(model, X_test, y_test)
        
        # Store results
        results['accuracies'].append(metrics['accuracy'])
        results['precisions'].append(metrics['precision'])
        results['recalls'].append(metrics['recall'])
        results['f1_scores'].append(metrics['f1_score'])
        results['training_times'].append(training_time)
        results['final_epochs'].append(len(model.history['accuracy']))
        results['converged'].append(metrics['accuracy'] == 1.0)
        results['histories'].append(model.history)
    
    # Calculate statistics
    results['statistics'] = {
        'accuracy': {
            'mean': np.mean(results['accuracies']),
            'std': np.std(results['accuracies']),
            'min': np.min(results['accuracies']),
            'max': np.max(results['accuracies']),
            'median': np.median(results['accuracies'])
        },
        'training_time': {
            'mean': np.mean(results['training_times']),
            'std': np.std(results['training_times']),
            'min': np.min(results['training_times']),
            'max': np.max(results['training_times'])
        },
        'convergence_rate': np.mean(results['converged']),
        'avg_epochs_to_converge': np.mean(results['final_epochs'])
    }
    
    return results


def compare_architectures(architectures: Dict[str, List[int]],
                         X: np.ndarray,
                         y: np.ndarray,
                         n_runs: int = 10) -> Dict[str, Any]:
    """
    Compare different multi-layer perceptron architectures.
    
    Args:
        architectures: Dictionary of architecture_name: layer_sizes
        X: Input data
        y: Target labels
        n_runs: Number of runs per architecture
        
    Returns:
        Comparison results
    """
    from .multi_layer_perceptron import MultiLayerPerceptron
    
    results = {}
    
    for arch_name, layer_sizes in architectures.items():
        print(f"Testing architecture: {arch_name} - {layer_sizes}")
        
        exp_results = run_experiment(
            model_class=MultiLayerPerceptron,
            model_params={'layer_sizes': layer_sizes, 'activation': 'sigmoid'},
            X_train=X,
            y_train=y,
            X_test=X,
            y_test=y,
            training_params={'epochs': 1000, 'verbose': False},
            n_runs=n_runs
        )
        
        results[arch_name] = exp_results
    
    return results


def statistical_hypothesis_test(results1: List[float], 
                               results2: List[float],
                               test_type: str = 'paired') -> Dict[str, float]:
    """
    Perform statistical hypothesis testing between two sets of results.
    
    Args:
        results1: First set of results
        results2: Second set of results
        test_type: Type of test ('paired' or 'independent')
        
    Returns:
        Dictionary with test statistics and p-value
    """
    if test_type == 'paired':
        # Paired t-test for dependent samples
        statistic, p_value = stats.ttest_rel(results1, results2)
    else:
        # Independent t-test
        statistic, p_value = stats.ttest_ind(results1, results2)
    
    # Calculate effect size (Cohen's d)
    mean_diff = np.mean(results1) - np.mean(results2)
    pooled_std = np.sqrt((np.var(results1) + np.var(results2)) / 2)
    cohens_d = mean_diff / pooled_std if pooled_std > 0 else 0
    
    return {
        'statistic': statistic,
        'p_value': p_value,
        'cohens_d': cohens_d,
        'mean_diff': mean_diff,
        'significant': p_value < 0.05
    }


def generate_experiment_report(experiment_name: str,
                              hypothesis: str,
                              results: Dict[str, Any],
                              save_path: Optional[str] = None) -> str:
    """
    Generate a formatted experiment report.
    
    Args:
        experiment_name: Name of the experiment
        hypothesis: Hypothesis being tested
        results: Experimental results
        save_path: Optional path to save the report
        
    Returns:
        Formatted report string
    """
    report = f"""
# Experiment: {experiment_name}
Date: {time.strftime('%Y-%m-%d %H:%M:%S')}

## Hypothesis
{hypothesis}

## Results Summary

### Performance Metrics
- **Mean Accuracy**: {results['statistics']['accuracy']['mean']:.2%} ± {results['statistics']['accuracy']['std']:.2%}
- **Min/Max Accuracy**: {results['statistics']['accuracy']['min']:.2%} / {results['statistics']['accuracy']['max']:.2%}
- **Median Accuracy**: {results['statistics']['accuracy']['median']:.2%}

### Training Statistics
- **Mean Training Time**: {results['statistics']['training_time']['mean']:.3f}s ± {results['statistics']['training_time']['std']:.3f}s
- **Convergence Rate**: {results['statistics']['convergence_rate']:.2%}
- **Average Epochs to Converge**: {results['statistics']['avg_epochs_to_converge']:.1f}

### Individual Run Results
"""
    
    for i, acc in enumerate(results['accuracies']):
        report += f"Run {i+1}: Accuracy = {acc:.2%}, Time = {results['training_times'][i]:.3f}s, Converged = {results['converged'][i]}\n"
    
    report += f"""
## Conclusion
The experiment {'SUPPORTS' if results['statistics']['accuracy']['mean'] > 0.9 else 'DOES NOT SUPPORT'} the hypothesis.
"""
    
    if save_path:
        with open(save_path, 'w') as f:
            f.write(report)
    
    return report
