# Phase 3: Hypothesis Design

## 🎯 Week 9-10: Research Project Design & Experimental Rigor

This folder contains your original research project design and hypothesis formation.

### Getting Started

Design your original research project to address limitations discovered in Phase 2:

1. **Hypothesis Formation**
2. **Experimental Design**
3. **Ablation Planning**
4. **Statistical Planning**

### Recommended Files

- `research-proposal.md` - Complete research proposal
- `hypothesis.md` - Clear, testable hypotheses
- `experimental-design.md` - Detailed experimental methodology
- `ablation-plan.md` - Systematic component analysis strategy
- `statistical-plan.md` - Statistical analysis methodology

### Research Proposal Template

#### 1. Problem Statement
- What limitation did you discover in Phase 2?
- Why is this limitation important to address?
- What gap in knowledge does this represent?

#### 2. Research Questions
- Primary research question
- Secondary research questions
- Specific, measurable, achievable questions

#### 3. Hypotheses
- Clear, testable hypotheses
- Null and alternative hypotheses
- Expected outcomes and reasoning

#### 4. Methodology
- Experimental approach
- Controls and variables
- Data collection methods
- Analysis techniques

#### 5. Expected Contributions
- What new knowledge will this generate?
- How will this advance the field?
- What are the practical implications?

### Experimental Design Framework

#### Variables
- **Independent Variables**: What you're manipulating
- **Dependent Variables**: What you're measuring
- **Control Variables**: What you're keeping constant
- **Confounding Variables**: What might interfere

#### Controls
- **Positive Controls**: Known to work
- **Negative Controls**: Known to fail
- **Baseline Comparisons**: Standard methods
- **Ablation Controls**: Component removal

### Example: Perceptron to MLP Research

If following the Perceptron example:

#### Research Question
"Can multi-layer neural networks solve problems that single-layer perceptrons cannot?"

#### Hypothesis
"Multi-layer perceptrons with hidden layers can learn non-linearly separable functions like XOR, while single-layer perceptrons cannot."

#### Experimental Design
1. **Comparison Study**: Single-layer vs multi-layer performance
2. **Problem Set**: AND, OR (linearly separable) vs XOR (non-linearly separable)
3. **Architecture Variations**: Test 2-layer, 3-layer networks
4. **Training Methods**: Explore different training approaches

#### Ablation Plan
- Test impact of hidden layer size
- Test different activation functions
- Test various initialization methods
- Test learning rate sensitivity

### Learning Resources

#### Research Project Design (Week 9-10)
- **Hypothesis Formation**: [UNC Writing Center: Research Questions](https://writingcenter.unc.edu/tips-and-tools/research-questions/) | [PICO Framework](https://guides.library.oregonstate.edu/c.php?g=286121&p=1906399)
- **Experimental Design**: [Khan Academy: Designing Studies](https://www.khanacademy.org/math/statistics-probability/designing-studies) | [Randomized Controlled Trials](https://www.bmj.com/about-bmj/resources-readers/publications/epidemiology-uninitiated/7-randomised-controlled-trials)
- **Ablation Planning**: [Ablation Studies Guide](https://towardsdatascience.com/ablation-studies-in-machine-learning-what-why-and-how-f3e73c3b3b4e) | [Component Analysis Methods](https://www.nature.com/articles/s41598-019-42759-4)

#### Statistical Planning
- **Power Analysis**: [Statistical Power Guide](https://www.statisticssolutions.com/statistical-power-analysis/) | [Effect Size Calculator](https://www.psychometrica.de/effect_size.html)
- **Sample Size Calculation**: [Sample Size Determination](https://www.statisticshowto.com/probability-and-statistics/find-sample-size/)
- **Statistical Tests Selection**: [Choosing Statistical Tests](https://www.scribbr.com/statistics/statistical-tests/)
- **Reproducibility Protocol**: [FAIR Data Principles](https://www.go-fair.org/fair-principles/) | [Reproducibility Checklist](https://www.cs.mcgill.ca/~jpineau/ReproducibilityChecklist.pdf)

### Statistical Planning Framework

#### Power Analysis Template
```python
import scipy.stats as stats
import numpy as np

def calculate_sample_size(effect_size, alpha=0.05, power=0.8):
    """
    Calculate required sample size for detecting effect
    """
    # For t-test comparison
    from scipy.stats import norm
    
    z_alpha = norm.ppf(1 - alpha/2)
    z_beta = norm.ppf(power)
    
    n = 2 * ((z_alpha + z_beta) / effect_size) ** 2
    return int(np.ceil(n))

# Example: Detect medium effect size (d=0.5)
required_n = calculate_sample_size(effect_size=0.5)
print(f"Required sample size per group: {required_n}")
```

#### Statistical Test Selection Guide
```python
def select_statistical_test(data_type, groups, distribution):
    """
    Guide for selecting appropriate statistical tests
    """
    tests = {
        ('continuous', 2, 'normal'): 'Independent t-test',
        ('continuous', 2, 'non_normal'): 'Mann-Whitney U test',
        ('continuous', '>2', 'normal'): 'One-way ANOVA',
        ('continuous', '>2', 'non_normal'): 'Kruskal-Wallis test',
        ('categorical', 2, 'any'): 'Chi-square test',
        ('paired', 2, 'normal'): 'Paired t-test',
        ('paired', 2, 'non_normal'): 'Wilcoxon signed-rank test'
    }
    
    key = (data_type, groups, distribution)
    return tests.get(key, 'Consult statistician')
```

### Enhanced Perceptron Example Research Design

#### Complete Research Proposal Template

##### 1. Problem Statement
**Limitation Discovered**: Single-layer perceptrons cannot solve non-linearly separable problems like XOR.

**Research Gap**: While multi-layer architectures were proposed in 1962, effective training methods weren't developed until 1986. This 25-year gap represents a critical implementation bottleneck in neural network research.

**Significance**: Understanding this historical bottleneck demonstrates how research engineering methodology can systematically identify and address fundamental limitations in proposed solutions.

##### 2. Research Questions
**Primary**: Can multi-layer perceptrons solve non-linearly separable problems that single-layer perceptrons cannot?

**Secondary**: 
- What architectural factors (hidden units, layers) affect MLP performance on XOR?
- Why did the field struggle for 25 years to train MLPs effectively?
- How does systematic experimentation reveal implementation bottlenecks?

##### 3. Hypotheses
**H1**: Multi-layer perceptrons with hidden layers can learn XOR function (accuracy > 90%)
**H0**: Multi-layer perceptrons perform no better than single-layer perceptrons on XOR (accuracy ≤ 50%)

**H2**: MLP performance on XOR increases with hidden layer size up to optimal point
**H0**: Hidden layer size has no effect on XOR learning performance

**H3**: Without backpropagation, MLPs cannot be trained effectively on XOR
**H0**: Training method has no effect on MLP performance

##### 4. Experimental Design

###### Variables
- **Independent Variables**: 
  - Architecture type (single-layer vs multi-layer)
  - Hidden layer size (2, 4, 8, 16 units)
  - Training method (random updates vs backpropagation)
- **Dependent Variables**: 
  - Classification accuracy on XOR
  - Training convergence time
  - Training stability (loss variance)
- **Control Variables**: 
  - Learning rate (0.1)
  - Random seed management
  - Training epochs (1000)
  - Input data (standardized XOR dataset)

###### Controls and Baselines
- **Negative Control**: Random classifier (expected 50% accuracy)
- **Positive Control**: Known working solution (if available)
- **Baseline**: Single-layer perceptron performance
- **Historical Control**: Pre-backpropagation training methods

##### 5. Statistical Analysis Plan

###### Sample Size Calculation
```python
# Expecting large effect size (d=1.5) for architecture comparison
required_n = calculate_sample_size(effect_size=1.5, alpha=0.05, power=0.9)
print(f"Required runs per condition: {required_n}")  # Likely ~8-10 runs

# For ablation studies (medium effect size d=0.5)
ablation_n = calculate_sample_size(effect_size=0.5, alpha=0.05, power=0.8)
print(f"Required runs for ablation: {ablation_n}")  # Likely ~16-20 runs
```

###### Statistical Tests Planned
1. **Architecture Comparison**: Independent t-test (perceptron vs MLP accuracy)
2. **Hidden Unit Analysis**: One-way ANOVA (effect of hidden layer size)
3. **Training Method Comparison**: Independent t-test (random vs backpropagation)
4. **Multiple Comparisons**: Bonferroni correction for family-wise error rate

###### Effect Size Interpretation
- **Small effect**: d = 0.2 (minimal practical significance)
- **Medium effect**: d = 0.5 (moderate practical significance)  
- **Large effect**: d = 0.8+ (substantial practical significance)

##### 6. Reproducibility Protocol

###### Environment Documentation
```yaml
# research-environment.yml
name: perceptron-research
dependencies:
  - python=3.9
  - numpy=1.21.0
  - matplotlib=3.4.2
  - scipy=1.7.0
  - jupyter=1.0.0
  - pytest=6.2.4
```

###### Experiment Configuration
```yaml
# experiment-config.yml
random_seeds: [42, 123, 456, 789, 999, 111, 222, 333, 444, 555]
architectures:
  single_layer: [1]
  multi_layer_small: [2, 1]
  multi_layer_medium: [4, 1] 
  multi_layer_large: [8, 1]
training_parameters:
  learning_rate: 0.1
  max_epochs: 1000
  convergence_threshold: 0.01
```

### Just-in-Time Learning Checkpoints

**Week 9**: Research design fundamentals
- **If you need**: Hypothesis formation → [Research Question Guide](https://writingcenter.unc.edu/tips-and-tools/research-questions/)
- **If you need**: Experimental design → [Designing Studies](https://www.khanacademy.org/math/statistics-probability/designing-studies)
- **If you need**: Statistical concepts → [Statistics Fundamentals](https://www.khanacademy.org/math/statistics-probability)

**Week 10**: Statistical planning and power analysis
- **If you need**: Power analysis → [Statistical Power Guide](https://www.statisticssolutions.com/statistical-power-analysis/)
- **If you need**: Effect sizes → [Effect Size Interpretation](https://www.statisticshowto.com/probability-and-statistics/effect-size/)
- **If you need**: Sample size calculation → [Sample Size Methods](https://www.statisticshowto.com/probability-and-statistics/find-sample-size/)

### Milestone

Complete a well-designed original research project with clear hypotheses, rigorous experimental methodology, and systematic ablation planning.
