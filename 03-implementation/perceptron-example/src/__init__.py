"""
Perceptron Research Implementation

This module implements both single-layer and multi-layer perceptrons
to investigate the XOR problem and test our research hypotheses.
"""

from .single_layer_perceptron import SingleLayerPerceptron
from .multi_layer_perceptron import MultiLayerPerceptron
from .data_utils import generate_logic_gate_data, visualize_decision_boundary
from .evaluation import evaluate_model, run_experiment

__all__ = [
    'SingleLayerPerceptron',
    'MultiLayerPerceptron',
    'generate_logic_gate_data',
    'visualize_decision_boundary',
    'evaluate_model',
    'run_experiment'
]
