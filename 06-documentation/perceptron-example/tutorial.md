# Tutorial: Building Your First Neural Network to Solve XOR

A beginner-friendly guide to understanding neural network limitations and solutions through hands-on implementation.

## Introduction

Have you ever wondered why some problems are "hard" for computers? In this tutorial, we'll explore one of the most famous problems in AI history - the XOR problem - and build neural networks from scratch to solve it!

## What You'll Learn

- Why some problems are impossible for simple neural networks
- How adding "hidden layers" makes networks more powerful
- How to implement and train neural networks from scratch
- How to test scientific hypotheses with code

## Prerequisites

- Basic Python knowledge
- High school math (we'll explain the rest!)
- Curiosity about how AI works

## Part 1: Understanding the Problem

### What is XOR?

XOR (exclusive OR) is a simple logic function:
- Output 1 when inputs are DIFFERENT
- Output 0 when inputs are the SAME

```python
# XOR Truth Table
(0, 0) → 0  # Same inputs
(0, 1) → 1  # Different inputs  
(1, 0) → 1  # Different inputs
(1, 1) → 0  # Same inputs
```

### Why is XOR Special?

Try drawing a single straight line that separates the 1s from the 0s:

```
    Input 2
    1 |  0    1
      |
    0 |  1    0
      +--------
      0    1   Input 1
```

You can't do it! This makes XOR "non-linearly separable" - a fancy way of saying "you need a curved boundary, not a straight line."

## Part 2: Building a Single-Layer Perceptron

Let's build the simplest neural network - a single-layer perceptron:

```python
import numpy as np

class SimplePerceptron:
    def __init__(self, learning_rate=0.1):
        # Initialize random weights and bias
        self.weights = np.random.randn(2) * 0.1
        self.bias = np.random.randn() * 0.1
        self.learning_rate = learning_rate
    
    def predict(self, X):
        # Calculate: output = step(w·x + b)
        linear_output = np.dot(X, self.weights) + self.bias
        return (linear_output > 0).astype(int)
    
    def train(self, X, y, epochs=100):
        for epoch in range(epochs):
            predictions = self.predict(X)
            errors = y - predictions
            
            # Update weights when wrong
            for i in range(len(X)):
                self.weights += self.learning_rate * errors[i] * X[i]
                self.bias += self.learning_rate * errors[i]
            
            # Check accuracy
            accuracy = np.mean(predictions == y)
            if epoch % 20 == 0:
                print(f"Epoch {epoch}: Accuracy = {accuracy:.2%}")
```

### Testing on XOR

```python
# Create XOR data
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([0, 1, 1, 0])  # XOR outputs

# Train perceptron
perceptron = SimplePerceptron()
perceptron.train(X, y, epochs=100)

# Test predictions
print("\nFinal predictions:")
for inputs, target in zip(X, y):
    prediction = perceptron.predict(inputs.reshape(1, -1))[0]
    print(f"{inputs} → {prediction} (target: {target})")
```

**Result**: The perceptron fails! It can't learn XOR, getting only 50% accuracy (random guessing).

## Part 3: Building a Multi-Layer Perceptron

Now let's add a hidden layer to create a more powerful network:

```python
class MultiLayerPerceptron:
    def __init__(self, hidden_size=2, learning_rate=0.5):
        # Layer 1: input (2) → hidden (hidden_size)
        self.W1 = np.random.randn(2, hidden_size) * 0.5
        self.b1 = np.zeros((1, hidden_size))
        
        # Layer 2: hidden → output (1)
        self.W2 = np.random.randn(hidden_size, 1) * 0.5
        self.b2 = np.zeros((1, 1))
        
        self.learning_rate = learning_rate
    
    def sigmoid(self, x):
        """Smooth activation function"""
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        """Derivative for backpropagation"""
        s = self.sigmoid(x)
        return s * (1 - s)
    
    def forward(self, X):
        """Pass input through network"""
        # Hidden layer
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)
        
        # Output layer
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.sigmoid(self.z2)
        
        return self.a2
    
    def backward(self, X, y):
        """Backpropagation - the key to training deep networks!"""
        m = X.shape[0]
        
        # Output layer gradients
        dz2 = self.a2 - y.reshape(-1, 1)
        dW2 = np.dot(self.a1.T, dz2) / m
        db2 = np.mean(dz2, axis=0, keepdims=True)
        
        # Hidden layer gradients
        da1 = np.dot(dz2, self.W2.T)
        dz1 = da1 * self.sigmoid_derivative(self.z1)
        dW1 = np.dot(X.T, dz1) / m
        db1 = np.mean(dz1, axis=0, keepdims=True)
        
        # Update weights
        self.W1 -= self.learning_rate * dW1
        self.b1 -= self.learning_rate * db1
        self.W2 -= self.learning_rate * dW2
        self.b2 -= self.learning_rate * db2
    
    def train(self, X, y, epochs=1000):
        for epoch in range(epochs):
            # Forward pass
            output = self.forward(X)
            
            # Backward pass
            self.backward(X, y)
            
            # Check progress
            if epoch % 200 == 0:
                predictions = (output > 0.5).astype(int).flatten()
                accuracy = np.mean(predictions == y)
                print(f"Epoch {epoch}: Accuracy = {accuracy:.2%}")
    
    def predict(self, X):
        output = self.forward(X)
        return (output > 0.5).astype(int).flatten()
```

### Testing the Multi-Layer Network

```python
# Train multi-layer perceptron
mlp = MultiLayerPerceptron(hidden_size=2)
mlp.train(X, y, epochs=1000)

# Test predictions
print("\nFinal predictions:")
for inputs, target in zip(X, y):
    prediction = mlp.predict(inputs.reshape(1, -1))[0]
    print(f"{inputs} → {prediction} (target: {target})")
```

**Result**: Success! The multi-layer perceptron learns XOR with 100% accuracy!

## Part 4: Visualizing the Solution

Let's see how the networks create decision boundaries:

```python
import matplotlib.pyplot as plt

def plot_decision_boundary(model, X, y, title):
    # Create mesh grid
    h = 0.01
    x_min, x_max = -0.5, 1.5
    y_min, y_max = -0.5, 1.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    
    # Predict on mesh
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    # Plot
    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z, alpha=0.3, cmap='RdYlBu')
    plt.scatter(X[:, 0], X[:, 1], c=y, s=200, 
                cmap='RdYlBu', edgecolors='black', linewidth=2)
    
    # Add labels
    for i, (x, y_val) in enumerate(zip(X, y)):
        plt.annotate(f'({int(x[0])},{int(x[1])})→{int(y_val)}',
                    xy=(x[0], x[1]), xytext=(5, 5),
                    textcoords='offset points')
    
    plt.title(title)
    plt.xlabel('Input 1')
    plt.ylabel('Input 2')
    plt.show()

# Visualize both models
plot_decision_boundary(perceptron, X, y, 'Single-Layer: Linear Boundary (Fails)')
plot_decision_boundary(mlp, X, y, 'Multi-Layer: Non-Linear Boundary (Succeeds)')
```

## Part 5: Understanding What Happened

### Why Single-Layer Failed

Single-layer perceptrons can only create straight line boundaries:
- They compute: `output = step(w₁x₁ + w₂x₂ + b)`
- This is the equation of a line!
- XOR needs a curved boundary

### Why Multi-Layer Succeeded

Hidden layers enable complex boundaries:
1. **First layer** creates multiple linear boundaries
2. **Second layer** combines them into curves
3. **Non-linear activation** (sigmoid) is crucial - without it, multiple linear layers still make lines!

### The Historical Context

- **1958**: Perceptron invented - AI researchers excited!
- **1969**: Minsky & Papert prove XOR limitation - AI winter begins
- **1986**: Backpropagation solved training problem - AI renaissance!
- **Today**: Deep learning uses same principles with many more layers

## Part 6: Experiments You Can Try

### Experiment 1: Minimum Network Size
```python
# Test different hidden layer sizes
for hidden_size in [1, 2, 3, 4, 8]:
    mlp = MultiLayerPerceptron(hidden_size=hidden_size)
    mlp.train(X, y, epochs=2000)
    predictions = mlp.predict(X)
    accuracy = np.mean(predictions == y)
    print(f"Hidden size {hidden_size}: Accuracy = {accuracy:.2%}")
```

**Finding**: You need at least 2 hidden units for XOR!

### Experiment 2: Different Logic Gates
```python
# Test on simpler gates
gates = {
    'AND': [0, 0, 0, 1],
    'OR': [0, 1, 1, 1],
    'XOR': [0, 1, 1, 0]
}

for name, outputs in gates.items():
    y_gate = np.array(outputs)
    
    # Test single-layer
    slp = SimplePerceptron()
    slp.train(X, y_gate, epochs=100)
    slp_acc = np.mean(slp.predict(X) == y_gate)
    
    # Test multi-layer
    mlp = MultiLayerPerceptron()
    mlp.train(X, y_gate, epochs=1000)
    mlp_acc = np.mean(mlp.predict(X) == y_gate)
    
    print(f"{name}: Single-Layer = {slp_acc:.2%}, Multi-Layer = {mlp_acc:.2%}")
```

**Finding**: Single-layer works for AND/OR but not XOR!

### Experiment 3: Learning Dynamics
```python
# Track learning progress
def train_with_history(model, X, y, epochs=1000):
    history = []
    
    for epoch in range(epochs):
        if hasattr(model, 'forward'):
            # Multi-layer
            output = model.forward(X)
            model.backward(X, y)
            predictions = (output > 0.5).astype(int).flatten()
        else:
            # Single-layer
            predictions = model.predict(X)
            # ... training step ...
        
        accuracy = np.mean(predictions == y)
        history.append(accuracy)
    
    return history

# Compare learning curves
slp = SimplePerceptron()
mlp = MultiLayerPerceptron()

slp_history = train_with_history(slp, X, y)
mlp_history = train_with_history(mlp, X, y)

plt.plot(slp_history, label='Single-Layer')
plt.plot(mlp_history, label='Multi-Layer')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Learning Curves on XOR')
plt.legend()
plt.show()
```

## Key Takeaways

1. **Not all problems are equal**: Some require more complex models
2. **Architecture matters**: Hidden layers enable non-linear decision boundaries
3. **Activation functions are crucial**: Non-linearity is required for complex patterns
4. **Historical lessons**: Understanding limitations drives innovation

## Next Steps

Now that you understand the XOR problem:

1. **Try 3-input XOR** (parity problem) - Do you need more hidden units?
2. **Implement different activations** - Try ReLU instead of sigmoid
3. **Visualize hidden layer** - What features does it learn?
4. **Scale up** - Can you solve real image classification?

## Complete Code

Find all code from this tutorial in:
- Implementation: `03-implementation/perceptron-example/`
- Experiments: `04-experiments/perceptron-example/`
- Analysis: `05-analysis/perceptron-example/`

## Resources for Further Learning

- **Visual Introduction to Neural Networks**: [3Blue1Brown Series](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)
- **Deep Learning Book**: [Goodfellow, Bengio & Courville](https://www.deeplearningbook.org/)
- **Neural Networks Playground**: [TensorFlow Playground](https://playground.tensorflow.org/)

## Conclusion

Congratulations! You've just:
- Discovered a fundamental limitation of simple neural networks
- Built a solution using hidden layers
- Understood why this took 25+ years historically
- Gained insights applicable to modern deep learning

The XOR problem might seem simple, but it teaches profound lessons about neural network capabilities and limitations. Every modern AI system, from ChatGPT to computer vision models, builds on these same principles you've just mastered!

---

*This tutorial is part of the Average Joes Lab Research Engineering Learning Path. Start your own research journey at [averagejoeslab.com](https://averagejoeslab.com/docs/research-engineering/getting-started)*
