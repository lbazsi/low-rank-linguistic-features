# Final Conclusions

## Low-Rank Linguistic Features: Representation, Sparse Recovery, Causal Mediation, and Behavioral Influence in XGLM-564M

## 1. Overall conclusion

The experiments provide evidence that a substantial range of low-level linguistic distinctions are represented inside XGLM-564M in recoverable and, for a smaller subset, causally consequential forms. However, the results do not support a simple picture in which each linguistic variable corresponds to a clean, monosemantic sparse feature. Instead, the evidence separates four properties that are often implicitly treated as equivalent in mechanistic interpretability: **recoverability, sparse isolation, human interpretability, and causal influence**.

These properties overlap, but they are not interchangeable.

Supervised activation probes showed that many controlled structural distinctions could be recovered robustly from model activations and generalized beyond the exact marker families and lexical domains used for training. A separately trained sparse autoencoder also exposed features associated with nearly all of the controlled contrasts at a permissive statistical level, with substantially stronger held-out evidence for a majority of variables. The supervised and sparse analyses agreed considerably more often than expected from a completely unrelated pair of methods.

Yet natural-text inspection changed the interpretation of these results. Many statistically strong SAE features were not clean representations of the intended typological variable. They instead tracked narrower morphological markers, lexical classes, punctuation, language identity, tokenization patterns, or surface realizations that correlated with the controlled contrast. This distinction persisted even among the statistically strongest candidates.

Causal intervention then revealed an additional layer. Nineteen of forty selected SAE features produced specific downstream effects under ablation, twenty-three produced specific effects under steering, and fifteen variables satisfied a pre-behavior criterion requiring specific effects in both directions together with a monotonic steering response. These fifteen were frozen before behavioral evaluation.

Of those fifteen, **six variables ultimately showed the complete causal chain**: a positive and control-specific representational effect under ablation, a positive and control-specific effect under steering, monotonic representation-level steering, and a positive, FDR-corrected effect on next-token preference with a monotonic behavioral dose response. These variables were morphological segmentation type, animacy/humanness, inclusive/exclusive distinction, possession/alienability, aspect/event structure, and mirativity/stance/affect marking.

The central conclusion is therefore not that six abstract linguistic universals have been located inside XGLM. The stronger and more defensible conclusion is that **sparse directions associated with several controlled linguistic distinctions causally participate in both internal representation and local token prediction**, while many other recoverable distinctions either remain distributed, are represented through entangled surface correlates, or fail to propagate into the tested behavioral output.

The results consequently support a layered view of linguistic representation: structural information is widespread, sparse representations can isolate causally relevant components of that information, but neither statistical association nor apparent interpretability alone determines whether a feature actually participates in model computation.

---

## 2. Evidence across the full experimental pipeline

The project began with forty linguistic variables represented by 500 controlled contrast pairs each, yielding 20,000 basis/changed pairs and 40,000 sentences. The controlled dataset was kept separate from the SAE training corpus. Train, validation, and test partitions additionally encoded held-out marker families and lexical domains, making later evaluation stricter than simple random example separation.

The major empirical results can be summarized as follows.

| Stage | Main result | Interpretation |
|---|---:|---|
| Controlled feature dataset | 40 variables × 500 pairs | Broad typological test bed with explicit held-out constructions |
| Raw activation probes | 27/40 passed activation recoverability in each probe seed | Many linguistic contrasts are linearly recoverable |
| Directional probe test | 33/40 passed directional consistency | Pair transformations frequently form stable activation directions |
| Split generalization | 26/40 passed in each seed | Many signals survive marker/domain holdout |
| Learned-direction viability | Same 12 variables passed across seeds 1, 2, and 42 | A smaller subset supports especially strong supervised directional evidence |
| Probe core evidence | 26/40 robust across all three seeds | Broad cross-seed representational evidence |
| Canonical SAE | 16,384 features; 0.99863 validation explained variance | High-fidelity sparse decomposition with broad feature coverage |
| SAE first-stage recovery | Every variable had at least one corrected-null candidate under the broad candidate search | Sparse activation differences are extremely widespread |
| Primary mean-pooled SAE tiers | A: 11, B1: 2, B2: 16, C: 3, D: 8 | 29/40 had strong A/B sparse evidence; 32/40 preserved overall test direction through A/B/C |
| Probe–SAE comparison | 23 convergent, 6 SAE-only, 3 probe-only, 8 weak in both | Supervised and sparse evidence overlap strongly but imperfectly |
| Manual causal-candidate inspection | A: 7, B: 13, C: 12, D: 8 | Statistical strength substantially exceeded clean semantic interpretability |
| Ablation | 31/40 positive; 25/40 beat controls; 19/40 specific after correction | A sizeable subset is causally involved in downstream representations |
| Steering | 31/40 positive; 31/40 beat controls; 23/40 specific; 25/40 monotonic | Adding SAE directions can predictably alter representations |
| Pre-behavior mechanistic cohort | 15/40 | Frozen before behavioral outcomes were inspected |
| Behavioral evaluation | 9/15 positive; 10/15 beat controls; 6/15 FDR-specific | Internal causal effects translate to token-level behavior for a selective subset |
| Final full-chain cohort | 6/15 primary candidates | Strongest evidence for causal linguistic influence |

This funnel is itself one of the main results. The number of variables decreases as the evidential standard changes from **information being recoverable** to **information being isolated in a sparse direction**, then to **that direction causally mediating downstream computation**, and finally to **that intervention altering actual output probabilities in the predicted direction**.

That decrease should not be interpreted as failure of the earlier stages. Rather, it demonstrates that these stages measure genuinely different properties.

---

## 3. Raw activations contain widespread structural linguistic information

The supervised probing stage provides the clearest evidence that structural linguistic information is broadly present in XGLM activations.

Across seeds 1, 2, and 42, the evidence profile was remarkably stable. Each seed produced 27 variables passing the activation-recoverability screen, 33 passing directional consistency, and 26 passing split generalization. The same twelve variables passed the most conservative learned-direction viability criterion in all three seeds.

Those twelve included morphosyntactic alignment, voice and agent prominence, causativity and valency change, morphological segmentation type, agreement/indexing density, definiteness/specificity, gender/noun class, inclusive/exclusive distinction, pronoun richness/reduction, mirativity/stance/affect marking, quantifier scope/distributivity, and quotation/reported-speech structure.

Their average sentence-level activation AUROC was approximately 0.858, while the learned pair-difference directions achieved a mean AUROC of approximately 0.956. Thus, at least for this restricted subset, the evidence went beyond ordinary classifiability: the controlled transformation repeatedly corresponded to a stable representational direction.

At the same time, the probe results already warned against treating decodability as an abstract linguistic representation. Text baselines frequently performed well because the intended linguistic changes were often surface-visible. This is expected for features realized by case morphology, pronouns, complementizers, quotation marks, verbal inflections, or other explicit linguistic material. A successful activation probe therefore establishes that the information is present in the representation, but not that the representation has abstracted away from the surface form that expresses it.

The updated probing framework was important precisely because it separated activation recovery, surface visibility, directional consistency, split generalization, and learned-direction viability. A single high AUROC was not treated as sufficient evidence for a mechanistic claim.

One further lesson emerges retrospectively from the later causal results: the most conservative supervised probe criteria were useful evidence filters but were **not exhaustive detectors of causal relevance**. Some variables that did not belong to the original twelve learned-direction candidates later produced strong sparse causal results. Probe failure or incompleteness therefore cannot be equated with absence of linguistic information.

---

## 4. The canonical SAE provided a healthy sparse basis, but architecture choice mattered

The sparse-autoencoder training process produced a methodological result of its own.

Initial JumpReLU experiments reconstructed the residual stream well but suffered catastrophic dictionary collapse. The original 16× JumpReLU model reached approximately 0.992 explained variance while leaving around 95% of its 16,384 features dead. Altering sparsity penalties, threshold parameterization, dead-feature objectives, and dictionary width improved the situation but did not solve progressive collapse.

BatchTopK produced a dramatically healthier dictionary. The selected four-epoch model used a 16× expansion from 1,024 residual dimensions to 16,384 SAE features with training \(k=256\). It achieved approximately 0.99863 validation explained variance, a cosine similarity of 0.99459, and only 85 trainer-dead features. On the full unique training corpus, 16,372 of 16,384 features activated at least once.

A longer eight-epoch model marginally improved reconstruction to approximately 0.99894 explained variance, but substantially worsened dictionary coverage: hundreds of additional features became dead or unused. The four-epoch model was therefore correctly selected because the scientific objective was feature discovery rather than optimizing reconstruction error alone.

This result illustrates an important principle for sparse interpretability work: **reconstruction quality and useful dictionary quality are not synonymous**. A slightly better autoencoder can be a worse interpretability instrument if it concentrates reconstruction into fewer active features.

Native BatchTopK inference introduced a separate problem because an example's activation pattern depends on the other examples sharing its inference batch. The trained model was therefore exported to a fixed-threshold JumpReLU-style representation using a threshold calibrated exclusively from training activations. This gave each controlled sentence an independent representation and reproduced the training sparsity closely.

The resulting SAE was thus sufficiently stable and well-covered to serve as a fixed representational basis for the later linguistic experiments.

---

## 5. Sparse recoverability was broad, but sparse recoverability did not imply a clean linguistic feature

The post-canonical SAE analysis initially appeared extremely strong.

Across the forty variables and 16,384 SAE features, paired basis/changed activation effects were evaluated under a sign-flip permutation framework. Because feature selection searched a large dictionary, the null distribution used the maximum absolute effect over the full SAE dictionary on each permutation, controlling the within-variable feature search.

Under the broad first-stage procedure, every variable possessed at least one top candidate that survived corrected training significance and preserved its direction on held-out data in at least one representation. This establishes a broad result: **controlled linguistic transformations leave sparse signatures throughout the SAE dictionary**.

The more informative mean-pooled evidence synthesis was less uniform. Eleven variables received Tier A, two Tier B1, sixteen Tier B2, three Tier C, and eight Tier D. Thus, 29 of forty variables fell into the stronger A/B family, while 32 preserved the overall held-out test direction when Tier C was also included.

Mean pooling was preferable to final-token activation because final-token features showed much greater reuse across variables and were often dominated by punctuation or sentence-final regularities. This is another important negative finding: localization to a convenient token position can increase apparent sparsity while reducing structural specificity.

The supervised and sparse approaches nevertheless agreed substantially. Twenty-three variables were simultaneously robust under the supervised probe criteria and strong under the SAE evidence tiers. Six had strong sparse evidence without robust probe evidence, three had robust probes but weak or unstable SAE evidence, and eight were weak or unstable under both systems. Binary agreement was 77.5%, with a Jaccard overlap of approximately 0.719 and Cohen's \(\kappa\) of approximately 0.48. The estimated odds ratio between robust probe evidence and strong SAE evidence was approximately 10.2.

The methods therefore appear to be detecting overlapping representational structure, but not identical structure. A probe can recover information distributed across many dimensions even if no individual SAE latent cleanly isolates it. Conversely, an SAE feature can generalize even when the stricter cross-seed probe pipeline does not classify the variable as robust.

This distinction became crucial in later stages.

---

## 6. Natural-text feature inspection fundamentally changed the interpretation of the SAE results

Feature inspection was the point at which the project moved from a feature-recovery study to a more defensible mechanistic study.

Several candidates that appeared exceptionally strong statistically were clearly dominated by shallow correlates in natural text. Examples included a morphological-segmentation candidate dominated by the Turkish lexical item *İstanbul*, a cumulative-exponence candidate dominated by Spanish *para*, a possession candidate dominated by equivalents of *last*, a speech-act candidate dominated by *wait/waiting*, and a quotation candidate that behaved primarily as a quotation-mark detector.

Other candidates were linguistically relevant but much narrower than the intended variable. A gender/noun-class feature strongly tracked feminine morphology in Arabic and Urdu. A pronoun feature tracked explicit third-person pronouns across languages rather than abstract pronoun-system richness. A complementizer feature tracked forms such as *that*, *qu-* and *que* rather than embedding as an abstract relation.

The initial high SAE tiers therefore overstated semantic interpretability. After inspection of all forty variables and alternative candidates where useful, the primary causal candidates were graded as seven A, thirteen B, twelve C, and eight D.

These grades were not statistical tiers. They represented the quality of the linguistic interpretation:

**A** indicated comparatively strong target alignment; **B** indicated a plausible and relevant feature with a narrower or imperfect interpretation; **C** indicated a partial, language-specific, lexical, or otherwise entangled correlate that remained scientifically interesting; and **D** indicated weak, uninterpretable, or strongly proxy-like behavior.

Crucially, the weaker grades were not automatically excluded from causal intervention. This decision was vindicated by the later results.

The ultimate full-chain causal cohort contained **no grade-A feature**. Its grades were B, D, C, C, B, and C.

This is one of the most consequential findings of the project. Human interpretability from top activations was not a reliable proxy for causal importance.

That does not mean interpretation is unnecessary. Quite the opposite: the grading prevents the causal results from being mislabeled. A grade-D animacy feature that later has a strong causal effect should not suddenly be renamed a clean "animacy neuron." Its causal success demonstrates that the sparse direction participates in the controlled animacy contrast; it does not erase the evidence that the feature's natural activation is dominated by a narrower lexical correlate.

The correct lesson is therefore that **interpretability and causal relevance are orthogonal enough to require separate measurement**.

---

## 7. Causal ablation established necessity-like evidence for a substantial subset

Step 7 tested all forty selected candidate features rather than retaining only the cleanest inspection grades.

For each variable, the condition with higher target-feature activation was determined from training data. The corresponding SAE decoder contribution was then removed from the XGLM residual stream at hidden state 12. The outcome was measured downstream at the final hidden layer using a linguistic pair-difference direction derived from training data.

Three other SAE features were used as controls for each target. These were matched using training-only activation magnitude, firing rate, and decoder norm.

The result was broad but selective:

31 of 40 target ablations moved the downstream distinction in the predicted direction; 25 produced greater attenuation than their matched controls; and 19 were classified as specific positive effects after correction.

Importantly, these interventions were highly local in global representation space. The mean cosine similarity between the intervened and original final representation was approximately **0.999955**. The causal results therefore cannot easily be explained as simple destruction of the model's hidden state.

The largest effect occurred for gender/noun class, whose selected feature 5205 produced a target-minus-control attenuation of approximately 0.228. Animacy/humanness, transitivity/valency, possession/alienability, and agreement/indexing density also produced comparatively large effects.

The ablation stage provides **necessity-like**, rather than absolute necessity, evidence. Removing a single SAE feature cannot establish that the represented linguistic property depends exclusively on that feature; information may be distributed or redundantly encoded. What it does establish is that, for a substantial subset, removing the selected sparse component reduces the downstream representational distinction more than matched interventions do.

---

## 8. Steering established complementary sufficiency-like evidence

Step 8 tested the complementary causal direction.

The feature-low member of each pair received the candidate feature's SAE decoder direction. Steering strength was defined from the training-set difference in target-feature activation rather than selected from held-out outcomes. Three doses were fixed in advance: 0.5×, 1×, and 2× the training activation gap, with 1× designated as the primary inferential condition. Control directions were adjusted to match the residual-space perturbation norm of the target intervention.

Again, all forty variables were retained.

Thirty-one target interventions moved the representation in the predicted direction, all thirty-one of those also outperformed the average matched control effect, twenty-three were specific positive after FDR correction, and twenty-five showed a monotonic 0.5×→1×→2× dose response.

The intervention remained extremely local: mean final-representation cosine similarity at the primary dose was approximately **0.999998**.

This combination—directionally predictable change, matched controls, dose dependence, and extremely small global representational displacement—is considerably stronger evidence than ordinary activation correlation.

A pre-behavior primary cohort was then frozen using only Steps 7 and 8. A variable entered this cohort if it showed specific-positive ablation, specific-positive steering, and monotonic steering across the three doses. Fifteen variables satisfied these criteria:

transitivity/valency; morphological segmentation type; agreement/indexing density; definiteness/specificity; gender/noun class; animacy/humanness; inclusive/exclusive distinction; pronoun richness/reduction; possession/alienability; aspect/event structure; modality/mood; mirativity/stance/affect marking; quantifier scope/distributivity; quotation/reported speech; and social deixis/honorifics.

The behavioral outcomes had not been consulted when this cohort was frozen.

---

## 9. Behavioral influence was real but substantially more selective than internal causal influence

The behavioral test asked a stricter question than the representational interventions.

For each controlled pair, the first token position at which the feature-high and feature-low realizations diverged was identified. XGLM's next-token logit margin between those alternatives was then measured before and after SAE steering. When the sentences diverged immediately, the model's BOS token served as the common context.

The outcome therefore tested whether manipulating the SAE feature changed the model's **actual next-token preference toward the feature-high linguistic realization**.

The original diagnostic evaluation in bfloat16 exhibited quantized logit differences. The behavioral specification was therefore rerun in float32 without changing the primary cohort, features, controls, doses, test split, metric, or multiple-comparison procedure. The FP32 run is the canonical behavioral result.

Within the fifteen-variable cohort frozen before behavior, nine target interventions produced a positive mean behavioral effect, ten outperformed matched controls, and six produced a positive, control-specific effect surviving Benjamini-Hochberg correction across the fifteen primary variables. Nine also displayed monotonic behavioral dose response.

Thus, **40% of the frozen mechanistic cohort survived the full behavioral standard**.

This is a meaningful positive result, but the selectivity is just as important as the success rate. Internal causal mediation was considerably more common than demonstrable next-token behavioral control.

The intervention can therefore manipulate some internal linguistic distinctions without necessarily altering the immediate output probability in the same direction.

---

## 10. The six full-chain causal results

The final full-chain variables were:

| Variable | SAE feature | Inspection grade | Natural-text interpretation |
|---|---:|---:|---|
| Morphological segmentation type | 15843 | B | Turkish suffixal/person/possessive morphology |
| Animacy and humanness | 6618 | D | Lexical proxy with strong artificial-intelligence/human-reference associations |
| Inclusive/exclusive distinction | 6062 | C | First-person-pronoun proxy rather than clean inclusivity |
| Possession and alienability | 15325 | C | Kinship/possession proxy rather than alienability itself |
| Aspect and event structure | 6216 | B | Strong English progressive `-ing` / aspectual morphology |
| Mirativity, stance and affect marking | 1887 | C | Mirative contexts entangled with Japanese punctuation/language identity |

### Morphological segmentation type

Feature 15843 is one of the clearest examples of why alternative-feature inspection mattered. The original statistically strong feature for this variable was dominated by a lexical/tokenization pattern around *İstanbul*. Returning to alternative candidates identified feature 15843, which tracks Turkish suffixal morphology, including person- and possessive-like material.

The feature remains narrower than an abstract representation of morphological segmentation type. Nevertheless, it survived ablation, steering, both dose-response stages, matched controls, and behavioral FDR correction. Its final behavioral target-minus-control effect was approximately **+0.00593**.

The defensible conclusion is that a sparse direction associated with Turkish suffixal morphological structure contributes causally to the controlled segmentation contrast. The result does not establish a language-universal latent for agglutinative morphology.

### Animacy and humanness

Feature 6618 is methodologically perhaps the most interesting success. Its inspection grade was D because top natural activations did not cleanly describe general animacy or humanness; they were heavily associated with artificial-intelligence-related lexical material.

Despite this poor semantic interpretation, the feature produced strong ablation, steering, monotonic response, and behavioral evidence. Its final target-minus-control behavioral effect was approximately **+0.00690**, with primary-family FDR \(q \approx 0.00214\).

This result demonstrates that a feature can be causally useful without being cleanly interpretable from top activations. It does **not** justify relabeling feature 6618 as an abstract animacy representation. Instead, it shows that the controlled animacy contrast depends on a sparse direction whose exact semantics remain entangled.

### Inclusive/exclusive distinction

Feature 6062 was graded C because it behaved most clearly as a first-person-pronoun feature, especially in Chinese, rather than as a direct representation of inclusive versus exclusive reference.

Its final behavioral effect was small but consistent: approximately **+0.00073** relative to matched controls, with FDR \(q \approx 0.0233\). It also showed monotonic dose response and passed the earlier causal stages.

This result is compatible with inclusive/exclusive distinctions being mediated through a lower-level person-reference representation rather than a dedicated inclusivity feature. It therefore supports causal relevance of the representation without establishing that the SAE has disentangled the higher-level typological distinction.

### Possession and alienability

Feature 15325 activated strongly in kinship and possessive contexts. It was therefore considered possession-related but insufficiently specific to demonstrate alienability as such.

Nevertheless, it produced the largest final behavioral effect among the six full-chain variables: the target-minus-control effect was approximately **+0.01959**, with FDR \(q \approx 0.00214\).

The natural interpretation and causal result together suggest that the controlled alienability manipulation may recruit a more general possession/kinship representation. This is a useful example of how a typological variable can be behaviorally mediated by a lower-level correlate rather than by an explicitly matching sparse abstraction.

### Aspect and event structure

Feature 6216 strongly tracks progressive `-ing` morphology and is relatively straightforwardly aspect-related, although narrower than the full event-structure variable.

This variable is particularly informative because it had weak earlier evidence: the original SAE evidence tier was D, its held-out candidate direction was unstable, and the strict probe comparison classified the variable as weak under both the probe and initial SAE systems. Yet the later manually selected feature produced specific ablation, steering, monotonicity, and an FDR-corrected behavioral effect of approximately **+0.00303** relative to controls.

Had the causal stage excluded all variables that failed an earlier evidence threshold, this result would have been missed.

Aspect/event structure therefore provides direct evidence against treating early statistical screening as an absolute mechanistic gate.

### Mirativity, stance and affect marking

Feature 1887 consistently activated in several mirative or surprise-related contexts but was heavily entangled with Japanese punctuation and language identity. It was accordingly graded C.

Despite that entanglement, it produced strong causal evidence throughout the intervention pipeline and a final target-minus-control behavioral effect of approximately **+0.00521**, with FDR \(q \approx 0.00214\).

This again demonstrates the distinction between causal participation and clean abstraction. The result supports the causal relevance of the selected sparse direction to the controlled mirativity contrast while leaving open whether the model internally separates mirativity from the language-specific surface pattern through which it was induced.

---

## 11. Negative results reveal a dissociation between internal representation and behavioral output

The most informative counterexamples may be as important as the six successes.

Gender/noun class was one of the strongest and most interpretable sparse features in the entire analysis. Feature 5205 received inspection grade A and strongly tracked feminine morphology in Arabic and Urdu. It produced by far the strongest ablation result and a strong steering result. Yet its behavioral effect was significantly negative: the target intervention changed the feature-high versus feature-low logit margin in the opposite direction, with a target-minus-control effect of approximately **−0.01328** and FDR \(q \approx 0.00214\).

Transitivity/valency displayed a similar dissociation. Feature 164 produced a large specific-positive ablation result and specific-positive steering, but its final behavioral target-minus-control effect was approximately **−0.02491**, again significant in the opposite direction.

Social deixis/honorifics provides another example. Feature 2081 had grade A interpretation as Korean formal/honorific morphology and passed both internal causal tests with monotonic steering, yet behavioral intervention moved the tested output preference in the wrong direction.

Quotation/reported speech also passed both internal causal stages, but its next-token behavioral result was null or slightly reversed.

These cases rule out an overly simple interpretation of SAE features as direct behavioral switches.

A decoder direction can contribute causally to the internal representation of a linguistic contrast while its addition does not increase—or may even decrease—the local probability of the corresponding surface realization. Several mechanisms could produce this dissociation: the relevant information may participate in later compensatory computation; the feature may be entangled with additional properties; the model may encode a distinction in a direction that is not aligned with its generative decision boundary; multiple features may interact nonlinearly; or the next-token branch-point metric may interrogate only one local consequence of a broader internal representation.

Whatever the mechanism, the empirical conclusion is clear:

**causal control of an internal representation does not imply predictable control of model output.**

This distinction should be retained prominently in the paper.

---

## 12. Human interpretability, statistical recoverability, and causal importance are separate axes

The combined results support a stronger methodological conclusion than any individual variable result.

Feature quality cannot be represented by a single scalar notion of "interpretability."

At least four questions must be asked separately:

1. Can the target distinction be decoded from the representation?
2. Can a sparse component be statistically associated with that distinction?
3. Does the sparse component have a human-readable interpretation consistent with the intended variable?
4. Does intervention on the component causally change downstream representation or output?

The experiments produced every relevant kind of disagreement.

Some variables were easily decoded but lacked a clean sparse feature. Some had statistically strong sparse features that turned out to be lexical or punctuation artifacts. Some poorly interpreted features produced strong causal effects. Some exceptionally interpretable features changed internal representations but failed or reversed at the output layer. Some variables weak under the initial probe and SAE evidence pipelines later yielded full-chain causal candidates.

The final cohort makes this especially vivid: none of the six full-chain successes had inspection grade A. Conversely, several grade-A features did not survive the behavioral stage.

This does not imply that inspection should be abandoned in favor of intervention. Without inspection, the six full-chain features would be vulnerable to stronger claims than the evidence permits. Instead, the findings argue for **triangulation**: semantic inspection determines what a causal effect can be called, while intervention determines whether the inspected feature actually matters computationally.

---

## 13. The results do not support a one-feature-per-variable model

The original research question naturally invites a search for individual sparse latents corresponding to individual linguistic variables. The results argue against treating that as the default expectation.

Several variables were represented by features that were clearly narrower than the target abstraction. Others appeared distributed across multiple features or shared features with other linguistic transformations. Final-token representations showed particularly high feature reuse. Some variables had stronger supervised probe evidence than sparse-feature evidence, suggesting that the relevant information may be distributed across activation space. Others had SAE evidence where strict probe evidence was weaker.

The causal stage similarly showed cases where matched control features had substantial effects, particularly for variables such as number marking. This suggests distributed or overlapping representation rather than a single privileged causal feature.

Accordingly, the strongest general model supported by the data is not:

> one linguistic variable → one sparse latent.

It is closer to:

> a linguistic distinction can recruit one or more sparse, partially shared, and often surface-grounded representational directions, some of which make causal contributions to downstream computation.

This interpretation is less visually appealing than a clean dictionary of linguistic concepts, but it is better supported by the evidence.

---

## 14. What the project establishes

The experiments support several conclusions with different levels of strength.

First, **low-level structural linguistic distinctions are widely encoded in XGLM-564M activations**. This is supported by cross-seed supervised probing, directional tests, and held-out marker/domain generalization.

Second, **a sparse autoencoder trained independently of the controlled feature dataset recovers substantial structure associated with these distinctions**. The signal is not merely an artifact of supervised probe training on the controlled labels.

Third, **supervised and sparse evidence converge for a majority of variables but are not equivalent**. Sparse decomposition and linear recoverability expose overlapping aspects of the representation.

Fourth, **statistical SAE association substantially overestimates clean semantic interpretability**. Strong features frequently correspond to lexical, morphological, punctuation, language, or tokenization correlates of the intended variable.

Fifth, **individual SAE directions can causally contribute to downstream representation of linguistic contrasts**. This is supported by specific ablation and steering effects relative to matched controls, dose response, and extremely small global perturbations.

Sixth, **some of these causal directions also influence actual model output probabilities**. Six pre-frozen mechanistic candidates produced positive, control-specific, FDR-corrected next-token effects with monotonic behavioral response.

Seventh, **internal causal mediation is more common than behavioral control**. Many features that strongly affect internal representations fail to alter output in the predicted direction.

Eighth, **semantic interpretability is not a reliable predictor of causal efficacy**. Poorly interpreted features can be causal, while highly interpretable features can fail behaviorally.

Ninth, **strict early filtering would have hidden scientifically relevant effects**. The final aspect/event-structure result and the animacy result demonstrate the value of retaining imperfect candidates as exploratory causal targets rather than equating one failed criterion with absence of representation.

Together, these conclusions support a methodology in which representation recovery, feature inspection, causal intervention, and behavioral evaluation are treated as cumulative but non-redundant forms of evidence.

---

## 15. What the project does not establish

The experiments do not demonstrate that XGLM contains forty discrete, abstract linguistic features corresponding directly to the typological inventory.

They do not demonstrate that the six final causal features are language-universal representations. Several are visibly tied to one language or one family of surface markers.

They do not establish that the natural-language meaning assigned to an SAE feature is exhausted by the controlled variable used to discover it. Polysemanticity and feature entanglement remain plausible, particularly for the weaker inspection grades.

They do not establish formal necessity or sufficiency of individual latents. The ablation and steering results are better described as necessity-like and sufficiency-like causal evidence because linguistic information may be redundantly or distributively encoded.

They do not demonstrate that SAE features are superior to supervised probes as representations of linguistic information. The two methods answer different questions, and each succeeded where the other sometimes failed.

They do not establish high-level behavioral consequences such as changes in truthfulness, bias, deference, refusal, social judgment, responsibility attribution, or epistemic reasoning. Step 9 measured local next-token preference at the first controlled linguistic divergence. It is a genuine behavioral output measure, but it is deliberately narrow.

Finally, the experiments do not yet establish the broader "constitutional language" hypothesis that low-level linguistic structures systematically alter alignment-relevant model behavior. They provide a mechanistic foundation for testing that hypothesis: some structural linguistic signals can be isolated and causally manipulated internally, and a subset already affects local model output. The downstream behavioral and alignment consequences remain a separate empirical question.

---

## 16. Limitations

The strongest limitation is model scope. All sparse causal results come from a single multilingual model, `facebook/xglm-564M`, with the SAE trained at hidden-state index 12. Raw probes examined a broader layer profile, but the causal claims concern one model and one SAE intervention site. Replication across model families, scales, layers, and independently trained SAEs is necessary before treating the observed patterns as general properties of language models.

The controlled dataset is synthetic by design. This gives experimental control but increases the risk that linguistic variables are represented through recurring surface realizations. Marker-family and lexical-domain holdouts significantly improve the split design, and natural-text feature inspection provides an additional safeguard, but neither guarantees abstraction. Several feature interpretations confirm that this concern is real.

The multilingual design is also intentionally compact. Variables requiring non-English evidence were generally assigned one selected language rather than being instantiated independently across multiple typologically different languages. Consequently, a feature associated with Turkish morphology or Korean honorifics cannot yet be assumed to represent the same structural property in another language.

The SAE corpus was separate from the controlled evaluation set and used no target supervision, which is a major strength. However, it was itself a generated multilingual natural-language corpus rather than a corpus composed entirely of naturally occurring text. This may affect the feature distribution learned by the SAE.

Candidate selection and interpretation also involved researcher judgment. The final behavioral cohort was cleanly frozen before behavioral outcomes were observed, but the causal candidate pool emerged after statistical analysis and natural-example inspection. Steps 7 and 8 should therefore be interpreted as strong causal validation of selected candidates, not as a preregistered test of a fully fixed feature map.

The SAE itself was trained once. Probe robustness was evaluated across multiple seeds, but the causal experiment does not establish robustness to independently retraining the SAE dictionary. Sparse dictionaries can permute, split, merge, or otherwise reorganize features across training runs.

The interventions modify a decoder direction across token positions. SAE decoder features are not guaranteed to be orthogonal or causally independent, and subtracting or adding one component can indirectly affect computations associated with correlated features. Matched controls and the extremely high representation cosines reduce concern about nonspecific disruption but do not eliminate this issue.

The behavioral evaluation is intentionally local. It compares competing next-token realizations at the first divergence between controlled sentences. This produces a clean and comparable metric, but it does not test complete generated sequences. Sentence-initial divergences use BOS as the common context, which means those cases are evaluated under less contextual information than later-divergence examples.

Behavioral test sets also contain only fifty pairs per variable. Bootstrap inference and the frozen multiple-comparison family address statistical uncertainty, but larger held-out evaluation sets would provide more precise estimates, particularly for the smaller effects.

The initial bfloat16 behavioral diagnostic showed quantized logit differences, requiring a float32 rerun. Because the hypothesis family, intervention specification, dose, controls, test split, and metric remained frozen, this is best understood as numerical correction rather than outcome-dependent redesign. Nevertheless, the episode illustrates that extremely small logit interventions require careful numerical treatment.

---

## 17. Implications for mechanistic interpretability

The results suggest several broader methodological lessons.

The first is that **decodability should be treated as evidence of information presence, not mechanistic localization**. High probe accuracy can coexist with distributed representations and does not imply a causal axis.

The second is that **SAE feature ranking should not be treated as semantic labeling**. Controlled contrasts are excellent tools for discovering candidate features, but a feature's statistical association with a label does not tell us its full meaning. Natural activation inspection remains necessary.

The third is that **top-activation interpretability is itself insufficient**. Feature 6618 provides a clear counterexample: its natural interpretation was poor, yet it became one of the strongest causal candidates. Causal validation can therefore reveal computational importance that descriptive inspection misses.

The fourth is that **matched intervention controls matter**. Several variables showed positive target effects that were no stronger than the effects of unrelated matched SAE features. Without control directions, these would have looked like positive causal findings.

The fifth is that **dose response provides valuable evidence**. The consistent effects of 0.5×, 1×, and 2× intervention levels strengthen the interpretation that some results arise from controlled manipulation of a relevant direction rather than a binary perturbation accident.

The sixth is that **representation-level and output-level causality should be evaluated separately**. The large gap between fifteen internally convergent candidates and six full behavioral successes demonstrates why mechanistic work should not stop once a hidden-state direction moves predictably.

Taken together, the pipeline offers a useful template for linguistic mechanistic interpretability:

**controlled contrast → supervised recovery → unsupervised sparse recovery → natural-text inspection → matched ablation → matched steering → pre-behavior freeze → output-level causal evaluation.**

The value of this framework is not merely that it produces positive findings. It systematically exposes where an apparently strong interpretation fails.

---

## 18. Implications for low-level linguistic influence and constitutional-language research

The broader motivation behind studying low-level linguistic features is that structural properties of language may affect model computation even when propositional content is held approximately constant.

The present results provide a necessary mechanistic precursor to that hypothesis.

They demonstrate that controlled changes in morphology, person reference, possession, aspect, stance-related marking, and other structural dimensions can correspond to internal directions that are not merely decodable but experimentally manipulable. For six variables, manipulating those directions also changes the model's immediate probability distribution over linguistic alternatives.

This makes it plausible that low-level linguistic form can participate causally in computations that later influence higher-level behavior.

However, the current work stops before demonstrating the stronger alignment claim. A change in next-token preference toward a morphological or stance-marked realization is not equivalent to a change in truthfulness, deference, social bias, uncertainty calibration, or refusal behavior.

The next phase of constitutional-language research should therefore use the present feature map and causal methodology to ask whether these linguistic interventions alter **semantic decisions while propositional content is controlled**.

The most informative experiment would not merely ask whether steering a mirativity feature generates more mirative morphology. It would ask whether activating that representation changes confidence, evidence weighting, epistemic caution, or downstream judgment on an otherwise matched task.

Likewise, social-deixis or honorific representations should ultimately be evaluated for their effects on deference, authority weighting, and social reasoning; evidentiality for evidence-sensitive confidence; agent-prominence and voice representations for responsibility attribution; modality for obligation and permission judgments; and discourse or perspective features for framing sensitivity.

The present work therefore provides evidence that such a program is mechanically plausible while leaving its most consequential behavioral hypotheses open.

---

## 19. Recommended interpretation of the final six variables

The six full-chain variables should be presented as **causally validated sparse correlates of controlled linguistic distinctions**, not as six fully discovered abstract concepts.

This wording captures the strongest common evidence shared by all six.

For the better-interpreted B-grade features, such as morphological suffixal structure and progressive aspect morphology, stronger linguistic language is reasonable so long as its scope is explicit.

For C- and D-grade features, the paper should retain the proxy interpretation established during natural-text inspection. Their causal success is scientifically interesting precisely because the direction can matter computationally even when its semantic decomposition remains unclear.

This distinction prevents the final results from being weakened by overclaiming.

A reader should leave with two conclusions simultaneously:

**some sparse linguistic directions are genuinely causal**, and **their causal role does not guarantee that the SAE has discovered the human linguistic abstraction used to name the controlled dataset variable**.

Both conclusions are supported by the data.

---

## 20. Recommended overall claim for the paper

The strongest compact claim supported by the completed experiments is:

> Across forty controlled structural linguistic contrasts in XGLM-564M, linguistic information was broadly recoverable from both supervised activations and an independently trained sparse autoencoder, but statistical feature recovery frequently reflected narrower lexical, morphological, language-specific, or orthographic correlates rather than clean abstract linguistic features. Causal intervention nevertheless identified a subset of sparse directions that specifically mediated downstream representations. Fifteen variables showed convergent ablation and steering evidence with monotonic dose response, and six of these produced FDR-corrected, control-specific changes in next-token linguistic preference after the behavioral cohort had been frozen. These results show that sparse representations can capture causally relevant linguistic structure while also demonstrating that recoverability, human interpretability, internal causal mediation, and behavioral influence are distinct properties.

That claim incorporates the positive result without erasing the negative evidence that makes the project scientifically credible.

---

## 21. Final conclusion

The experiments began with a broad question: whether basic structural properties of language can be found inside a language model as measurable internal features and whether those features matter causally.

The answer is **yes, but not in the simplest possible form**.

Structural linguistic contrasts are widely recoverable from XGLM activations. Sparse autoencoding exposes substantial corresponding structure without being trained on the controlled linguistic labels. Supervised and sparse representations converge across a majority of variables. Yet the sparse dictionary does not resolve neatly into one abstract typological concept per feature. Many candidates encode the surface machinery through which the linguistic distinction is expressed: a suffix, pronoun, complementizer, punctuation pattern, lexical class, or language-specific morphology.

That does not make those representations irrelevant. Causal experiments show that several of these imperfect and sometimes poorly interpreted sparse directions actively participate in the model's computation. Removing them weakens downstream linguistic distinctions; adding them moves representations in the predicted direction; and for a smaller set, those internal changes propagate to the model's token probabilities.

At the same time, some of the most interpretable and internally causal features fail or reverse at the behavioral stage. This establishes a meaningful boundary between **representation** and **behavior**. A model may internally encode and causally use a linguistic distinction without that representation functioning as a simple output control knob.

The final result is therefore more informative than either a universal success or a universal failure.

It demonstrates that low-level linguistic structure is mechanistically accessible, that sparse representations can isolate components with real causal influence, and that such influence occasionally reaches observable model behavior. It also demonstrates why strong interpretability claims require more than decoding, more than SAE feature ranking, and even more than an apparently interpretable activation pattern.

The most defensible picture is one in which linguistic structure is encoded through **partially sparse, partially distributed, and frequently surface-grounded representations whose causal influence varies across the computational pathway from hidden state to output**.

This provides a concrete mechanistic foundation for studying how structural language may influence higher-level model behavior. The next question is no longer simply whether linguistic form exists inside the model. The evidence indicates that it does, and that some of it matters causally.

The remaining question is **what those representations ultimately make the model do**.