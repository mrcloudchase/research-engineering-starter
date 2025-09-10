# Your Experiments

This is your workspace for Step 5: Systematic Experimentation.

## Getting Started

1. Review the experiment log example in `../perceptron-example/experiment-log.md`
2. Design experiments to test each of your hypotheses
3. Run experiments systematically with proper controls
4. Document everything for reproducibility

## Experiment Structure

```
your-work/
├── experiment-logs/          # Detailed experiment records
│   ├── experiment-01.md     # Hypothesis 1 test
│   ├── experiment-02.md     # Hypothesis 2 test
│   └── ablation-study.md    # Component analysis
├── results/                  # Data and outputs
│   ├── data/                # Raw experimental data
│   ├── figures/             # Plots and visualizations
│   └── statistics/          # Statistical analyses
└── notebooks/               # Experimental notebooks
    ├── hypothesis-testing.ipynb
    └── exploratory-analysis.ipynb
```

## Experiment Log Template

For each experiment, document:

```markdown
# Experiment: [Name]
**Date**: [YYYY-MM-DD]
**Objective**: [What are you testing?]

## Hypothesis
[Which hypothesis and specific prediction]

## Configuration
- Parameters: [All settings]
- Data: [Dataset details]
- Environment: [Software/hardware]
- Random seeds: [For reproducibility]

## Results
- Primary metrics: [Key measurements]
- Statistical analysis: [p-values, effect sizes]
- Visualizations: [Link to plots]

## Observations
- Expected: [What matched predictions]
- Unexpected: [Surprises]
- Failures: [What didn't work]

## Conclusions
- Hypothesis: [Supported/Refuted/Partial]
- Key insights: [What you learned]
- Next steps: [Follow-up experiments]
```

## Experimental Best Practices

### Design Principles
- **One variable at a time**: Isolate what you're testing
- **Proper controls**: Include baselines and comparisons
- **Multiple runs**: Account for randomness
- **Statistical rigor**: Use appropriate tests

### Documentation
- **Record everything**: Even "failed" experiments
- **Be specific**: Exact parameters and configurations
- **Include timestamps**: When experiments were run
- **Version control**: Commit experiment logs

### Analysis
- **Statistical significance**: p-values and confidence intervals
- **Effect sizes**: Practical significance
- **Visualizations**: Plots that tell the story
- **Reproducibility**: Can someone else repeat this?

## Common Experiment Types

1. **Direct Hypothesis Test**: Test your main predictions
2. **Ablation Study**: Remove components to test importance
3. **Parameter Sweep**: Find optimal configurations
4. **Failure Analysis**: Understand when/why methods fail
5. **Comparison Study**: Compare against baselines

## Tips

- **Start with pilot studies**: Small tests before full experiments
- **Expect surprises**: Experiments reveal unexpected truths
- **Document failures**: They're as valuable as successes
- **Be systematic**: Follow your experimental plan
- **Stay objective**: Let data speak, not hopes

When complete, move to [Step 6-7: Analysis](../../05-analysis/)
