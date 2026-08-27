# 150k Batch Construction Plan

The complete pre-defined schedule is `configs/batch_plan_150k.csv`.

The schedule contains **3,000 batches of 50 examples**. It is balanced at the primary-target level:

- 40 linguistic variables
- 3,750 primary examples per variable
- 5 construction families per variable
- 750 primary examples per variable × construction family
- 15 batches for every variable × construction family combination

Within a variable/construction combination, the schedule rotates across the variable's preferred XGLM-supported languages. Each batch also rotates across three lexical domains and requests 15 short, 25 medium, and 10 long examples.

Batch order is deterministically shuffled with seed `150040`, so a partial run is not simply a long block of one variable.

The generation script builds every individual prompt from the row in this schedule plus `configs/variable_constructions.yaml`.
