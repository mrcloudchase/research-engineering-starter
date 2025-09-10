"""
Multi-Layer Perceptron Implementation

This demonstrates the solution to the XOR problem using hidden layers.
Includes both random weight updates (fails) and backpropagation (succeeds)
to illustrate why effective training took 25 years to develop.
"""

import numpy as np
from typing import Optional, Tuple, List
from .activation import sigmoid, sigmoid_derivative


class MultiLayerPerceptron:
    """
    Two-layer neural network that can solve XOR.
    
    This implementation shows:
    1. How hidden layers enable non-linear decision boundaries
    2. Why random weight updates fail (pre-1986)
    3. How backpropagation enables successful training (1986)
    """
    
    def __init__(self, 
                 input_size: int,
                 hidden_size: int,
                 output_size: int,
                 learning_rate: float = 0.5,
                 random_state: Optional[int] = None):
        """
        Initialize MLP with random weights.
        
        Args:
            input_size: Number of input features
            hidden_size: Number of hidden neurons
            output_size: Number of output neurons
            learning_rate: Learning rate for weight updates
            random_state: Random seed for reproducibility
        """
        if random_state is not None:
            np.random.seed(random_state)
        
        # Initialize weights and biases
        # Input -> Hidden layer
        self.W1 = np.random.randn(input_size, hidden_size) * 0.5
        self.b1 = np.zeros((1, hidden_size))
        
        # Hidden -> Output layer
        self.W2 = np.random.randn(hidden_size, output_size) * 0.5
        self.b2 = np.zeros((1, output_size))
        
        self.learning_rate = learning_rate
        
        # Track training history
        self.loss_history = []
        
    def forward(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Forward pass through the network.
        
        Args:
            X: Input data of shape (n_samples, input_size)
            
        Returns:
            Tuple of (hidden_output, final_output, input)
        """
        # Input -> Hidden
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = sigmoid(self.z1)
        
        # Hidden -> Output
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = sigmoid(self.z2)
        
        return self.a1, self.a2, X
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions (binary classification).
        
        Args:
            X: Input data
            
        Returns:
            Binary predictions (0 or 1)
        """
        _, output, _ = self.forward(X)
        return (output > 0.5).astype(int).flatten()
    
    def compute_loss(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Compute binary cross-entropy loss.
        
        Args:
            y_true: True labels
            y_pred: Predicted probabilities
            
        Returns:
            Mean loss value
        """
        # Clip to prevent log(0)
        y_pred = np.clip(y_pred, 1e-7, 1 - 1e-7)
        
        loss = -np.mean(
            y_true * np.log(y_pred) + 
            (1 - y_true) * np.log(1 - y_pred)
        )
        return loss
    
    def backpropagation(self, X: np.ndarray, y: np.ndarray):
        """
        Backpropagation algorithm (Rumelhart, Hinton & Williams, 1986).
        
        This is the key innovation that made multi-layer networks trainable!
        
        Args:
            X: Input data
            y: True labels
        """
        m = X.shape[0]
        
        # Forward pass
        hidden, output, inputs = self.forward(X)
        
        # Reshape y for calculations
        y = y.reshape(-1, 1)
        
        # Calculate gradients (this is the magic!)
        # Output layer gradients
        dz2 = output - y  # Error at output
        dW2 = (1/m) * np.dot(hidden.T, dz2)
        db2 = (1/m) * np.sum(dz2, axis=0, keepdims=True)
        
        # Hidden layer gradients (backpropagate the error)
        da1 = np.dot(dz2, self.W2.T)
        dz1 = da1 * sigmoid_derivative(hidden)
        dW1 = (1/m) * np.dot(inputs.T, dz1)
        db1 = (1/m) * np.sum(dz1, axis=0, keepdims=True)
        
        # Update weights and biases
        self.W2 -= self.learning_rate * dW2
        self.b2 -= self.learning_rate * db2
        self.W1 -= self.learning_rate * dW1
        self.b1 -= self.learning_rate * db1
    
    def random_weight_update(self, X: np.ndarray, y: np.ndarray):
        """
        Random weight updates (pre-backpropagation era).
        
        This simulates attempts to train MLPs before backpropagation.
        Spoiler: It doesn't work well!
        
        Args:
            X: Input data
            y: True labels
        """
        # Forward pass to get current loss
        _, output, _ = self.forward(X)
        current_loss = self.compute_loss(y.reshape(-1, 1), output)
        
        # Try random weight changes
        weight_change = 0.01
        
        # Randomly perturb weights
        self.W1 += np.random.randn(*self.W1.shape) * weight_change
        self.W2 += np.random.randn(*self.W2.shape) * weight_change
        self.b1 += np.random.randn(*self.b1.shape) * weight_change
        self.b2 += np.random.randn(*self.b2.shape) * weight_change
        
        # Check if it improved
        _, new_output, _ = self.forward(X)
        new_loss = self.compute_loss(y.reshape(-1, 1), new_output)
        
        # Keep changes only if they improve loss (hill climbing)
        if new_loss > current_loss:
            # Revert changes
            self.W1 -= np.random.randn(*self.W1.shape) * weight_change
            self.W2 -= np.random.randn(*self.W2.shape) * weight_change
            self.b1 -= np.random.randn(*self.b1.shape) * weight_change
            self.b2 -= np.random.randn(*self.b2.shape) * weight_change
    
    def train(self, X: np.ndarray, y: np.ndarray, 
              epochs: int = 1000, 
              method: str = 'backprop') -> 'MultiLayerPerceptron':
        """
        Train the MLP using specified method.
        
        Args:
            X: Training data
            y: Training labels
            epochs: Number of training iterations
            method: 'backprop' or 'random' (to show why backprop was crucial)
            
        Returns:
            Self for method chaining
        """
        self.loss_history = []
        
        for epoch in range(epochs):
            # Choose training method
            if method == 'backprop':
                self.backpropagation(X, y)
            elif method == 'random':
                self.random_weight_update(X, y)
            else:
                raise ValueError(f"Unknown method: {method}")
            
            # Track loss
            _, output, _ = self.forward(X)
            loss = self.compute_loss(y.reshape(-1, 1), output)
            self.loss_history.append(loss)
            
            # Print progress
            if epoch % 100 == 0:
                accuracy = self.score(X, y)
                print(f"Epoch {epoch}: Loss = {loss:.4f}, Accuracy = {accuracy:.2%}")
        
        return self
    
    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Calculate accuracy on given data.
        
        Args:
            X: Input data
            y: True labels
            
        Returns:
            Accuracy score (0 to 1)
        """
        predictions = self.predict(X)
        accuracy = np.mean(predictions == y)
        return accuracy


def demonstrate_mlp_solves_xor():
    """
    Demonstrate that multi-layer perceptron solves XOR.
    
    This shows how hidden layers enable learning non-linear patterns.
    """
    from .data_utils import generate_logic_gate_data
    
    # Generate XOR data
    X, y = generate_logic_gate_data('XOR')
    
    print("=" * 60)
    print("MULTI-LAYER PERCEPTRON XOR SOLUTION")
    print("=" * 60)
    
    # Test with backpropagation (1986)
    print("\n1. WITH BACKPROPAGATION (Rumelhart et al., 1986):")
    print("-" * 40)
    mlp_backprop = MultiLayerPerceptron(
        input_size=2,
        hidden_size=2,  # Minimal architecture
        output_size=1,
        learning_rate=1.0,
        random_state=42
    )
    mlp_backprop.train(X, y, epochs=1000, method='backprop')
    
    print(f"\nFinal Accuracy: {mlp_backprop.score(X, y):.2%}")
    print(f"Predictions: {mlp_backprop.predict(X)}")
    print(f"Expected:     {y}")
    
    # Test with random updates (pre-1986)
    print("\n2. WITH RANDOM WEIGHT UPDATES (Pre-1986 attempts):")
    print("-" * 40)
    mlp_random = MultiLayerPerceptron(
        input_size=2,
        hidden_size=2,
        output_size=1,
        learning_rate=1.0,
        random_state=42
    )
    mlp_random.train(X, y, epochs=1000, method='random')
    
    print(f"\nFinal Accuracy: {mlp_random.score(X, y):.2%}")
    print(f"Predictions: {mlp_random.predict(X)}")
    print(f"Expected:     {y}")
    
    print("\n" + "=" * 60)
    print("CONCLUSION:")
    print("- Backpropagation SUCCEEDS at training MLPs for XOR")
    print("- Random updates FAIL to find good weights")
    print("- This explains the 25-year gap (1962-1986) in MLP training!")
    print("=" * 60)
    
    return mlp_backprop, mlp_random


def analyze_hidden_layer_importance():
    """
    Show why hidden layers are necessary for XOR.
    """
    from .data_utils import generate_logic_gate_data
    import matplotlib.pyplot as plt
    
    X, y = generate_logic_gate_data('XOR')
    
    # Train an MLP
    mlp = MultiLayerPerceptron(2, 2, 1, learning_rate=1.0, random_state=42)
    mlp.train(X, y, epochs=1000, method='backprop')
    
    # Get hidden layer representations
    hidden, output, _ = mlp.forward(X)
    
    # Visualize
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Original XOR problem
    axes[0].scatter(X[y==0, 0], X[y==0, 1], c='red', s=100, label='XOR=0')
    axes[0].scatter(X[y==1, 0], X[y==1, 1], c='blue', s=100, label='XOR=1')
    axes[0].set_title("Original XOR Problem\n(Not linearly separable)")
    axes[0].set_xlabel("Input 1")
    axes[0].set_ylabel("Input 2")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Hidden layer representation
    axes[1].scatter(hidden[y==0, 0], hidden[y==0, 1], c='red', s=100, label='XOR=0')
    axes[1].scatter(hidden[y==1, 0], hidden[y==1, 1], c='blue', s=100, label='XOR=1')
    axes[1].set_title("Hidden Layer Representation\n(Transformed to be separable)")
    axes[1].set_xlabel("Hidden Unit 1")
    axes[1].set_ylabel("Hidden Unit 2")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    # Loss curve
    axes[2].plot(mlp.loss_history)
    axes[2].set_title("Training Loss\n(Successful convergence)")
    axes[2].set_xlabel("Epoch")
    axes[2].set_ylabel("Loss")
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print("=" * 60)
    print("KEY INSIGHT: Hidden layers transform the input space")
    print("so that non-linearly separable problems become separable!")
    print("=" * 60)


if __name__ == "__main__":
    # Run demonstrations
    demonstrate_mlp_solves_xor()
    print("\n")
    analyze_hidden_layer_importance()
