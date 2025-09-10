"""
Activation Functions

Different activation functions for neural networks, showing the evolution
from simple step functions to differentiable non-linear functions.
"""

import numpy as np


def step_function(x: np.ndarray) -> np.ndarray:
    """
    Step function (Heaviside function) used in original perceptron.
    
    This was Rosenblatt's original activation function - simple but
    not differentiable, which prevented gradient-based learning.
    
    Args:
        x: Input values
        
    Returns:
        Binary output (0 or 1)
    """
    return (x >= 0).astype(int)


def sigmoid(x: np.ndarray) -> np.ndarray:
    """
    Sigmoid activation function.
    
    Key properties:
    - Smooth and differentiable (enables backpropagation)
    - Output range: (0, 1)
    - Non-linear (enables learning complex patterns)
    
    Args:
        x: Input values
        
    Returns:
        Sigmoid activation in range (0, 1)
    """
    # Clip to prevent overflow
    x = np.clip(x, -500, 500)
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x: np.ndarray) -> np.ndarray:
    """
    Derivative of sigmoid function.
    
    Critical for backpropagation - this is what was missing
    for 25 years (1962-1986) in training multi-layer networks.
    
    Args:
        x: Input values (sigmoid outputs)
        
    Returns:
        Derivative values
    """
    return x * (1 - x)


def tanh(x: np.ndarray) -> np.ndarray:
    """
    Hyperbolic tangent activation function.
    
    Properties:
    - Output range: (-1, 1)
    - Zero-centered (often trains better than sigmoid)
    - Differentiable
    
    Args:
        x: Input values
        
    Returns:
        Tanh activation in range (-1, 1)
    """
    return np.tanh(x)


def tanh_derivative(x: np.ndarray) -> np.ndarray:
    """
    Derivative of tanh function.
    
    Args:
        x: Input values (tanh outputs)
        
    Returns:
        Derivative values
    """
    return 1 - x**2


def relu(x: np.ndarray) -> np.ndarray:
    """
    Rectified Linear Unit (ReLU) - modern activation function.
    
    Properties:
    - Simple and efficient
    - Helps with vanishing gradient problem
    - Not used in original perceptron era
    
    Args:
        x: Input values
        
    Returns:
        ReLU activation (max(0, x))
    """
    return np.maximum(0, x)


def relu_derivative(x: np.ndarray) -> np.ndarray:
    """
    Derivative of ReLU function.
    
    Args:
        x: Input values
        
    Returns:
        Derivative (1 if x > 0, else 0)
    """
    return (x > 0).astype(float)


def demonstrate_activation_evolution():
    """
    Show the evolution of activation functions in neural networks.
    """
    import matplotlib.pyplot as plt
    
    x = np.linspace(-5, 5, 100)
    
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    fig.suptitle("Evolution of Activation Functions in Neural Networks", fontsize=16)
    
    # Step function (1958)
    axes[0, 0].plot(x, step_function(x), 'b-', linewidth=2)
    axes[0, 0].set_title("Step Function (1958)\nOriginal Perceptron")
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].set_ylim(-0.1, 1.1)
    
    # Sigmoid (1970s)
    axes[0, 1].plot(x, sigmoid(x), 'g-', linewidth=2)
    axes[0, 1].set_title("Sigmoid (1970s)\nEnabled Backpropagation")
    axes[0, 1].grid(True, alpha=0.3)
    
    # Tanh (1980s)
    axes[0, 2].plot(x, tanh(x), 'r-', linewidth=2)
    axes[0, 2].set_title("Tanh (1980s)\nZero-Centered")
    axes[0, 2].grid(True, alpha=0.3)
    
    # Derivatives
    axes[1, 0].set_title("No Derivative\n(Can't use gradients)")
    axes[1, 0].text(0.5, 0.5, "Undefined at x=0", ha='center', va='center', fontsize=12)
    axes[1, 0].set_xlim(-5, 5)
    axes[1, 0].grid(True, alpha=0.3)
    
    axes[1, 1].plot(x, sigmoid_derivative(sigmoid(x)), 'g--', linewidth=2)
    axes[1, 1].set_title("Sigmoid Derivative\n(Enables learning)")
    axes[1, 1].grid(True, alpha=0.3)
    
    axes[1, 2].plot(x, tanh_derivative(tanh(x)), 'r--', linewidth=2)
    axes[1, 2].set_title("Tanh Derivative\n(Better gradients)")
    axes[1, 2].grid(True, alpha=0.3)
    
    for ax in axes.flat:
        ax.set_xlabel("Input")
        ax.set_ylabel("Output")
    
    plt.tight_layout()
    plt.show()
    
    print("=" * 60)
    print("ACTIVATION FUNCTION EVOLUTION")
    print("=" * 60)
    print("\n1958 - Step Function:")
    print("  ✗ Not differentiable - can't compute gradients")
    print("  ✗ Binary output only - limited expressiveness")
    print("  ✓ Simple to understand and implement")
    
    print("\n1970s - Sigmoid Function:")
    print("  ✓ Differentiable - enables backpropagation!")
    print("  ✓ Smooth gradients - stable learning")
    print("  ✗ Vanishing gradients in deep networks")
    
    print("\n1980s - Hyperbolic Tangent:")
    print("  ✓ Zero-centered - often trains faster")
    print("  ✓ Stronger gradients than sigmoid")
    print("  ✗ Still has vanishing gradient problem")
    
    print("\n" + "=" * 60)
    print("KEY INSIGHT: The shift from step to sigmoid functions")
    print("was CRUCIAL for enabling multi-layer network training!")
    print("=" * 60)


if __name__ == "__main__":
    # Demonstrate the evolution
    demonstrate_activation_evolution()
