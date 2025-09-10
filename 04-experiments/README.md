# Step 5: Systematic Experimentation

**Research Step**: Experimentation

## Overview

Use your implementation to systematically test your hypotheses. This is where you generate the data that will answer your research questions.

## Your Task

Design and execute rigorous experiments that test each of your hypotheses with proper controls and statistical methodology.

## File Structure

```
04-experiments/
├── README.md                    # This guide
├── perceptron-example/          # ✅ COMPLETE EXPERIMENTS
│   ├── run_experiments.py       # Automated experiment runner
│   ├── experiment-logs/         # Detailed experiment records
│   ├── results/                 # Data and visualizations
│   └── notebooks/               # Experimental notebooks
└── your-work/                   # Your experiments
    ├── experiment-logs/
    ├── results/
    └── notebooks/
```

## Complete Perceptron Experiments Available! ✅

The `perceptron-example/` folder contains fully executed experiments:
- **Hypothesis testing**: Single vs multi-layer on XOR (20 runs each)
- **Architecture scaling**: Testing 2-16 hidden units
- **Comprehensive testing**: All 5 logic gates
- **Statistical analysis**: t-tests, effect sizes, confidence intervals
- **Automated runner**: `run_experiments.py` executes all tests

## Experimental Methodology

### Research Engineering Principles
1. **Systematic approach**: Test one variable at a time
2. **Proper controls**: Include baselines and comparisons
3. **Statistical rigor**: Multiple runs, significance testing
4. **Documentation**: Record everything for reproducibility
5. **Honest reporting**: Document failures as well as successes

### Experimental Design Framework
- **Independent variables**: What you're manipulating
- **Dependent variables**: What you're measuring
- **Control variables**: What you're keeping constant
- **Confounding variables**: What might interfere

## Types of Experiments

### Hypothesis Testing Experiments
**Purpose**: Test your specific predictions
**Design**: Direct comparison between conditions
**Analysis**: Statistical tests for significance

### Ablation Studies
**Purpose**: Understand which components matter
**Design**: Systematically remove/modify components
**Analysis**: Component importance ranking

### Parameter Sweeps
**Purpose**: Find optimal configurations
**Design**: Systematic variation of parameters
**Analysis**: Performance landscapes and sensitivity

### Failure Mode Analysis
**Purpose**: Understand limitations and boundaries
**Design**: Test edge cases and challenging scenarios
**Analysis**: Characterize when/why methods fail

## Experiment Documentation

### Experiment Log Template
For each experiment, document:

```markdown
# Experiment: [Name]
**Date**: [YYYY-MM-DD]
**Objective**: [What are you testing?]

## Hypothesis
[Which hypothesis this tests and specific prediction]

## Configuration
- **Parameters**: [All settings and values]
- **Data**: [Dataset, size, preprocessing]
- **Environment**: [Software versions, hardware]
- **Random seeds**: [For reproducibility]

## Results
- **Primary metrics**: [Main measurements]
- **Statistical analysis**: [p-values, effect sizes, confidence intervals]
- **Visualizations**: [Plots and charts]

## Observations
- **Expected results**: [What matched predictions]
- **Surprises**: [Unexpected findings]
- **Failures**: [What didn't work and why]

## Conclusions
- **Hypothesis support**: [Supported/refuted/partially supported]
- **Key insights**: [What you learned]
- **Next experiments**: [What to test next]
```

## Learning Resources

### Experimental Design
- **[Experimental Design Basics](https://www.khanacademy.org/math/statistics-probability/designing-studies)** - Controls and variables
- **[Scientific Method](https://www.khanacademy.org/science/biology/intro-to-biology/science-of-biology/a/experiments-and-observations)** - Systematic investigation

### Statistical Analysis
- **[Statistical Tests Guide](https://www.scribbr.com/statistics/statistical-tests/)** - Choosing appropriate tests
- **[Effect Size Interpretation](https://www.statisticshowto.com/probability-and-statistics/effect-size/)** - Practical significance

### Research Tools
- **[MLflow](https://mlflow.org/docs/latest/index.html)** - Experiment tracking
- **[Jupyter](https://jupyter.org/)** - Interactive experimentation
- **[Matplotlib](https://matplotlib.org/stable/tutorials/index.html)** - Data visualization

## Success Criteria

By completing this step, you should have:
- [ ] **Systematic test results** for all hypotheses
- [ ] **Statistical analysis** with proper significance testing
- [ ] **Comprehensive documentation** of all experiments
- [ ] **Clear findings** about what works and what doesn't
- [ ] **Identified limitations** for future research

## Common Experimental Challenges

### Challenge: Results Don't Support Hypotheses
**Solution**: This is valuable! Negative results teach us about limitations

### Challenge: Experiments Take Too Long
**Solution**: Start with pilot studies, scale up after validating approach

### Challenge: Too Many Variables
**Solution**: Test one factor at a time, use systematic ablation

### Challenge: Inconsistent Results
**Solution**: Check for random seed issues, increase sample size

## Experimental Strategy

### Core Hypothesis Testing
- [ ] Test primary hypothesis with direct comparison
- [ ] Run multiple trials for statistical validity
- [ ] Document baseline performance
- [ ] Analyze initial results

### Systematic Investigation
- [ ] Conduct ablation studies
- [ ] Test parameter sensitivity
- [ ] Explore failure modes
- [ ] Compile comprehensive results

## Quick Start with Perceptron Experiments

```bash
# Navigate to experiments
cd 04-experiments/perceptron-example/

# Run all experiments
python run_experiments.py

# This will:
# 1. Test single vs multi-layer on XOR (Experiment 1)
# 2. Test different hidden layer sizes (Experiment 2)  
# 3. Test all logic gates (Experiment 3)
# 4. Generate statistical reports in experiment-logs/
# 5. Save visualizations in results/

# View results
cat experiment-logs/SUMMARY.md
```

### Expected Results from Perceptron Example
- **Single-layer on XOR**: ~38% accuracy (random performance)
- **Multi-layer on XOR**: ~94% accuracy (successful learning)
- **Statistical significance**: p < 0.001, Cohen's d > 9.0
- **Minimum architecture**: 2 hidden units required for XOR

## Next Steps

Once your experiments are complete:
1. **Move to Step 6-7**: [Analysis & Iteration](../05-analysis/)
2. **Interpret your findings**: What do the results mean?
3. **Plan iterations**: How will you refine your approach?

---

**Remember**: Experiments are conversations with reality. Listen carefully to what your results are telling you, even if it's not what you expected to hear.
