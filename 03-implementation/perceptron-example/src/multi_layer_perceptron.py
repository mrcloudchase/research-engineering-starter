"""
Multi-Layer Perceptron Implementation

This implements a multi-layer neural network with backpropagation,
solving the limitations of the single-layer perceptron.
"""

import numpy as np
from typing import List, Tuple, Optional, Callable


class MultiLayerPerceptron:
    """
    Multi-layer perceptron with configurable architecture and backpropagation training.
    
    This implementation demonstrates how adding hidden layers with non-linear activation
    functions enables learning of non-linearly separable functions like XOR.
    """
    
    def __init__(self, 
                 layer_sizes: List[int],
                 activation: str = 'sigmoid',
                 learning_rate: float = 0.5,
                 random_seed: Optional[int] = None):
        """
        Initialize the multi-layer perceptron.
        
        Args:
            layer_sizes: List of layer sizes [input_size, hidden1, hidden2, ..., output_size]
            activation: Activation function ('sigmoid', 'tanh', 'relu')
            learning_rate: Learning rate for backpropagation
            random_seed: Random seed for reproducibility
        """
        self.layer_sizes = layer_sizes
        self.n_layers = len(layer_sizes)
        self.learning_rate = learning_rate
        self.activation_name = activation
        
        if random_seed is not None:
            np.random.seed(random_seed)
        
        # Initialize weights and biases for each layer
        self.weights = []
        self.biases = []
        
        for i in range(self.n_layers - 1):
            # Xavier/Glorot initialization for better convergence
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * np.sqrt(2.0 / layer_sizes[i])
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)
        
        # Set activation functions
        self._set_activation_functions(activation)
        
        # Track training history
        self.history = {
            'loss': [],
            'accuracy': []
        }
    
    def _set_activation_functions(self, activation: str) -> None:
        """Set the activation function and its derivative."""
        if activation == 'sigmoid':
            self.activation = self._sigmoid
            self.activation_derivative = self._sigmoid_derivative
        elif activation == 'tanh':
            self.activation = self._tanh
            self.activation_derivative = self._tanh_derivative
        elif activation == 'relu':
            self.activation = self._relu
            self.activation_derivative = self._relu_derivative
        else:
            raise ValueError(f"Unknown activation: {activation}")
    
    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        """Sigmoid activation function."""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))  # Clip to prevent overflow
    
    def _sigmoid_derivative(self, x: np.ndarray) -> np.ndarray:
        """Derivative of sigmoid function."""
        s = self._sigmoid(x)
        return s * (1 - s)
    
    def _tanh(self, x: np.ndarray) -> np.ndarray:
        """Hyperbolic tangent activation function."""
        return np.tanh(x)
    
    def _tanh_derivative(self, x: np.ndarray) -> np.ndarray:
        """Derivative of tanh function."""
        return 1 - np.tanh(x) ** 2
    
    def _relu(self, x: np.ndarray) -> np.ndarray:
        """ReLU activation function."""
        return np.maximum(0, x)
    
    def _relu_derivative(self, x: np.ndarray) -> np.ndarray:
        """Derivative of ReLU function."""
        return (x > 0).astype(float)
    
    def forward_propagation(self, X: np.ndarray) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """
        Perform forward propagation through the network.
        
        Args:
            X: Input data of shape (n_samples, n_features)
            
        Returns:
            Tuple of (activations, weighted_inputs) for each layer
        """
        activations = [X]
        weighted_inputs = []
        
        for i in range(self.n_layers - 1):
            z = np.dot(activations[-1], self.weights[i]) + self.biases[i]
            weighted_inputs.append(z)
            
            # Apply activation function (except for output layer)
            if i < self.n_layers - 2:
                a = self.activation(z)
            else:
                # Output layer uses sigmoid for binary classification
                a = self._sigmoid(z)
            
            activations.append(a)
        
        return activations, weighted_inputs
    
    def backward_propagation(self, X: np.ndarray, y: np.ndarray,
                           activations: List[np.ndarray], 
                           weighted_inputs: List[np.ndarray]) -> None:
        """
        Perform backward propagation to update weights.
        
        Implements the backpropagation algorithm discovered by Rumelhart, Hinton & Williams (1986).
        
        Args:
            X: Input data
            y: Target labels
            activations: Activations from forward pass
            weighted_inputs: Weighted inputs from forward pass
        """
        m = X.shape[0]
        y_reshaped = y.reshape(-1, 1)
        
        # Calculate output layer error
        deltas = [activations[-1] - y_reshaped]
        
        # Backpropagate errors through hidden layers
        for i in range(self.n_layers - 2, 0, -1):
            if i < self.n_layers - 1:
                # Hidden layer error
                error = np.dot(deltas[0], self.weights[i].T)
                delta = error * self.activation_derivative(weighted_inputs[i-1])
            deltas.insert(0, delta)
        
        # Update weights and biases
        for i in range(self.n_layers - 1):
            self.weights[i] -= self.learning_rate * np.dot(activations[i].T, deltas[i]) / m
            self.biases[i] -= self.learning_rate * np.mean(deltas[i], axis=0, keepdims=True)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict probability for input data.
        
        Args:
            X: Input data of shape (n_samples, n_features)
            
        Returns:
            Predicted probabilities of shape (n_samples,)
        """
        activations, _ = self.forward_propagation(X)
        return activations[-1].flatten()
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make binary predictions for input data.
        
        Args:
            X: Input data of shape (n_samples, n_features)
            
        Returns:
            Binary predictions of shape (n_samples,)
        """
        probabilities = self.predict_proba(X)
        return (probabilities > 0.5).astype(int)
    
    def compute_loss(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Compute binary cross-entropy loss.
        
        Args:
            X: Input data
            y: Target labels
            
        Returns:
            Mean loss value
        """
        predictions = self.predict_proba(X)
        epsilon = 1e-7  # Small value to prevent log(0)
        loss = -np.mean(y * np.log(predictions + epsilon) + 
                        (1 - y) * np.log(1 - predictions + epsilon))
        return loss
    
    def fit(self, X: np.ndarray, y: np.ndarray, 
            epochs: int = 1000, verbose: bool = False) -> 'MultiLayerPerceptron':
        """
        Train the multi-layer perceptron using backpropagation.
        
        Args:
            X: Training data of shape (n_samples, n_features)
            y: Target labels of shape (n_samples,)
            epochs: Number of training epochs
            verbose: Whether to print training progress
            
        Returns:
            Self for method chaining
        """
        for epoch in range(epochs):
            # Forward propagation
            activations, weighted_inputs = self.forward_propagation(X)
            
            # Backward propagation
            self.backward_propagation(X, y, activations, weighted_inputs)
            
            # Calculate metrics
            loss = self.compute_loss(X, y)
            predictions = self.predict(X)
            accuracy = np.mean(predictions == y)
            
            # Store history
            self.history['loss'].append(loss)
            self.history['accuracy'].append(accuracy)
            
            if verbose and (epoch % 100 == 0 or epoch == epochs - 1):
                print(f"Epoch {epoch:4d}: Loss = {loss:.4f}, Accuracy = {accuracy:.2%}")
            
            # Early stopping if perfect accuracy
            if accuracy == 1.0 and loss < 0.01:
                if verbose:
                    print(f"Converged at epoch {epoch}")
                break
        
        return self
    
    def reset(self) -> None:
        """Reset the network to initial random state."""
        self.weights = []
        self.biases = []
        
        for i in range(self.n_layers - 1):
            w = np.random.randn(self.layer_sizes[i], self.layer_sizes[i+1]) * np.sqrt(2.0 / self.layer_sizes[i])
            b = np.zeros((1, self.layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)
        
        self.history = {
            'loss': [],
            'accuracy': []
        }
