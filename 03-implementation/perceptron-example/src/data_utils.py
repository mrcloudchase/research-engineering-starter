"""
Data Utilities for Logic Gate Experiments

Generate data for testing perceptron capabilities on logic gates,
particularly focusing on the XOR problem that reveals fundamental limitations.
"""

import numpy as np
from typing import Tuple, Dict, Optional
import matplotlib.pyplot as plt


def generate_logic_gate_data(gate: str = 'XOR') -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate input-output pairs for logic gates.
    
    Args:
        gate: Type of logic gate ('AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR')
        
    Returns:
        X: Input patterns (4, 2)
        y: Output labels (4,)
    """
    # All possible 2-bit inputs
    X = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ], dtype=np.float32)
    
    # Define outputs for each gate
    gates = {
        'AND':  np.array([0, 0, 0, 1]),
        'OR':   np.array([0, 1, 1, 1]),
        'XOR':  np.array([0, 1, 1, 0]),
        'NAND': np.array([1, 1, 1, 0]),
        'NOR':  np.array([1, 0, 0, 0]),
        'XNOR': np.array([1, 0, 0, 1])
    }
    
    if gate not in gates:
        raise ValueError(f"Unknown gate: {gate}. Choose from {list(gates.keys())}")
    
    y = gates[gate]
    
    return X, y


def visualize_logic_gate(gate: str = 'XOR', ax: Optional[plt.Axes] = None) -> plt.Axes:
    """
    Visualize a logic gate's input-output mapping.
    
    Args:
        gate: Type of logic gate
        ax: Matplotlib axes (creates new if None)
        
    Returns:
        Matplotlib axes with visualization
    """
    X, y = generate_logic_gate_data(gate)
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6))
    
    # Plot points
    colors = ['red' if yi == 0 else 'blue' for yi in y]
    ax.scatter(X[:, 0], X[:, 1], c=colors, s=200, edgecolors='black', linewidth=2)
    
    # Add labels
    for i, (x1, x2) in enumerate(X):
        label = f"({int(x1)},{int(x2)})→{y[i]}"
        ax.annotate(label, (x1, x2), xytext=(5, 5), textcoords='offset points')
    
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_xlabel("Input 1", fontsize=12)
    ax.set_ylabel("Input 2", fontsize=12)
    ax.set_title(f"{gate} Gate", fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add legend
    ax.scatter([], [], c='red', s=100, label='Output = 0')
    ax.scatter([], [], c='blue', s=100, label='Output = 1')
    ax.legend(loc='upper right')
    
    return ax


def analyze_linear_separability() -> Dict[str, bool]:
    """
    Analyze which logic gates are linearly separable.
    
    Returns:
        Dictionary mapping gate names to separability status
    """
    results = {}
    
    # Linearly separable gates (can be solved by single-layer perceptron)
    linearly_separable = ['AND', 'OR', 'NAND', 'NOR']
    
    # Non-linearly separable gates (require multi-layer networks)
    non_linearly_separable = ['XOR', 'XNOR']
    
    all_gates = linearly_separable + non_linearly_separable
    
    for gate in all_gates:
        results[gate] = gate in linearly_separable
    
    return results


def visualize_all_logic_gates():
    """
    Create a comprehensive visualization of all logic gates.
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle("Logic Gates: Linear Separability Challenge", fontsize=16, fontweight='bold')
    
    gates = ['AND', 'OR', 'NAND', 'NOR', 'XOR', 'XNOR']
    separability = analyze_linear_separability()
    
    for ax, gate in zip(axes.flat, gates):
        visualize_logic_gate(gate, ax)
        
        # Add separability indicator
        if separability[gate]:
            ax.set_facecolor('#e8f5e9')  # Light green for separable
            status = "✓ Linearly Separable"
            color = 'green'
        else:
            ax.set_facecolor('#ffebee')  # Light red for non-separable
            status = "✗ NOT Linearly Separable"
            color = 'red'
        
        ax.text(0.5, -0.3, status, transform=ax.transAxes,
                ha='center', fontsize=11, color=color, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    # Print analysis
    print("=" * 60)
    print("LOGIC GATE LINEAR SEPARABILITY ANALYSIS")
    print("=" * 60)
    
    print("\n✓ LINEARLY SEPARABLE (Single-layer perceptron can solve):")
    for gate, is_sep in separability.items():
        if is_sep:
            print(f"  - {gate}: Can draw a single line to separate outputs")
    
    print("\n✗ NON-LINEARLY SEPARABLE (Requires multi-layer network):")
    for gate, is_sep in separability.items():
        if not is_sep:
            print(f"  - {gate}: Need curved or multiple lines to separate")
    
    print("\n" + "=" * 60)
    print("KEY INSIGHT: XOR and XNOR require hidden layers because")
    print("they need to combine multiple decision boundaries.")
    print("=" * 60)


def generate_extended_xor_data(n_samples: int = 100, noise: float = 0.1, 
                               random_state: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate noisy XOR data for more realistic testing.
    
    Args:
        n_samples: Number of samples to generate
        noise: Standard deviation of Gaussian noise
        random_state: Random seed for reproducibility
        
    Returns:
        X: Input features with noise
        y: XOR labels
    """
    if random_state is not None:
        np.random.seed(random_state)
    
    # Generate random points in [0, 1] x [0, 1]
    X = np.random.rand(n_samples, 2)
    
    # Add noise
    X += np.random.randn(n_samples, 2) * noise
    
    # Compute XOR: output is 1 if inputs are in different halves
    y = ((X[:, 0] > 0.5) != (X[:, 1] > 0.5)).astype(int)
    
    return X, y


if __name__ == "__main__":
    # Demonstrate the visualizations
    print("Generating logic gate visualizations...")
    visualize_all_logic_gates()
    
    # Test data generation
    print("\nTesting data generation:")
    for gate in ['AND', 'OR', 'XOR']:
        X, y = generate_logic_gate_data(gate)
        print(f"\n{gate} Gate:")
        print(f"Inputs:\n{X}")
        print(f"Outputs: {y}")
