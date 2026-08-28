# Causal Interventions — Steps 7–9

Final causal-intervention artifacts for the Low-Rank Linguistic Features project.

## Step 7
SAE feature ablation across all 40 linguistic variables.

## Step 8
SAE decoder-direction steering at 0.5x, 1x, and 2x doses.

## Pre-behavior freeze
15 variables were frozen as the primary mechanistic cohort before behavioral results were inspected.

## Step 9
Next-token branch-point behavioral evaluation using the frozen 1x primary steering dose.

The initial bfloat16 behavioral diagnostic showed quantized logit differences.
The canonical Step-9 evaluation was therefore rerun in float32 without changing
the cohort, candidate features, controls, doses, metric, test split, or
multiple-comparison procedure.

## Final full-chain results

Variable IDs:

10, 17, 19, 21, 23, 27

These six variables showed convergent evidence across ablation, steering,
matched controls, monotonic steering response, and FDR-corrected behavioral
effects.