# Final Conclusions

## Low-Rank Linguistic Features in XGLM-564M

## 1. Summary

This study investigated whether low-level structural properties of language are represented in a multilingual language model in forms that are recoverable, sparsely isolatable, causally consequential, and behaviorally influential. Forty linguistic variables were evaluated using a controlled contrast-pair dataset containing 500 pairs per variable. Supervised probes were used to test linear recoverability from XGLM activations, while an independently trained sparse autoencoder (SAE) was used to identify unsupervised sparse directions associated with the same contrasts. Candidate SAE features were then inspected on naturalistic multilingual text and subjected to matched ablation, steering, and next-token behavioral interventions.

The results support a qualified positive conclusion. Structural linguistic information is widespread in XGLM-564M and can often be recovered both by supervised probes and by sparse decomposition. However, recoverability does not imply that the model contains a clean, one-to-one sparse feature for each linguistic abstraction. Many statistically strong SAE candidates were better described as narrower lexical, morphological, orthographic, tokenization, or language-specific correlates of the intended variable. Natural-text inspection therefore substantially weakened the semantic interpretation of several otherwise strong statistical candidates.

Causal intervention showed that some of these sparse directions nevertheless participate directly in model computation. Across all forty selected candidate features, 19 produced specific positive effects under ablation and 23 produced specific positive effects under steering. Fifteen variables satisfied a stronger mechanistic criterion requiring specific-positive effects in both ablation and steering together with a monotonic steering dose response. This 15-variable cohort was frozen before behavioral outcomes were inspected.

Behavioral evaluation was substantially more selective. Within the frozen cohort, nine of fifteen target interventions produced a positive next-token effect, ten outperformed matched SAE controls, and six produced a positive, control-specific effect surviving Benjamini-Hochberg correction across the frozen primary family. All six also showed monotonic behavioral dose response. The final full-chain variables were:

1. morphological segmentation type — SAE feature 15843;
2. animacy and humanness — SAE feature 6618;
3. inclusive/exclusive distinction — SAE feature 6062;
4. possession and alienability — SAE feature 15325;
5. aspect and event structure — SAE feature 6216;
6. mirativity, stance, and affect marking — SAE feature 1887.

The strongest general conclusion is therefore not that six abstract linguistic universals have been localized as monosemantic SAE features. Rather, **sparse directions associated with several controlled linguistic distinctions causally contribute to internal representation and, for a smaller subset, to local next-token behavior**. At the same time, several highly recoverable or human-interpretable features failed to produce the predicted behavioral effect. The study therefore separates four properties that should not be treated as equivalent: **representational recoverability, sparse isolation, semantic interpretability, and causal influence**.

---

## 2. Representational evidence is broad but not uniform

The supervised and sparse analyses provide convergent evidence that low-level linguistic form is represented throughout XGLM-564M.

The supervised comparison classified 26 of 40 variables as robust across all three available probe seeds under the core criterion requiring the relevant activation-recovery, directional-consistency, and split-generalization tests to pass in every seed. The remaining fourteen variables did not satisfy this cross-seed core standard, although failure of the aggregate criterion did not imply absence of signal at the SAE intervention layer. Several non-robust variables retained substantial layer-12 pair-difference probe performance.

The SAE analysis produced similarly broad but non-uniform evidence. Under the primary mean-pooled SAE evidence synthesis, the forty variables were distributed as follows:

| SAE evidence tier | Variables | Interpretation |
|---|---:|---|
| A | 11 | held-out direction preserved, construction-robust, and cross-variable selective |
| B1 | 2 | construction-robust but shared across variables |
| B2 | 16 | held-out direction preserved with incomplete construction robustness |
| C | 3 | overall held-out direction preserved but subgroup robustness weak |
| D | 8 | selected feature failed to preserve direction on the overall held-out test |

Using A, B1, and B2 as the stronger SAE group gives 29 of 40 variables. The supervised and SAE analyses converged on 23 variables, while six were SAE-strong without cross-seed robust probe evidence, three were probe-robust without strong SAE evidence, and eight were weak or unstable under both classifications.

The binary agreement between the supervised and SAE classifications was 0.775, with a Jaccard overlap of 0.719, Cohen's kappa of approximately 0.480, an odds ratio of approximately 10.22, and a two-sided Fisher exact p-value of approximately 0.007. These results indicate that the two methods detect substantially overlapping representational structure while remaining meaningfully distinct.

This distinction is theoretically important. Linear probing can recover information distributed across many activation dimensions even if no single sparse latent isolates it. Conversely, an SAE can identify a stable sparse direction whose information is not captured by the stricter cross-seed probe criterion. Neither method should therefore be treated as a complete definition of whether a linguistic property is represented.

---

## 3. SAE quality depended on dictionary coverage, not reconstruction alone

The SAE training stage also produced a methodological conclusion relevant to sparse interpretability.

Initial JumpReLU configurations achieved high reconstruction quality but suffered severe feature death. The selected replacement architecture, a 16× BatchTopK SAE with 16,384 features and training k=256, produced substantially healthier dictionary utilization. The selected four-epoch model achieved approximately 0.99863 validation explained variance while preserving 16,372 active features over the full unique training corpus. Only 12 of 16,384 features never activated over that corpus.

A longer eight-epoch run produced a small reconstruction improvement, reaching approximately 0.99894 validation explained variance, but substantially worsened feature coverage. Full-corpus active features fell to 15,764, and trainer-dead feature fraction increased markedly. The four-epoch model was therefore selected because the objective was feature discovery rather than reconstruction optimization alone.

This comparison demonstrates that **reconstruction quality is an insufficient model-selection criterion for interpretability-oriented SAEs**. A model can reconstruct activations slightly better while yielding a materially less useful sparse dictionary.

For downstream evaluation, the BatchTopK model was exported to an example-independent fixed-threshold inference representation. This avoided batch-dependent activation assignments during feature analysis and causal intervention. The resulting inference model retained approximately 0.99863 validation explained variance and approximately 0.99460 cosine similarity to the original residual activations.

---

## 4. Statistical SAE recovery substantially exceeded semantic interpretability

The largest change in interpretation occurred during natural-text feature inspection.

Statistical feature ranking initially suggested that many variables had highly selective and robust sparse correlates. Inspection of top natural activations showed that a large fraction of these candidates were narrower than the typological labels used to discover them. Some primarily tracked individual lexical items, suffixes, pronouns, complementizers, punctuation marks, tokenization patterns, language identity, or recurrent surface constructions.

Examples included features dominated by Turkish lexical or suffixal material, Spanish function words, German and Romance lexical classes, quotation punctuation, Japanese punctuation, and highly specific pronoun forms. Other candidates were clearly relevant to the target variable but reflected only one surface realization, such as feminine morphology, progressive `-ing`, first-person pronouns, or complementizer forms.

After inspecting all forty variables and considering alternative candidates where appropriate, the selected causal features received semantic grades of:

| Inspection grade | Count | Interpretation |
|---|---:|---|
| A | 7 | comparatively strong target alignment |
| B | 13 | plausible target-relevant feature with narrower or imperfect interpretation |
| C | 12 | partial, language-specific, lexical, or entangled correlate |
| D | 8 | weak, proxy-like, or uninterpretable candidate |

These grades were deliberately not used as hard exclusion criteria for causal testing. All forty variables remained in the initial intervention screen. This decision was empirically important: some low-grade candidates later produced strong causal evidence, while some high-grade candidates failed at the behavioral stage.

The inspection results therefore support a central methodological conclusion: **statistical association with a controlled contrast is not equivalent to semantic identification of the corresponding linguistic abstraction**. Controlled datasets are effective tools for discovering candidate model directions, but the human-readable meaning of those directions must be evaluated separately.

---

## 5. Ablation provides necessity-like evidence for a substantial subset

The first causal intervention tested whether removing the selected sparse contribution weakened the corresponding downstream linguistic distinction.

For each variable, the feature-high member of the pair was identified using training data. The selected feature's SAE decoder contribution was removed at XGLM hidden state 12, and the downstream effect was evaluated at the final hidden layer using a linguistic pair-difference direction derived from training data. Three other SAE features were matched using training-only activation magnitude, firing rate, and decoder norm and served as intervention controls.

Across forty variables:

- 31 produced positive target attenuation;
- 25 produced a larger effect than the matched controls;
- 19 were classified as specific positive after multiple-comparison correction.

The global representational disturbance was extremely small. The mean cosine similarity between the intervened and baseline final-layer representations was approximately 0.999955, with the lowest variable-level mean still approximately 0.998758. The effects are therefore difficult to explain as nonspecific destruction of the residual stream.

Ablation should be interpreted as **necessity-like evidence**, not as proof that an individual latent is uniquely necessary for a linguistic distinction. Information can be redundant or distributed across multiple features. The result instead establishes that, for a substantial subset, removing one selected sparse component specifically reduces a downstream representation associated with the target contrast more than matched interventions do.

---

## 6. Steering provides complementary sufficiency-like evidence

The second causal intervention tested whether adding the selected SAE decoder direction to the feature-low condition moved the downstream representation toward the feature-high condition.

Steering strength was determined from the training-set target-feature activation gap. Three doses were fixed: 0.5×, 1×, and 2×, with 1× designated as the primary inferential condition. Matched-control steering vectors were rescaled so that their residual-space perturbation norm matched that of the target direction.

Across forty variables:

- 31 produced positive target steering effects;
- 31 outperformed their matched controls;
- 23 were specific positive after FDR correction;
- 25 showed monotonic 0.5× → 1× → 2× dose response.

The intervention again remained highly local. Mean final-layer representation cosine similarity at the primary dose was approximately 0.999998, with a minimum variable-level mean of approximately 0.999985.

These results provide **sufficiency-like evidence** complementary to the ablation experiment. Adding a small amount of the selected sparse direction can predictably move the model's internal representation toward the associated linguistic condition. The combination of matched controls, dose response, and extremely small global representational displacement strengthens the causal interpretation beyond ordinary feature correlation.

---

## 7. A mechanistic cohort was frozen before behavioral evaluation

To separate internal causal evidence from output-level behavior, a primary mechanistic cohort was defined before behavioral outcomes were inspected.

A variable entered this cohort only if it satisfied all three criteria:

1. specific-positive ablation;
2. specific-positive steering;
3. monotonic 0.5× → 1× → 2× steering response.

Fifteen variables met these conditions:

- transitivity and valency;
- morphological segmentation type;
- agreement/indexing density;
- definiteness and specificity;
- gender/noun class;
- animacy and humanness;
- inclusive/exclusive distinction;
- pronoun richness and reduction;
- possession and alienability;
- aspect and event structure;
- modality and mood;
- mirativity, stance, and affect marking;
- quantifier scope and distributivity;
- quotation and reported-speech structure;
- social deixis, honorifics, and status encoding.

This freeze is important for interpreting the final behavioral statistics. The behavioral primary family was not selected from behavioral performance itself.

---

## 8. Behavioral effects are real but substantially more selective than internal causal effects

The behavioral evaluation tested whether SAE steering changed the model's actual next-token preference at the first controlled divergence between the feature-high and feature-low sentences.

For each pair, the next-token logit margin between the two alternative realizations was measured before and after intervention. When the pair diverged at the first token, the XGLM beginning-of-sequence token provided the common context. The primary 1× dose and the matched control features were inherited from the already frozen intervention design.

The initial diagnostic behavioral run used bfloat16 model computation and exhibited quantized logit differences. The same experiment was therefore rerun in float32 without changing the cohort, candidate features, controls, doses, metric, test split, or multiple-comparison procedure. The float32 evaluation is the canonical behavioral result.

Within the fifteen-variable frozen mechanistic cohort:

- 9 of 15 produced a positive target behavioral effect;
- 10 of 15 outperformed their matched controls;
- 6 of 15 produced a positive, control-specific effect surviving FDR correction across the primary family;
- 9 of 15 showed monotonic behavioral dose response.

The reduction from fifteen internally convergent candidates to six full-chain behavioral results is a central finding rather than a weakness of the experiment. Internal causal mediation was considerably more common than predictable output-level control.

The behavioral metric is deliberately narrow. It measures a local shift in the probability of the feature-high linguistic realization, not complete sentence rewriting or a high-level semantic decision. It therefore establishes that selected sparse interventions can influence the model's output distribution without implying that the corresponding feature acts as a general-purpose behavioral control knob.

---

## 9. Final full-chain causal features

Six variables satisfied the strongest complete criterion: specific-positive ablation, specific-positive steering, monotonic representation-level steering, positive control-specific behavioral influence surviving primary-family FDR correction, and monotonic behavioral dose response.

| ID | Variable | Feature | Inspection grade | Target-minus-control behavioral effect | Primary FDR q |
|---:|---|---:|:---:|---:|---:|
| 10 | morphological segmentation type | 15843 | B | +0.005927 | 0.002142 |
| 17 | animacy and humanness | 6618 | D | +0.006903 | 0.002142 |
| 19 | inclusive/exclusive distinction | 6062 | C | +0.000734 | 0.023322 |
| 21 | possession and alienability | 15325 | C | +0.019592 | 0.002142 |
| 23 | aspect and event structure | 6216 | B | +0.003034 | 0.009370 |
| 27 | mirativity, stance, and affect marking | 1887 | C | +0.005211 | 0.002142 |

### 9.1 Morphological segmentation type — feature 15843

Feature 15843 was interpreted as a Turkish suffixal morphology feature, including person- and possessive-like morphology. Its natural activations were relevant to morphological segmentation but narrower than an abstract, language-general representation of segmentation type. It nevertheless survived the complete causal pipeline.

The appropriate interpretation is therefore that a sparse direction associated with Turkish suffixal morphological structure contributes causally to the controlled morphological-segmentation contrast. The result does not establish a language-universal latent for agglutinative or synthetic morphology.

### 9.2 Animacy and humanness — feature 6618

Feature 6618 received the weakest inspection grade among the full-chain features. Natural activations primarily reflected artificial-intelligence-related lexical material rather than a clean general animacy/humanness distinction. Despite this, it produced robust ablation, steering, dose-response, and behavioral evidence.

This is a particularly important counterexample to the assumption that top-activation interpretability predicts causal importance. The feature is causally relevant to the controlled contrast even though its semantics remain entangled. It should therefore be described as an animacy-related lexical proxy with demonstrated causal participation, not as a clean animacy feature.

### 9.3 Inclusive/exclusive distinction — feature 6062

Feature 6062 was primarily interpreted as a first-person-pronoun feature, with particularly strong Chinese first-person-pronoun activation. It is relevant to person reference but does not isolate inclusive versus exclusive reference as an abstract distinction.

Its full-chain causal success suggests that the controlled inclusive/exclusive manipulation may recruit a lower-level person-reference representation. The result supports causal participation without demonstrating that the SAE independently encodes grammatical inclusivity.

### 9.4 Possession and alienability — feature 15325

Feature 15325 repeatedly activated in kinship and possessive contexts. It was therefore interpreted as a kinship/possession proxy rather than a clean representation of alienability.

This feature produced the largest target-minus-control behavioral effect in the final cohort. The combined evidence suggests that the controlled alienability manipulation is mediated partly through a more general possession/kinship representation. The typological distinction and the model feature are therefore related but should not be treated as semantically identical.

### 9.5 Aspect and event structure — feature 6216

Feature 6216 strongly tracked English progressive `-ing` morphology and was interpreted as a progressive-aspect feature. It is linguistically relevant but narrower than the full category of event structure.

This result is particularly informative because the variable was weak under the original combined probe/SAE classification. Its later manually selected feature nevertheless survived specific ablation, specific steering, monotonicity, and behavioral correction. The case demonstrates that an early statistical screen should not be treated as an absolute mechanistic exclusion criterion.

### 9.6 Mirativity, stance, and affect marking — feature 1887

Feature 1887 occurred in contexts containing surprise or mirative content but was strongly entangled with Japanese punctuation and language identity. It was therefore graded as a partial and language-specific correlate.

Its causal success shows that such entanglement does not prevent a sparse direction from participating in the controlled linguistic transformation. The result supports causal relevance to the mirativity contrast while leaving unresolved how much of the direction corresponds to mirativity itself versus the language-specific surface form used to express it.

---

## 10. Strong internal features can fail or reverse behaviorally

The full-chain successes are only part of the final result. Several variables exhibited strong internal causal effects but failed to influence next-token behavior in the predicted direction.

Gender/noun class is the clearest example. Feature 5205 was graded A and showed strong natural alignment with feminine morphology. It produced the largest specific ablation effect in the entire causal screen and also passed the steering criteria. Nevertheless, its final target-minus-control behavioral effect was approximately **−0.01328**, significant in the opposite direction within the primary family.

Transitivity/valency showed a similar dissociation. Feature 164 produced a large specific-positive ablation effect and specific-positive steering, but the final target-minus-control behavioral effect was approximately **−0.02491**.

Social deixis/honorifics and quotation/reported speech also passed the internal mechanistic freeze while failing to produce the predicted final behavioral result.

These cases demonstrate that **causal control of an internal linguistic representation does not guarantee predictable control of the model's immediate output distribution**.

Several mechanisms are compatible with this dissociation. The sparse feature may participate in a broader distributed representation; downstream layers may compensate for the intervention; the decoder direction may be entangled with additional properties; the output decision boundary may not align with the internal feature direction; or the first-divergence metric may capture only one local consequence of a broader linguistic state. The present experiments do not distinguish among these mechanisms.

The empirical conclusion, however, is unambiguous: representation-level causal evidence and behavioral causal evidence must be measured separately.

---

## 11. Interpretability and causal importance are distinct dimensions

The strongest methodological conclusion of the study is that no single measure captures "feature quality."

At least four distinct questions emerged:

1. **Recoverability:** can the linguistic distinction be decoded from model activations?
2. **Sparse isolation:** does an individual SAE latent reliably covary with the distinction?
3. **Semantic interpretability:** do natural activations support the intended human linguistic interpretation?
4. **Causal influence:** does intervening on the latent change downstream representation or output in the predicted direction?

The experiments produced substantial disagreement among these axes.

A feature could be statistically strong but semantically shallow. A feature could be poorly interpretable but causally powerful. A highly interpretable feature could strongly alter hidden representations yet fail behaviorally. A variable could be robustly probe-decodable while lacking a stable sparse correlate, or possess a sparse correlate while failing the stricter cross-seed probe criterion.

The final six full-chain features make this particularly clear: their inspection grades were B, D, C, C, B, and C. **None was grade A.** Conversely, several grade-A candidates did not survive the full behavioral stage.

This does not diminish the value of semantic inspection. Without inspection, the causal results would be easy to overstate. A causally successful feature whose natural activations are dominated by a lexical proxy should not be relabeled as a clean abstract linguistic feature. Instead, semantic inspection determines what the causal effect can legitimately be called, while intervention determines whether the feature matters computationally.

The appropriate methodology is therefore triangulation rather than reliance on any single indicator.

---

## 12. The evidence does not support a one-feature-per-variable model

The combined results argue against a simple dictionary in which each linguistic variable maps to one independent sparse latent.

Several variables were represented by features narrower than the target abstraction. Others showed evidence of shared features, distributed information, or substantial effects from matched control directions. The supervised probe and SAE analyses also disagreed for a meaningful minority of variables, indicating that linear recoverability and sparse localization are not identical.

The most defensible model is therefore:

> Linguistic distinctions can recruit one or more sparse, partially shared, and often surface-grounded representational directions, some of which make causal contributions to downstream computation.

This formulation accommodates the successful interventions without assuming that the SAE has recovered a human-designed linguistic ontology directly.

---

## 13. Claims supported by the evidence

The completed experiments support the following claims.

### 13.1 Low-level linguistic structure is widely recoverable

A majority of the forty controlled linguistic distinctions were robustly recoverable across supervised probe seeds, and a majority also received strong SAE evidence. Structural linguistic information is therefore broadly present in XGLM-564M activations.

### 13.2 Unsupervised sparse decomposition recovers overlapping linguistic structure

The SAE was trained independently of the controlled linguistic labels, yet its evidence substantially overlapped the supervised probe results. The linguistic signal is therefore not solely an artifact of fitting supervised probes to the contrast-pair dataset.

### 13.3 Sparse statistical evidence is not sufficient for semantic interpretation

Natural-text inspection repeatedly showed that statistically strong candidates corresponded to narrower lexical, morphological, orthographic, tokenization, or language-specific correlates.

### 13.4 Individual sparse directions can causally mediate internal linguistic distinctions

Matched ablation and steering produced corrected, target-specific effects for substantial subsets of variables while causing extremely small global representational disturbance.

### 13.5 Some sparse linguistic directions causally influence output probabilities

Six variables in a cohort frozen before behavioral evaluation produced positive, control-specific, FDR-corrected changes in next-token preference together with monotonic behavioral dose response.

### 13.6 Internal causal mediation is more common than behavioral control

Fifteen variables satisfied the representation-level mechanistic freeze, but only six satisfied the complete behavioral criterion. Internal causal involvement is therefore not equivalent to predictable output control.

### 13.7 Human interpretability is not a reliable proxy for causal efficacy

The final full-chain cohort contained no grade-A feature, while several grade-A candidates failed or reversed behaviorally. Natural interpretability and causal importance must therefore be evaluated separately.

### 13.8 Early screening failures should be treated as evidence weight, not absolute absence

The aspect/event-structure result demonstrates that a variable weak under the initial combined evidence framework can still yield a later causally validated feature. Strict early filtering can therefore discard scientifically relevant representations.

---

## 14. Claims not supported by the evidence

The experiments do **not** establish that XGLM contains forty clean, discrete, language-universal linguistic features.

They do not establish that the six full-chain SAE features are semantically equivalent to the typological variables used to discover them. Several are explicitly narrower proxies.

They do not establish strict necessity or sufficiency of individual latents. Ablation and steering provide necessity-like and sufficiency-like evidence within the tested intervention framework, but representations may be distributed or redundant.

They do not establish that SAEs are superior to supervised probes for linguistic representation. The two methods answer different questions and exhibit complementary strengths and failures.

They do not establish that the identified directions control complete linguistic generation. The final behavioral metric measures local next-token preference at the first controlled divergence.

They do not establish that low-level linguistic structure already causes alignment-relevant behavioral changes such as shifts in truthfulness, deference, bias, refusal, responsibility attribution, or epistemic calibration. Those are downstream hypotheses requiring separate experiments.

Finally, the results are not sufficient to claim that the model internally organizes language according to the same discrete categories used in linguistic theory. The controlled variables are experimental interventions and discovery labels, not guaranteed descriptions of the model's own ontology.

---

## 15. Limitations

### 15.1 Single model and intervention site

The causal experiments were conducted on `facebook/xglm-564M`, with the SAE operating at hidden-state index 12. Replication across model families, scales, layers, and independently trained SAEs is necessary before treating the findings as general properties of multilingual language models.

### 15.2 Synthetic controlled evaluation data

The contrast-pair dataset was synthetically constructed to isolate linguistic variables. This provides strong control but creates a risk that variables are learned or recovered through recurring surface cues. Held-out marker families, held-out lexical domains, natural-text inspection, and matched causal controls reduce this concern but do not eliminate it.

### 15.3 Limited cross-linguistic instantiation per variable

Many non-English variables were instantiated in a selected language rather than independently across multiple unrelated languages. A causal feature associated with Turkish morphology, Korean honorifics, Chinese pronouns, or Japanese punctuation should therefore not be assumed to represent the same structural property universally.

### 15.4 SAE corpus and dictionary dependence

The SAE was trained on a separate multilingual corpus without controlled feature labels, which is an important safeguard. However, the causal analysis uses one trained dictionary. Independent SAE retraining could split, merge, rotate, or otherwise reorganize features even if the same linguistic information remains present.

### 15.5 Candidate selection involved post-hoc scientific judgment

Natural-text inspection and alternative-candidate selection necessarily involved researcher judgment. The behavioral cohort was frozen before behavioral evaluation, but the full feature-discovery and causal-candidate process was not a preregistered procedure. Causal results should therefore be understood as validation of selected mechanistic candidates rather than as a fully confirmatory test of a predetermined feature map.

### 15.6 SAE feature interventions are not orthogonal interventions

SAE decoder directions are not guaranteed to be orthogonal or causally independent. Adding or subtracting one direction may affect computations associated with correlated features. Matched control directions and the very high final-representation cosines reduce the likelihood of generic disruption but do not provide complete isolation.

### 15.7 Behavioral evaluation is local

The first-divergence next-token test gives a clean, model-native output metric but measures only a local linguistic preference. It does not establish that steering would transform an entire generated sentence or produce a stable high-level behavioral change.

### 15.8 Behavioral sample size

The held-out behavioral evaluation used fifty test pairs per variable. Bootstrap inference and FDR correction address uncertainty, but larger evaluation sets would improve power and effect-size precision, especially for the smallest full-chain effects.

### 15.9 Numerical precision in behavioral inference

A diagnostic bfloat16 behavioral run produced quantized logit changes. The experiment was therefore repeated in float32 with the hypothesis family and intervention specification unchanged. The float32 run should be treated as canonical. This episode illustrates that small output-logit interventions require explicit numerical validation.

---

## 16. Implications for mechanistic interpretability

Several general methodological lessons follow from the study.

First, **decodability is evidence of information presence, not mechanistic localization**. A high-performing probe does not establish that the information resides in a single feature or that the decoded direction is used causally.

Second, **SAE feature ranking is not semantic labeling**. Controlled contrasts can discover candidate latents effectively, but statistical selectivity does not define the full meaning of a latent.

Third, **natural-text inspection is necessary but not sufficient**. Inspection protects against semantic overclaiming, yet poor top-activation interpretability does not imply causal irrelevance.

Fourth, **matched intervention controls are essential**. Some target interventions produced positive effects no larger than matched non-target SAE directions. Without these controls, generic perturbation effects would be mistaken for linguistic causality.

Fifth, **dose response materially strengthens causal evidence**. Monotonic change across fixed intervention strengths is more informative than a single arbitrary steering coefficient.

Sixth, **internal and behavioral causality should be tested separately**. The transition from fifteen internally convergent variables to six behaviorally specific variables demonstrates that a hidden representation can be causally active without functioning as a direct output-control direction.

A robust linguistic mechanistic-interpretability pipeline should therefore combine:

> controlled contrast construction → supervised recovery → unsupervised sparse recovery → natural-text inspection → matched ablation → matched steering → pre-behavior evidence freeze → output-level causal evaluation.

The value of this sequence is not only that it identifies positive results. It also reveals exactly where an apparently strong feature interpretation fails.

---

## 17. Implications for structural-language and constitutional-language research

The broader motivation for studying low-level linguistic structure is the possibility that formal properties of language influence model computation even when higher-level propositional content is held approximately constant.

The present evidence establishes an important prerequisite for that research direction. Controlled changes in morphology, person reference, possession, aspect, stance-related marking, and other structural properties correspond to internal directions that are not merely decodable but experimentally manipulable. For six variables, intervention on those directions also changes the model's local output probability in the predicted direction.

This makes it plausible that structural linguistic signals could influence higher-level model behavior through identifiable internal mechanisms. It does not yet establish that they affect alignment-relevant outcomes.

A subsequent research stage should therefore test whether interventions on these representations change **semantic decisions under controlled propositional content**, rather than only the linguistic realization itself. Candidate outcomes include confidence and evidence weighting for evidential or epistemic features, deference and authority weighting for honorific or social-deixis features, responsibility attribution for voice and agent-prominence features, or framing sensitivity for discourse and perspective features.

The present study supplies the mechanistic basis for such experiments while leaving the high-level behavioral hypothesis open.

---

## 18. Recommended interpretation of the six final variables

The six full-chain results are best described as **causally validated sparse correlates of controlled linguistic distinctions**.

This terminology preserves both sides of the evidence. The directions are not merely correlated: they survived matched causal intervention and behavioral evaluation. At the same time, their natural-text semantics are often narrower than the linguistic variable names used for discovery.

For B-grade candidates such as Turkish suffixal morphology and progressive aspect morphology, relatively specific linguistic interpretation is justified as long as its language and construction scope is stated explicitly. For C- and D-grade candidates, the proxy interpretation established during feature inspection should be retained even when the causal evidence is strong.

A causal result should therefore strengthen the claim that the feature **matters**, not automatically broaden the claim about what the feature **means**.

---

## 19. Overall claim

The strongest conclusion supported by the complete evidence is:

> Across forty controlled structural linguistic contrasts in XGLM-564M, linguistic information was broadly recoverable from both supervised activations and an independently trained sparse autoencoder, but statistical sparse-feature recovery frequently reflected narrower lexical, morphological, language-specific, orthographic, or tokenization correlates rather than clean abstract linguistic features. Causal intervention nevertheless identified a subset of sparse directions that specifically mediated downstream representations. Fifteen variables showed convergent ablation and steering evidence with monotonic dose response and were frozen before behavioral evaluation. Six of these subsequently produced FDR-corrected, control-specific changes in next-token linguistic preference together with monotonic behavioral dose response. These results show that sparse representations can capture causally relevant linguistic structure while demonstrating that recoverability, sparse isolation, human interpretability, internal causal mediation, and behavioral influence are distinct properties.

---

## 20. Final conclusion

Low-level linguistic structure is mechanistically accessible in XGLM-564M, but it is not organized as a simple dictionary of clean human linguistic concepts.

Many controlled linguistic distinctions can be recovered from model activations, and an unsupervised sparse decomposition recovers substantially overlapping information. Yet the strongest statistical SAE candidates often correspond to the surface machinery through which a distinction is expressed rather than to the abstract typological distinction itself. Sparse representations therefore appear to be partly structural, partly distributed, and frequently grounded in language-specific morphology, lexical material, punctuation, or other surface cues.

Causal intervention establishes that this imperfection does not make the representations epiphenomenal. Removing selected sparse components can specifically weaken downstream linguistic distinctions, and adding the corresponding decoder directions can move internal states toward the associated linguistic condition. For a smaller but statistically robust subset, these interventions also change the model's next-token preference in the predicted direction.

At the same time, several of the strongest internal features fail or reverse at the behavioral stage. This dissociation shows that a causally active hidden representation need not constitute a direct behavioral control axis. Representation and output are connected through additional computation that cannot be inferred from feature association or internal intervention alone.

The completed evidence therefore supports a layered account of linguistic representation in language models. **Information can be present without being sparsely isolated; a sparse feature can be isolated without being cleanly interpretable; an interpretable or statistically strong feature can participate causally without controlling output; and a subset of sparse directions can survive all of these tests and exert measurable behavioral influence.**

The main scientific contribution is consequently not a catalog of six linguistic neurons. It is evidence that structural linguistic information can be traced across progressively stronger levels of analysis—from recoverability, through sparse representation and causal mediation, to observable output—while showing where those levels diverge.

This distinction provides a stronger foundation for future work on how low-level linguistic form influences model reasoning and behavior. The relevant question is no longer only whether structural language is represented internally. The evidence indicates that it is, and that some of those representations matter causally. The next question is which downstream computations and decisions those representations influence beyond linguistic form itself.

---

## Repository evidence used for this synthesis

The conclusions above are grounded in the final repository artifacts, particularly:

- `SAE/canonical_sae/sae_canonical/inference_evaluation.json`
- `SAE/canonical_sae/sae_canonical/model_selection.json`
- `SAE/post_canonical/post_canonical/evidence/sae/sae_variable_evidence.csv`
- `SAE/post_canonical/post_canonical/evidence/sae/sae_variable_evidence_summary.json`
- `SAE/post_canonical/post_canonical/evidence/probe/probe_sae_comparison.csv`
- `SAE/post_canonical/post_canonical/evidence/probe/probe_sae_comparison_summary.json`
- `SAE/post_canonical/post_canonical/evidence/probe/probe_sae_agreement_summary.json`
- `SAE/feature_inspection/all_variables/causal_candidate_ranking.csv`
- `SAE/feature_inspection/all_variables/ALL_VARIABLE_FEATURE_REVIEW.md`
- `causal_steps/causal_interventions/ablation_screen/ablation_variable_summary.csv`
- `causal_steps/causal_interventions/steering_screen/steering_variable_summary.csv`
- `causal_steps/causal_interventions/mechanistic_convergence/PREBEHAVIOR_PRIMARY_COHORT.csv`
- `causal_steps/causal_interventions/mechanistic_convergence/mechanistic_convergence.csv`
- `causal_steps/causal_interventions/behavioral_evaluation/behavioral_variable_summary.csv`
- `causal_steps/causal_interventions/final_summary/final_causal_evidence.csv`
- `causal_steps/causal_interventions/final_summary/FULL_CHAIN_PRIMARY_RESULTS.csv`
- `causal_steps/causal_interventions/final_summary/final_causal_evidence.json`
