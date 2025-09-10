"""
Single-Layer Perceptron Implementation

Recreating Frank Rosenblatt's 1958 perceptron with the original learning algorithm.
This implementation will successfully learn linearly separable functions (AND, OR)
but fail on non-linearly separable functions (XOR).
"""

import numpy as np
from typing import Tuple, Optional
from .activation import step_function


class Perceptron:
    """
    Single-layer perceptron with Rosenblatt's learning rule.
    
    This is a faithful recreation of the 1958 perceptron algorithm,
    demonstrating both its capabilities and fundamental limitations.
    """
    
    def __init__(self, n_features: int, learning_rate: float = 0.1, random_state: Optional[int] = None):
        """
        Initialize perceptron with random weights.
        
        Args:
            n_features: Number of input features
            learning_rate: Learning rate (eta) for weight updates
            random_state: Random seed for reproducibility
        """
        self.n_features = n_features
        self.learning_rate = learning_rate
        
        # Initialize weights and bias
        if random_state is not None:
            np.random.seed(random_state)
        
        self.weights = np.random.randn(n_features) * 0.01
        self.bias = 0.0
        
        # Track training history
        self.errors_history = []
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions using current weights.
        
        Args:
            X: Input data of shape (n_samples, n_features)
            
        Returns:
            Binary predictions (0 or 1)
        """
        # Calculate weighted sum
        linear_output = np.dot(X, self.weights) + self.bias
        
        # Apply step function (threshold at 0)
        predictions = step_function(linear_output)
        
        return predictions
    
    def train_step(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Perform one training step on the entire dataset.
        
        Implements Rosenblatt's perceptron learning rule:
        w_new = w_old + learning_rate * error * input
        
        Args:
            X: Training data of shape (n_samples, n_features)
            y: Target labels of shape (n_samples,)
            
        Returns:
            Mean absolute error for this step
        """
        total_error = 0
        
        for xi, yi in zip(X, y):
            # Make prediction
            prediction = self.predict(xi.reshape(1, -1))[0]
            
            # Calculate error
            error = yi - prediction
            total_error += abs(error)
            
            # Update weights only if there's an error
            if error != 0:
                # Perceptron learning rule
                self.weights += self.learning_rate * error * xi
                self.bias += self.learning_rate * error
        
        mean_error = total_error / len(X)
        self.errors_history.append(mean_error)
        
        return mean_error
    
    def fit(self, X: np.ndarray, y: np.ndarray, epochs: int = 100) -> 'Perceptron':
        """
        Train the perceptron using the perceptron learning rule.
        
        Args:
            X: Training data of shape (n_samples, n_features)
            y: Target labels of shape (n_samples,)
            epochs: Number of training iterations
            
        Returns:
            Self for method chaining
        """
        self.errors_history = []
        
        for epoch in range(epochs):
            error = self.train_step(X, y)
            
            # Convergence check
            if error == 0:
                print(f"Converged at epoch {epoch + 1}")
                break
                
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
    
    def get_decision_boundary(self) -> Tuple[float, float, float]:
        """
        Get decision boundary parameters for 2D visualization.
        
        For 2D inputs, the decision boundary is defined by:
        w1*x1 + w2*x2 + b = 0
        
        Returns:
            Tuple of (w1, w2, bias) defining the decision boundary
        """
        if self.n_features != 2:
            raise ValueError("Decision boundary only available for 2D inputs")
            
        return self.weights[0], self.weights[1], self.bias


def demonstrate_perceptron_limitation():
    """
    Demonstrate that single-layer perceptron solves AND/OR but fails on XOR.
    
    This recreates the fundamental discovery that led to the first AI winter.
    """
    # Generate logic gate data
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y_and = np.array([0, 0, 0, 1])  # AND gate
    y_or = np.array([0, 1, 1, 1])   # OR gate  
    y_xor = np.array([0, 1, 1, 0])  # XOR gate
    
    print("=" * 50)
    print("PERCEPTRON CAPABILITY DEMONSTRATION")
    print("=" * 50)
    
    # Test on AND gate (linearly separable)
    print("\n1. AND Gate (Linearly Separable):")
    perceptron_and = Perceptron(n_features=2, learning_rate=0.1, random_state=42)
    perceptron_and.fit(X, y_and, epochs=100)
    accuracy_and = perceptron_and.score(X, y_and)
    print(f"   Accuracy: {accuracy_and:.2%}")
    print(f"   Predictions: {perceptron_and.predict(X)}")
    print(f"   Expected:     {y_and}")
    
    # Test on OR gate (linearly separable)
    print("\n2. OR Gate (Linearly Separable):")
    perceptron_or = Perceptron(n_features=2, learning_rate=0.1, random_state=42)
    perceptron_or.fit(X, y_or, epochs=100)
    accuracy_or = perceptron_or.score(X, y_or)
    print(f"   Accuracy: {accuracy_or:.2%}")
    print(f"   Predictions: {perceptron_or.predict(X)}")
    print(f"   Expected:     {y_or}")
    
    # Test on XOR gate (NOT linearly separable)
    print("\n3. XOR Gate (NOT Linearly Separable):")
    perceptron_xor = Perceptron(n_features=2, learning_rate=0.1, random_state=42)
    perceptron_xor.fit(X, y_xor, epochs=1000)  # Even with more epochs
    accuracy_xor = perceptron_xor.score(X, y_xor)
    print(f"   Accuracy: {accuracy_xor:.2%}")
    print(f"   Predictions: {perceptron_xor.predict(X)}")
    print(f"   Expected:     {y_xor}")
    
    print("\n" + "=" * 50)
    print("CONCLUSION: Single-layer perceptron CANNOT solve XOR!")
    print("This fundamental limitation led to the 1969 Minsky-Papert")
    print("critique and the first AI winter.")
    print("=" * 50)
    
    return {
        'AND': accuracy_and,
        'OR': accuracy_or, 
        'XOR': accuracy_xor
    }


if __name__ == "__main__":
    # Run demonstration
    results = demonstrate_perceptron_limitation()
