# Phase 2: Implementation

## 💻 Week 5-6: Programming for Research

This folder contains your implementation of the chosen research paper.

### Getting Started

Implement your chosen paper from scratch following research engineering practices:

1. **Code Implementation**
2. **Testing and Validation**
3. **Documentation**
4. **Reproducibility**

### Recommended Structure

Organize your implementation with these files/folders:

- `src/` - Source code implementation
- `tests/` - Unit tests and validation
- `data/` - Datasets and data files
- `notebooks/` - Jupyter notebooks for exploration
- `requirements.txt` - Python dependencies
- `README.md` - Implementation documentation

### Implementation Guidelines

#### Code Organization
```
implementation/
├── src/
│   ├── __init__.py
│   ├── model.py          # Main algorithm implementation
│   ├── data_utils.py     # Data loading and preprocessing
│   ├── evaluation.py     # Evaluation metrics and testing
│   └── visualization.py  # Plotting and visualization
├── tests/
│   ├── test_model.py
│   ├── test_data_utils.py
│   └── test_evaluation.py
├── notebooks/
│   ├── exploration.ipynb
│   └── validation.ipynb
├── data/
│   └── datasets/
├── requirements.txt
└── README.md
```

#### Best Practices
- **Clean, readable code** with clear variable names
- **Comprehensive comments** explaining the algorithm
- **Modular design** with separate functions for each component
- **Error handling** for edge cases
- **Unit tests** for all major functions

### Example: Perceptron Implementation

If following the Perceptron example:

1. **Core Algorithm** (`src/model.py`)
   - Perceptron class with fit() and predict() methods
   - Weight initialization and update rules
   - Activation function implementation

2. **Data Utilities** (`src/data_utils.py`)
   - Logic gate dataset generation (AND, OR, XOR)
   - Data preprocessing and normalization
   - Train/test split functionality

3. **Evaluation** (`src/evaluation.py`)
   - Accuracy calculation
   - Confusion matrix generation
   - Learning curve plotting

### Learning Resources

#### Programming for Research (Week 5-6)
- **Python Fundamentals**: [Python.org Beginner's Guide](https://www.python.org/about/gettingstarted/) | [Automate the Boring Stuff (Free)](https://automatetheboringstuff.com/)
- **Jupyter Notebooks**: [Jupyter.org Getting Started](https://jupyter.org/try) | [Real Python: Jupyter Tutorial](https://realpython.com/jupyter-notebook-introduction/)
- **Version Control**: [Git Tutorial by Atlassian](https://www.atlassian.com/git/tutorials) | [GitHub Skills](https://skills.github.com/)
- **Collaborative Coding**: [GitHub Flow Guide](https://guides.github.com/introduction/flow/) | [Scientific Computing Best Practices](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745)

#### Testing and Documentation
- **Unit Testing**: [pytest Documentation](https://docs.pytest.org/en/stable/)
- **Code Documentation**: [Real Python: Documenting Python Code](https://realpython.com/documenting-python-code/)
- **Code Quality**: [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)

### Perceptron Implementation Guide

If following the Perceptron example:

#### Week 5: Core Implementation
**Goal**: Implement perceptron algorithm from scratch (~50 lines of code)

##### Essential Components
1. **Perceptron Class** (`src/model.py`)
```python
import numpy as np

class Perceptron:
    def __init__(self, learning_rate=0.1, max_epochs=100):
        self.learning_rate = learning_rate
        self.max_epochs = max_epochs
        self.weights = None
        self.bias = None
    
    def fit(self, X, y):
        # Initialize weights and bias
        # Implement training loop
        # Update weights based on errors
        pass
    
    def predict(self, X):
        # Implement prediction logic
        pass
```

2. **Data Utilities** (`src/data_utils.py`)
```python
def generate_logic_gate_data(gate_type='AND'):
    """Generate training data for logic gates"""
    if gate_type == 'AND':
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y = np.array([0, 0, 0, 1])
    elif gate_type == 'OR':
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y = np.array([0, 1, 1, 1])
    elif gate_type == 'XOR':
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y = np.array([0, 1, 1, 0])  # This will fail!
    return X, y
```

##### Learning Resources for Implementation
- **Neural Networks from Scratch**: [NNFS.io Tutorial](https://nnfs.io/)
- **Perceptron Algorithm**: [Machine Learning Mastery Guide](https://machinelearningmastery.com/implement-perceptron-algorithm-scratch-python/)
- **NumPy Basics**: [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html)

#### Week 6: Testing and Validation
**Goal**: Validate implementation and discover limitations

##### Testing Strategy
1. **Unit Tests** (`tests/test_model.py`)
```python
import pytest
from src.model import Perceptron
from src.data_utils import generate_logic_gate_data

def test_perceptron_and_gate():
    X, y = generate_logic_gate_data('AND')
    model = Perceptron()
    model.fit(X, y)
    predictions = model.predict(X)
    assert np.array_equal(predictions, y)

def test_perceptron_xor_gate():
    # This test will fail - that's the point!
    X, y = generate_logic_gate_data('XOR')
    model = Perceptron()
    model.fit(X, y)
    predictions = model.predict(X)
    # Document this failure for Phase 3 research
```

2. **Validation Notebook** (`notebooks/validation.ipynb`)
- Test on AND, OR gates (should work)
- Test on XOR gate (should fail)
- Visualize decision boundaries
- Document the XOR limitation discovery

##### Key Discovery
**The XOR Problem**: Your perceptron will fail on XOR - this is a famous limitation that drove the development of multi-layer networks. Document this failure carefully as it becomes your Phase 3 research question!

### Just-in-Time Learning Checkpoints

**Week 5**: Focus on core programming skills
- **If you need**: Python basics → [Codecademy Python Course](https://www.codecademy.com/learn/learn-python-3)
- **If you need**: NumPy fundamentals → [NumPy Tutorial](https://numpy.org/doc/stable/user/quickstart.html)
- **If you need**: Object-oriented programming → [Real Python OOP Guide](https://realpython.com/python3-object-oriented-programming/)

**Week 6**: Focus on testing and validation
- **If you need**: Testing concepts → [pytest Getting Started](https://docs.pytest.org/en/stable/getting-started.html)
- **If you need**: Data visualization → [Matplotlib Tutorial](https://matplotlib.org/stable/tutorials/index.html)
- **If you need**: Linear algebra review → [Khan Academy Linear Algebra](https://www.khanacademy.org/math/linear-algebra)

### Milestone

Implement and reproduce your chosen research paper with clean, documented, and tested code (~50-200 lines depending on complexity).
