"""
Single-Layer Perceptron Implementation

This is the original perceptron as described by Frank Rosenblatt in 1958.
It can only learn linearly separable functions.
"""

import numpy as np
from typing import Tuple, Optional


class SingleLayerPerceptron:
    """
    Single-layer perceptron implementation following Rosenblatt's 1958 design.
    
    This implements the perceptron learning algorithm with a step activation function.
    As proven by Minsky & Papert (1969), this can only learn linearly separable functions.
    """
    
    def __init__(self, input_size: int = 2, learning_rate: float = 0.1, random_seed: Optional[int] = None):
        """
        Initialize the single-layer perceptron.
        
        Args:
            input_size: Number of input features
            learning_rate: Learning rate for weight updates (η in the paper)
            random_seed: Random seed for reproducibility
        """
        self.input_size = input_size
        self.learning_rate = learning_rate
        
        if random_seed is not None:
            np.random.seed(random_seed)
        
        # Initialize weights and bias with small random values
        # Following Rosenblatt's initialization strategy
        self.weights = np.random.randn(input_size) * 0.1
        self.bias = np.random.randn() * 0.1
        
        # Track training history
        self.history = {
            'loss': [],
            'accuracy': [],
            'weights': [],
            'bias': []
        }
    
    def step_activation(self, x: np.ndarray) -> np.ndarray:
        """
        Step activation function (Heaviside function).
        
        This is the original activation used by Rosenblatt.
        Output is 1 if input > 0, else 0.
        
        Args:
            x: Input to activate
            
        Returns:
            Binary output (0 or 1)
        """
        return (x > 0).astype(int)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions for input data.
        
        Implements the perceptron decision rule:
        y = step(w·x + b)
        
        Args:
            X: Input data of shape (n_samples, n_features)
            
        Returns:
            Binary predictions of shape (n_samples,)
        """
        # Compute weighted sum: w·x + b
        linear_output = np.dot(X, self.weights) + self.bias
        
        # Apply step activation
        predictions = self.step_activation(linear_output)
        
        return predictions
    
    def train_step(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Perform one training step on a batch of data.
        
        Implements the perceptron learning rule:
        w_new = w_old + η(target - output)x
        b_new = b_old + η(target - output)
        
        Args:
            X: Input data of shape (n_samples, n_features)
            y: Target labels of shape (n_samples,)
            
        Returns:
            Mean loss for this batch
        """
        predictions = self.predict(X)
        errors = y - predictions
        
        # Update weights and bias for each sample
        for i in range(len(X)):
            self.weights += self.learning_rate * errors[i] * X[i]
            self.bias += self.learning_rate * errors[i]
        
        # Calculate loss (mean squared error)
        loss = np.mean(errors ** 2)
        
        return loss
    
    def fit(self, X: np.ndarray, y: np.ndarray, epochs: int = 100, verbose: bool = False) -> 'SingleLayerPerceptron':
        """
        Train the perceptron on the given data.
        
        Args:
            X: Training data of shape (n_samples, n_features)
            y: Target labels of shape (n_samples,)
            epochs: Number of training epochs
            verbose: Whether to print training progress
            
        Returns:
            Self for method chaining
        """
        for epoch in range(epochs):
            # Perform training step
            loss = self.train_step(X, y)
            
            # Calculate accuracy
            predictions = self.predict(X)
            accuracy = np.mean(predictions == y)
            
            # Store history
            self.history['loss'].append(loss)
            self.history['accuracy'].append(accuracy)
            self.history['weights'].append(self.weights.copy())
            self.history['bias'].append(self.bias.copy())
            
            if verbose and (epoch % 10 == 0 or epoch == epochs - 1):
                print(f"Epoch {epoch:3d}: Loss = {loss:.4f}, Accuracy = {accuracy:.2%}")
            
            # Early stopping if perfect accuracy achieved
            if accuracy == 1.0:
                if verbose:
                    print(f"Perfect accuracy achieved at epoch {epoch}")
                break
        
        return self
    
    def get_decision_boundary(self) -> Tuple[np.ndarray, float]:
        """
        Get the decision boundary parameters.
        
        For a 2D input space, the decision boundary is defined by:
        w1*x1 + w2*x2 + b = 0
        
        Returns:
            Tuple of (weights, bias) defining the boundary
        """
        return self.weights, self.bias
    
    def reset(self) -> None:
        """Reset the perceptron to initial random state."""
        self.weights = np.random.randn(self.input_size) * 0.1
        self.bias = np.random.randn() * 0.1
        self.history = {
            'loss': [],
            'accuracy': [],
            'weights': [],
            'bias': []
        }
