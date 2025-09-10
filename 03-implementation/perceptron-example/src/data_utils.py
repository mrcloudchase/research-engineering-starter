"""
Data utilities for perceptron research.

Provides functions to generate logic gate datasets and visualize decision boundaries.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Optional, Any
import seaborn as sns


def generate_logic_gate_data(gate_type: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate data for logic gate functions.
    
    Args:
        gate_type: Type of gate ('AND', 'OR', 'XOR', 'NAND', 'NOR')
        
    Returns:
        Tuple of (inputs, outputs) for the specified gate
    """
    # All logic gates use same input combinations
    X = np.array([[0, 0],
                  [0, 1],
                  [1, 0],
                  [1, 1]], dtype=float)
    
    # Define outputs for each gate type
    if gate_type.upper() == 'AND':
        y = np.array([0, 0, 0, 1], dtype=float)
    elif gate_type.upper() == 'OR':
        y = np.array([0, 1, 1, 1], dtype=float)
    elif gate_type.upper() == 'XOR':
        y = np.array([0, 1, 1, 0], dtype=float)
    elif gate_type.upper() == 'NAND':
        y = np.array([1, 1, 1, 0], dtype=float)
    elif gate_type.upper() == 'NOR':
        y = np.array([1, 0, 0, 0], dtype=float)
    else:
        raise ValueError(f"Unknown gate type: {gate_type}")
    
    return X, y


def visualize_decision_boundary(model: Any, 
                               X: np.ndarray, 
                               y: np.ndarray,
                               title: str = "Decision Boundary",
                               save_path: Optional[str] = None) -> None:
    """
    Visualize the decision boundary of a trained model.
    
    Args:
        model: Trained model with predict method
        X: Input data points
        y: Target labels
        title: Plot title
        save_path: Optional path to save the figure
    """
    # Set up the plot
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Create a mesh grid for the decision boundary
    h = 0.01  # Step size in the mesh
    x_min, x_max = -0.5, 1.5
    y_min, y_max = -0.5, 1.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    
    # Predict on the mesh grid
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    # Plot the decision boundary
    ax.contourf(xx, yy, Z, alpha=0.3, cmap='RdYlBu', levels=[0, 0.5, 1])
    ax.contour(xx, yy, Z, levels=[0.5], colors='black', linewidths=2, linestyles='--')
    
    # Plot the data points
    scatter = ax.scatter(X[:, 0], X[:, 1], c=y, s=200, 
                        cmap='RdYlBu', edgecolors='black', linewidth=2)
    
    # Add labels for each point
    for i, (x, y_val) in enumerate(zip(X, y)):
        ax.annotate(f'({int(x[0])},{int(x[1])})→{int(y_val)}',
                   xy=(x[0], x[1]), xytext=(5, 5),
                   textcoords='offset points', fontsize=10)
    
    # Formatting
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel('Input 1', fontsize=12)
    ax.set_ylabel('Input 2', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add colorbar
    plt.colorbar(scatter, ax=ax, label='Output')
    
    # Add model type annotation
    model_type = type(model).__name__
    ax.text(0.02, 0.98, f'Model: {model_type}',
           transform=ax.transAxes, fontsize=10,
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_training_history(history: dict, 
                         title: str = "Training History",
                         save_path: Optional[str] = None) -> None:
    """
    Plot training history (loss and accuracy over epochs).
    
    Args:
        history: Dictionary with 'loss' and 'accuracy' lists
        title: Plot title
        save_path: Optional path to save the figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    epochs = range(1, len(history['loss']) + 1)
    
    # Plot loss
    ax1.plot(epochs, history['loss'], 'b-', linewidth=2, label='Loss')
    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('Loss', fontsize=12)
    ax1.set_title('Training Loss', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot accuracy
    ax2.plot(epochs, history['accuracy'], 'g-', linewidth=2, label='Accuracy')
    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('Accuracy', fontsize=12)
    ax2.set_title('Training Accuracy', fontsize=14, fontweight='bold')
    ax2.set_ylim([0, 1.05])
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Add percentage labels on y-axis for accuracy
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
    
    plt.suptitle(title, fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def compare_models_on_gates(models: dict, gates: list = ['AND', 'OR', 'XOR']) -> dict:
    """
    Compare multiple models on different logic gates.
    
    Args:
        models: Dictionary of model_name: model pairs
        gates: List of gate types to test
        
    Returns:
        Dictionary of results
    """
    results = {}
    
    for gate in gates:
        X, y = generate_logic_gate_data(gate)
        results[gate] = {}
        
        for model_name, model in models.items():
            predictions = model.predict(X)
            accuracy = np.mean(predictions == y)
            results[gate][model_name] = accuracy
    
    return results


def plot_comparison_results(results: dict, save_path: Optional[str] = None) -> None:
    """
    Plot comparison results as a heatmap.
    
    Args:
        results: Dictionary of gate -> model -> accuracy
        save_path: Optional path to save the figure
    """
    # Convert results to matrix format
    gates = list(results.keys())
    models = list(results[gates[0]].keys())
    
    data = np.array([[results[gate][model] for model in models] for gate in gates])
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.heatmap(data, annot=True, fmt='.2%', cmap='RdYlGn',
                xticklabels=models, yticklabels=gates,
                vmin=0, vmax=1, cbar_kws={'label': 'Accuracy'},
                linewidths=1, linecolor='gray')
    
    ax.set_title('Model Performance on Logic Gates', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Model', fontsize=12)
    ax.set_ylabel('Logic Gate', fontsize=12)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()
