# Canonical XGLM-564M Sparse Autoencoder

This directory documents the canonical sparse autoencoder used in the **Low-Rank Linguistic Features** project.

The purpose of this artifact is to record the exact SAE architecture, training choice, inference conversion, and evaluation evidence used by all downstream linguistic-feature analyses.

---

## 1. Base model and activation site

The SAE was trained on activations from:

- **Base model:** `facebook/xglm-564M`
- **Hidden-state index:** `12`
- **Residual width / SAE input dimension:** `1024`
- **SAE width:** `16,384`
- **Expansion factor:** `16x`

The SAE was trained on token-level residual activations from broad multilingual natural text.

The controlled linguistic contrast dataset was **not** used for SAE training.

---

## 2. SAE training corpus

The final natural-text SAE corpus contained:

- **149,338 examples**
- **3,266,346 total unique-corpus tokens**
- **3,101,336 training tokens**
- **165,010 validation tokens**
- **20 languages**

The controlled feature dataset and the SAE training corpus were kept separate so that sparse features were not learned only from synthetic basis/changed examples.

The training corpus was tokenized with:

- `facebook/xglm-564M`
- `add_special_tokens=False`
- maximum context length `192`

No padding-token activations were stored.

---

## 3. Activation normalization

XGLM hidden-state activations were normalized before SAE encoding.

The exact frozen scale is:

```text
activation_scale = 0.02065550797801016
```

Every downstream use of the canonical SAE must apply the same scale before encoding.

Conceptually:

```text
XGLM hidden state 12
    ↓
multiply by 0.02065550797801016
    ↓
canonical SAE encoder
```

Using unscaled activations would not reproduce the trained SAE behavior.

---

## 4. Initial JumpReLU experiments

The first SAE architecture investigated was JumpReLU.

Repeated JumpReLU experiments produced severe dictionary collapse despite strong reconstruction quality.

The original 16x JumpReLU model reached approximately:

```text
validation explained variance ≈ 0.9922
validation L0                 ≈ 39.7
dead features                 = 15,639 / 16,384
dead fraction                 ≈ 95.45%
```

Several modifications were tested, including:

- direct threshold parameterization;
- lower L0 coefficients;
- reduced threshold learning rates;
- dead-feature-aware pre-activation loss;
- reduced dictionary width.

These changes improved feature survival but did not eliminate progressive dictionary collapse.

A corrected dead-aware JumpReLU implementation still produced large numbers of dead features.

Reducing the dictionary from 16x to 8x did not solve the problem and reduced the number of usable features.

The JumpReLU training path was therefore abandoned.

---

## 5. BatchTopK architecture

The successful SAE architecture was BatchTopK.

The canonical training configuration used:

```text
architecture       = BatchTopK
d_in               = 1024
d_sae              = 16384
expansion factor    = 16x
k                   = 256
aux_k               = 512
aux penalty         = 1/32
epochs              = 4
token batch size    = 4096
learning rate       = 1e-4
Adam beta1          = 0.9
Adam beta2          = 0.999
dead-feature window = 250 steps
```

BatchTopK applies a global top-k selection over the flattened batch × feature activation tensor during training.

This architecture immediately produced a substantially healthier dictionary than the JumpReLU runs.

---

## 6. Canonical 4-epoch BatchTopK result

The 4-epoch BatchTopK run produced:

```text
validation MSE                 = 0.0044971306
validation explained variance  = 0.9986338739
validation cosine similarity   = 0.9945938010
validation mean L0             = 256.0
validation active fraction     = 0.015625

validation zero-fire features  = 505
validation zero-fire fraction  = 0.03082

trainer dead features          = 85
trainer dead fraction          = 0.00519
```

Full-corpus evaluation showed:

```text
full-corpus zero-fire features = 12
full-corpus zero-fire fraction ≈ 0.0007
full-corpus active features    = 16,372 / 16,384

frequency > 1e-5               = 15,416 approximately during comparison
frequency > 1e-4               = 13,921 approximately during comparison
frequency > 1e-3               = 12,567 approximately during comparison
```

The later fixed-threshold inference evaluation gave the final exact corpus-frequency values recorded below.

---

## 7. 8-epoch diagnostic run

A longer 8-epoch BatchTopK run was trained as a diagnostic.

It slightly improved reconstruction:

```text
validation MSE                = 0.0035041506
validation explained variance = 0.9989355187
validation cosine similarity  = 0.9957445628
validation mean L0            = 256.0
```

However, dictionary coverage degraded:

```text
validation zero-fire features = 1,359
trainer dead features         = 879
full-corpus zero-fire         ≈ 620
full-corpus active features   = 15,764
```

The additional four epochs therefore yielded only a very small reconstruction gain while producing substantially more feature death.

For linguistic feature discovery, dictionary coverage was prioritized over the negligible reconstruction improvement.

The **4-epoch BatchTopK model was selected as canonical**.

The 8-epoch model should be interpreted only as an overtraining diagnostic / ablation.

---

## 8. Why native BatchTopK inference was not used

Native BatchTopK inference depends on the other examples present in the inference batch.

That is unsuitable for controlled linguistic analysis because the representation assigned to one sentence should not change when unrelated sentences are added to or removed from its batch.

The trained BatchTopK SAE was therefore converted to a fixed-threshold inference representation.

This follows the same general convention used by SAE Lens BatchTopK SAEs, which are exported to fixed-threshold JumpReLU-style inference.

---

## 9. BatchTopK → fixed-threshold JumpReLU conversion

The final 4-epoch BatchTopK weights were frozen.

A global activation threshold was calibrated using **training activations only**.

The calibration scanned 758 training batches and tracked the minimum positive activation selected by native BatchTopK.

The resulting threshold was:

```text
threshold = 0.11494007418131039
```

Calibration statistics:

```text
batches      = 758
cutoff mean  = 0.1151056066
cutoff min   = 0.0923736542
cutoff max   = 0.1384065896
EMA lr       = 0.01
```

The exported inference SAE uses:

```text
raw = ReLU((x_scaled - b_dec) @ W_enc + b_enc)
acts = raw where raw > threshold else 0
```

No BatchTopK operation is used during downstream inference.

---

## 10. Fixed-threshold inference evaluation

The exported fixed-threshold SAE reproduced the training sparsity almost exactly.

### Training split

```text
tokens                  = 3,101,336
mean L0                 = 255.8509
active fraction         = 0.0156159
zero-fire features      = 14
zero-fire fraction      = 0.0008545
MSE per dimension       = 0.00441769
explained variance      = 0.99866035
cosine similarity       = 0.99468990
```

### Validation split

```text
tokens                  = 165,010
mean L0                 = 255.9135
active fraction         = 0.0156197
zero-fire features      = 499
zero-fire fraction      = 0.0304565
MSE per dimension       = 0.00449457
explained variance      = 0.99863465
cosine similarity       = 0.99459663
```

### Full unique corpus

```text
tokens                  = 3,266,346
active features         = 16,372 / 16,384
zero-fire features      = 12
zero-fire fraction      = 0.0007324

frequency > 1e-5        = 15,398
frequency > 1e-4        = 13,918
frequency > 1e-3        = 12,566
```

The near-identical BatchTopK and fixed-threshold results indicate that the inference conversion preserved the trained representation.

---

## 11. Canonical inference artifact

The canonical local inference weight file is:

```text
sae_inference.safetensors
```

It contains:

```text
W_enc      (1024, 16384) float32
W_dec      (16384, 1024) float32
b_enc      (16384,)      float32
b_dec      (1024,)       float32
threshold  (16384,)      float32
```

The threshold vector contains the frozen scalar threshold for every feature.

The SHA-256 hash of the canonical inference weights is:

```text
72802a9c3a863f9e738880141118dbab394510d2addee986dabad0e38e79b634
```

All downstream SAE feature IDs refer to this exact dictionary.

The weight file does **not** need to be committed directly to GitHub if large binary artifacts are intentionally excluded, but an archival copy must be retained separately for reproducibility and for later causal work.

---

## 12. Canonical configuration

The frozen inference configuration is:

```text
architecture: JumpReLU
trained_as: BatchTopK
model: facebook/xglm-564M
hidden_state_index: 12
d_in: 1024
d_sae: 16384
training_k: 256
threshold: 0.11494007418131039
activation_scale: 0.02065550797801016
apply_decoder_bias_to_input: true
```

Downstream analyses must not modify these values.

---

## 13. Model-selection rationale

The final model-selection decision was based on the trade-off between reconstruction quality and usable dictionary coverage.

### 4 epochs

```text
EV                         ≈ 0.998634
MSE                        ≈ 0.004497
L0                         = 256
trainer dead fraction      ≈ 0.00519
full-corpus zero-fire      ≈ 0.0007
full-corpus active features = 16,372
```

### 8 epochs

```text
EV                         ≈ 0.998936
MSE                        ≈ 0.003504
L0                         = 256
trainer dead fraction      ≈ 0.05365
full-corpus zero-fire      ≈ 0.0378
full-corpus active features = 15,764
```

The 8-epoch run gained only approximately `0.000302` explained variance while losing hundreds of active features.

The 4-epoch model therefore provided the better basis for sparse feature discovery.

---

## 14. Important files

The compact canonical evidence consists of:

- `README.md`
- `sae_inference_config.json`
- `inference_evaluation.json`
- `corpus_feature_frequency.json`
- `training_config.yaml`
- `training_metrics.json`
- `training_trajectory.jsonl`
- `model_selection.json`
- `MANIFEST.json`

The exact weights are stored separately as:

- `sae_inference.safetensors`

The original training checkpoint is not required for downstream inference.

---

## 15. Relevant implementation files

The canonical SAE implementation is documented by:

- `scripts/common.py`
- `scripts/batchtopk.py`
- `scripts/train_batchtopk.py`
- `scripts/compare_batchtopk_corpus.py`
- `scripts/export_batchtopk_inference.py`

These files provide the training, evaluation, full-corpus comparison, and fixed-threshold export logic.

---

## 16. Reproducibility rules for downstream use

Any downstream experiment using this SAE must:

1. use `facebook/xglm-564M`;
2. extract hidden state index `12`;
3. use `add_special_tokens=False` when matching the original activation convention;
4. multiply residual activations by `0.02065550797801016`;
5. use the frozen SAE weights identified by the SHA-256 hash above;
6. use fixed-threshold JumpReLU inference with threshold `0.11494007418131039`;
7. avoid native BatchTopK inference;
8. not retrain or recalibrate the dictionary on the controlled feature dataset.

---

## 17. Status

The canonical SAE is **frozen**.

It is the fixed representational basis for all subsequent controlled linguistic feature analysis, feature inspection, ablation, steering, and behavioral evaluation.
