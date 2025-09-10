# Perceptron Implementation Example

Complete implementation of single-layer and multi-layer perceptrons to test hypotheses about the XOR problem.

## Implementation Structure

```
perceptron-example/
├── src/
│   ├── __init__.py
│   ├── perceptron.py         # Single-layer perceptron
│   ├── mlp.py                # Multi-layer perceptron
│   ├── activation.py         # Activation functions
│   ├── data_utils.py         # Logic gate data generation
│   └── visualization.py      # Decision boundary plotting
├── tests/
│   ├── test_perceptron.py    # Unit tests for perceptron
│   ├── test_mlp.py           # Unit tests for MLP
│   └── test_data_utils.py    # Data generation tests
└── notebooks/
    ├── exploration.ipynb      # Initial exploration
    └── xor_experiments.ipynb  # XOR problem analysis
```

## Key Implementation Details

### Single-Layer Perceptron
- **Algorithm**: Rosenblatt's original learning rule
- **Activation**: Step function (binary threshold)
- **Learning**: Error-driven weight updates
- **Limitation**: Cannot solve XOR

### Multi-Layer Perceptron
- **Architecture**: Input → Hidden → Output layers
- **Activation**: Sigmoid/tanh for non-linearity
- **Learning**: Initially random, then backpropagation
- **Capability**: Solves XOR successfully

## Research Engineering Practices

### Code Quality
- Clean, documented code with type hints
- Comprehensive unit tests for validation
- Modular design for easy experimentation
- Reproducible with fixed random seeds

### Version Control
- Each experiment gets a git commit
- Clear commit messages documenting changes
- Tagged versions for major milestones

### Documentation
- Docstrings for all functions and classes
- README files explaining usage
- Notebooks showing exploration process

## Running the Implementation

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Explore with notebooks
jupyter lab notebooks/
```

## Historical Context

This implementation recreates Rosenblatt's 1958 perceptron and explores why it took until 1986 for effective multi-layer training (backpropagation) to emerge, despite the architecture being proposed in 1962.

## Key Findings Preview

- Single-layer perceptron learns AND/OR perfectly
- Single-layer perceptron fails completely on XOR
- 2-layer MLP with 2 hidden units solves XOR
- Random weight updates fail to train MLPs effectively
- Backpropagation enables reliable MLP training

Next: [Step 5: Experiments](../../04-experiments/)
