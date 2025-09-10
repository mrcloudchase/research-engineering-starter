"""
Unit tests for perceptron implementations.

Tests both single-layer and multi-layer perceptrons to ensure correctness.
"""

import pytest
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.single_layer_perceptron import SingleLayerPerceptron
from src.multi_layer_perceptron import MultiLayerPerceptron
from src.data_utils import generate_logic_gate_data


class TestSingleLayerPerceptron:
    """Tests for single-layer perceptron."""
    
    def test_initialization(self):
        """Test perceptron initialization."""
        slp = SingleLayerPerceptron(input_size=2, learning_rate=0.1, random_seed=42)
        assert slp.input_size == 2
        assert slp.learning_rate == 0.1
        assert slp.weights.shape == (2,)
        assert isinstance(slp.bias, (float, np.floating))
    
    def test_step_activation(self):
        """Test step activation function."""
        slp = SingleLayerPerceptron()
        assert slp.step_activation(np.array([0.5])) == 1
        assert slp.step_activation(np.array([-0.5])) == 0
        assert slp.step_activation(np.array([0])) == 0
    
    def test_predict_shape(self):
        """Test prediction output shape."""
        slp = SingleLayerPerceptron(input_size=2)
        X = np.array([[0, 0], [1, 1]])
        predictions = slp.predict(X)
        assert predictions.shape == (2,)
        assert all(p in [0, 1] for p in predictions)
    
    def test_and_gate_learning(self):
        """Test that single-layer perceptron can learn AND gate."""
        X, y = generate_logic_gate_data('AND')
        slp = SingleLayerPerceptron(random_seed=42)
        slp.fit(X, y, epochs=100)
        
        predictions = slp.predict(X)
        accuracy = np.mean(predictions == y)
        assert accuracy == 1.0, "Single-layer perceptron should learn AND gate perfectly"
    
    def test_or_gate_learning(self):
        """Test that single-layer perceptron can learn OR gate."""
        X, y = generate_logic_gate_data('OR')
        slp = SingleLayerPerceptron(random_seed=42)
        slp.fit(X, y, epochs=100)
        
        predictions = slp.predict(X)
        accuracy = np.mean(predictions == y)
        assert accuracy == 1.0, "Single-layer perceptron should learn OR gate perfectly"
    
    def test_xor_gate_failure(self):
        """Test that single-layer perceptron CANNOT learn XOR gate."""
        X, y = generate_logic_gate_data('XOR')
        slp = SingleLayerPerceptron(random_seed=42)
        slp.fit(X, y, epochs=500)
        
        predictions = slp.predict(X)
        accuracy = np.mean(predictions == y)
        assert accuracy < 1.0, "Single-layer perceptron should NOT learn XOR gate perfectly"
        assert accuracy <= 0.75, "Single-layer perceptron accuracy on XOR should be ≤ 75%"
    
    def test_history_tracking(self):
        """Test that training history is properly tracked."""
        X, y = generate_logic_gate_data('AND')
        slp = SingleLayerPerceptron()
        slp.fit(X, y, epochs=10)
        
        assert len(slp.history['loss']) == 10
        assert len(slp.history['accuracy']) == 10
        assert len(slp.history['weights']) == 10
        assert len(slp.history['bias']) == 10


class TestMultiLayerPerceptron:
    """Tests for multi-layer perceptron."""
    
    def test_initialization(self):
        """Test MLP initialization."""
        mlp = MultiLayerPerceptron(layer_sizes=[2, 4, 1], learning_rate=0.5, random_seed=42)
        assert mlp.layer_sizes == [2, 4, 1]
        assert mlp.n_layers == 3
        assert len(mlp.weights) == 2
        assert len(mlp.biases) == 2
        assert mlp.weights[0].shape == (2, 4)
        assert mlp.weights[1].shape == (4, 1)
    
    def test_activation_functions(self):
        """Test different activation functions."""
        x = np.array([0.5, -0.5, 0])
        
        # Test sigmoid
        mlp_sigmoid = MultiLayerPerceptron([2, 2, 1], activation='sigmoid')
        sigmoid_output = mlp_sigmoid._sigmoid(x)
        assert all(0 < s < 1 for s in sigmoid_output)
        
        # Test tanh
        mlp_tanh = MultiLayerPerceptron([2, 2, 1], activation='tanh')
        tanh_output = mlp_tanh._tanh(x)
        assert all(-1 < t < 1 for t in tanh_output)
        
        # Test ReLU
        mlp_relu = MultiLayerPerceptron([2, 2, 1], activation='relu')
        relu_output = mlp_relu._relu(x)
        assert relu_output[0] == 0.5
        assert relu_output[1] == 0
        assert relu_output[2] == 0
    
    def test_forward_propagation(self):
        """Test forward propagation."""
        mlp = MultiLayerPerceptron([2, 3, 1], random_seed=42)
        X = np.array([[0, 0], [1, 1]])
        activations, weighted_inputs = mlp.forward_propagation(X)
        
        assert len(activations) == 3  # Input + hidden + output
        assert len(weighted_inputs) == 2  # Hidden + output
        assert activations[0].shape == (2, 2)  # Input
        assert activations[1].shape == (2, 3)  # Hidden
        assert activations[2].shape == (2, 1)  # Output
    
    def test_xor_gate_learning(self):
        """Test that multi-layer perceptron CAN learn XOR gate."""
        X, y = generate_logic_gate_data('XOR')
        
        # Try multiple architectures to ensure at least one works
        architectures = [
            [2, 2, 1],
            [2, 3, 1],
            [2, 4, 1]
        ]
        
        success = False
        for arch in architectures:
            mlp = MultiLayerPerceptron(arch, activation='sigmoid', 
                                      learning_rate=0.5, random_seed=42)
            mlp.fit(X, y, epochs=2000, verbose=False)
            
            predictions = mlp.predict(X)
            accuracy = np.mean(predictions == y)
            
            if accuracy == 1.0:
                success = True
                break
        
        assert success, "Multi-layer perceptron should learn XOR gate with appropriate architecture"
    
    def test_all_gates_learning(self):
        """Test that MLP can learn all basic logic gates."""
        gates = ['AND', 'OR', 'XOR', 'NAND', 'NOR']
        mlp = MultiLayerPerceptron([2, 4, 1], activation='sigmoid', 
                                  learning_rate=0.5)
        
        for gate in gates:
            X, y = generate_logic_gate_data(gate)
            mlp.reset()  # Reset for each gate
            mlp.fit(X, y, epochs=2000, verbose=False)
            
            predictions = mlp.predict(X)
            accuracy = np.mean(predictions == y)
            assert accuracy >= 0.75, f"MLP should learn {gate} gate reasonably well"
    
    def test_history_tracking(self):
        """Test that training history is properly tracked."""
        X, y = generate_logic_gate_data('OR')
        mlp = MultiLayerPerceptron([2, 2, 1])
        mlp.fit(X, y, epochs=10)
        
        assert len(mlp.history['loss']) <= 10
        assert len(mlp.history['accuracy']) <= 10
    
    def test_reset_functionality(self):
        """Test that reset properly reinitializes the network."""
        mlp = MultiLayerPerceptron([2, 3, 1], random_seed=42)
        
        # Store initial weights
        initial_weights = [w.copy() for w in mlp.weights]
        
        # Train on some data
        X, y = generate_logic_gate_data('AND')
        mlp.fit(X, y, epochs=10)
        
        # Weights should have changed
        assert not all(np.array_equal(w1, w2) for w1, w2 in zip(initial_weights, mlp.weights))
        
        # Reset
        mlp.reset()
        
        # History should be cleared
        assert len(mlp.history['loss']) == 0
        assert len(mlp.history['accuracy']) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
