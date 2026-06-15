# Mechanism Map for the Central Operation — Consolidated Handoff

**What this is.** A coverage map of existing mechanisms against the twelve characteristics of the central operation — candidate mechanisms by *function*, where one mechanism does several jobs, and (most usefully) where satisfying one characteristic damages another. It is a map of the possibility space, **not** a recommended design.

**Provenance.** Merged from four independent passes: a deep-research literature sweep, plus an Opus/ChatGPT/Grok fusion. Where those passes converge, the finding is marked **[CONFIRMED]** (robust across independent methods). Where a resolution is this-round's leading bet, it is marked **[PROPOSED]** — held provisionally per the sit-with-it-before-ratification discipline; the next round may challenge it and should not inherit it as settled.

**Reading convention.** Mechanism names appear freely here (this is the search *output*, not the search prompt). The operation being designed is still described in neutral terms. Each candidate is tagged where relevant for the stances the spec cares about: **online/offline** (bears on characteristic 7), **unified/split** (bears on the 2-vs-3 question), **iterated/one-shot** (bears on the tracing question), **own-space/shared-space** (bears on 10), and **persistence-in-weights/separate-store** (bears on the persistence question).

---

## Framing: the primitive, and the two hubs

The one operation — *poll → evoke an expected companion/successor bundle → return it → adjust by the discrepancy* — is abstractly a **content-addressable evocation step nested inside a discrepancy-driven loop over a set-valued state**. No existing system is built around exactly that primitive, but it decomposes cleanly, and two literatures recur as hubs:

- **Associative-memory / attractor dynamics + vector-symbolic algebra** — owns the part-whole, set-valued, confidence, and splitting side (characteristics 1, 2, 3, 5, 9) and supplies the substrate for the 6/8/10 store.
- **Predictive-coding / active-inference dynamics** — owns the loop, the command-as-prediction stance, priming, and learned coherence (characteristics 7, 10, 11, 12).

**Most of the design tension is between these two hubs.** [CONFIRMED — all four passes identify exactly this split.]

---

## Per-characteristic map

### 1 — Wave-bundling (one embedding per cortex per wave; co-arrival = co-occurrence; no finer timing)

The characteristic is really a **set-valued, permutation-invariant state with no shared space**, bound by membership rather than fine timing.

- **Vector Symbolic Architectures / hyperdimensional computing** — the most direct fit. *Bundling* (superposition) is commutative and unordered = "no finer time within a wave"; *binding* tags which cortex a slice came from without imposing order (Plate 1995, Holographic Reduced Representations; Smolensky 1990, tensor-product binding; Gayler 2003; Kanerva 2009, HDC). A bundle is then a superposition of role-bound slices. **own-space-compatible.**
- **Direct-sum / typed-product representation** (each slice stays in its native space) preserves "no shared space" even more cleanly than VSA — at the cost of being a construct, not a named architecture. **own-space.**
- **Global workspace** (Baars 1988; Dehaene & Naccache 2001) is the structural analogue of a central unit that "never touches the world, only sees and sends summaries" — supplies the architecture but no association, decay, or learning.
- **Theta–gamma phase–amplitude coupling** (Lisman & Jensen, *Neuron* 2013) is the neural analogue of slot-packaging; Jensen & Lisman 2000 showed phase distinctions finer than a gamma slot do not improve reconstruction — i.e. no useful timestamp finer than the slot. Auditory framing: Giraud–Poeppel line.
- **Event segmentation** (Zacks/Reynolds/Baldwin; Bayesian-surprise model, Kumar et al., *Cognitive Science* 2023) supplies the complementary idea that "now"-to-"now" boundaries arise from transient prediction-error increases — relevant because the wave-to-wave transition is where surprise is computed.

**Tension (1 vs 2/3):** wave-quantization deliberately discards within-window microstructure that spiking/STDP and reservoir methods mine for predictive power. Those can run *inside* a cortex but cannot supply the central timing.

**Caveat on a tempting grounding:** *binding-by-synchrony* (von der Malsburg 1981; Singer 1999) is contested (Shadlen & Movshon 1999; Ray & Maunsell 2010: gamma synchrony is stimulus-dependent and a poor binding tag; Burns et al. 2011: gamma is not a precise clock). **Wave-membership tagging (VSA roles) is the sounder grounding** — and the spec already sidesteps the debate by defining the wave as an *imposed* sampling clock, not emergent synchrony.

### 2 — Cued calling-forth within-wave (given part of a bundle, evoke the rest)

Pattern completion / hetero-association over a set.

- **Hopfield and modern/dense associative memories.** Classical Hopfield (1982) completes from partial cues but has low capacity; dense variants (Krotov & Hopfield 2016; Demircigil et al. 2017; Ramsauer et al. 2020 for continuous inputs) give super-linear capacity and near-single-step retrieval over continuous embeddings. Universal Hopfield Networks (Millidge et al. 2022) give the neutral skeleton: *similarity → separation → projection*. **persistence-in-weights; shared-space (default).**
- **Sparse Distributed Memory** (Kanerva 1988) — partial-cue completion in high-D space, intrinsically noise-tolerant (matters for 8). **persistence-in-weights.**
- **Bidirectional / hetero-associative memory** (Kosko 1988) — associates across *distinct* spaces without collapsing them; **own-space-compatible**, a better fit than common-latent methods for "each cortex keeps its own space."
- **Associative memory via predictive coding** (Salvatori, Song, Bogacz et al. 2021) — multimodal hetero-association (retrieve image from description and vice versa) inside one hierarchical generative network.
- **VSA unbinding + cleanup** — recover a missing slice by binding with the cortex tag's inverse, then clean up against an item store. (Note the cleanup dictionary — see persistence question.)
- **Hippocampal CA3 pattern completion** (Marr 1971; Treves & Rolls 1994) as the biological exemplar.

**Hub:** dense associative memory serves **2, 3, 5** and partly **9** — the strongest single-mechanism hub on the completion side.

### 3 — Cued calling-forth across-wave (current bundle → likely successor)

Hetero-association in time / sequence prediction.

- **Asymmetric Hopfield / sequence attractors** (Sompolinsky & Kanter 1986; long-sequence capacity, Chaudhry et al. 2023; hidden-neuron sequence attractors, 2024) — store transitions via temporally asymmetric weights *in the same network* that does (2)'s symmetric completion. **unified; iterated; persistence-in-weights.**
- **Sequence memory / hierarchical-temporal models** (Hawkins & Ahmad 2016) — high-order next-step prediction over sparse codes, learned continuously with local rules; serves 3, 4, 7 together, on sparse codes relevant to 8. **online; unified.**
- **Latent recurrent state-space (world) models** (Ha & Schmidhuber 2018; Hafner et al. 2019 PlaNet/RSSM; 2020 Dreamer) — "given current latent, evoke next latent," but split observation-model from transition-model and train offline. **offline; split.** (Collides with 7.)
- **Reservoir / echo-state / liquid-state** (Jaeger 2001; Maass et al. 2002) — carry recent context; readouts evoke the next state. **online.**
- **Successor representation** (Dayan 1993; Stachenfeld et al. 2017; empirical successor-skewing, *eLife* 2023) — expected *future occupancy* rather than only the next state; a natural bridge to growing reach (11).
- **Predictive coding in generalized coordinates** (Friston & Kiebel 2009) — successor prediction within one generative loop. **unified.**

**Open (2 vs 3) — KEPT OPEN.** Associative/VSA/sequence-memory families *unify* 2 and 3 (cue and target differ only by wave index, or symmetric vs asymmetric weight terms in one network); world-model families *split* them. No evidence forces either reading. The unification is more parsimonious and more consistent with the one-operation doctrine; it is not closed here.

### 4 — Tracing (called-forth bundle becomes the next cue → multi-step chains, unprompted)

Closed-loop autoregressive rollout in the association space.

- **Iterated attractor / asymmetric-weight chains** (Sompolinsky & Kanter 1986) and **heteroclinic / metastable sequences** (Rabinovich et al. 2008) — current state cues the next, one step at a time. **iterated** — the parsimonious "same operation iterated" reading.
- **Reservoir free-running dynamics** (Jaeger 2001; Sussillo & Abbott 2009, FORCE). **iterated.**
- **Latent imagination / rollout** (Ha & Schmidhuber 2018; Dreamer) — does this, but as a distinct generative act. **one-shot-leaning; offline.**
- **Hippocampal replay / preplay** (Foster & Wilson 2006; Diba & Buzsáki 2007; Dragoi & Tonegawa 2011) — biological exemplar of self-generated chains.

**Tension (4 vs 11) and the silent-swap warning.** Iterated single-step evocation drifts off-manifold after a few steps unless the space is well-shaped — *this is the practical ceiling on reach.* Formally, autoregressive rollout's probability of a fully-correct n-step trajectory falls roughly as (1−e)^n (exposure-bias lineage, Bengio et al. 2015; the off-distribution argument associated with LeCun 2023). Note that Dreamer is robust to horizon length precisely because it bolts on a separate **value model** to estimate returns beyond the imagination horizon — exactly the kind of silent architecture swap the central open question exists to catch. If reach is to grow as "the same operation maturing," prefer iterated single-step whose forward range extends because the space is better-shaped — not a switch to trained rollout-plus-planner.

### 5 — Strengthening by recurrence (confidence as a graded property of the evocation, not a stored score)

The "no separate scalar score" clause is sharply discriminating.

- **Energy-based associative memories satisfy this natively.** A frequently-written pattern deepens and sharpens its basin; retrieval is more confident because the attractor is steeper and convergence cleaner. Confidence *is* basin geometry / convergence speed (Hopfield 1982; Amit 1989; Krotov & Hopfield 2016). Direct neural evidence: **Wang, Falcone, Richmond & Averbeck, *Nature Neuroscience* 2023** — in macaque PFC, attractor basins around decision-states had *steeper landscapes for offers that led to consistent decisions*, operationalising confidence as an emergent property of the landscape, not a stored value.
- **Hebbian / fast-weight strengthening** (Hebb 1949; Oja 1982; Ba et al. 2016) — repeated co-activation raises efficacy; evocation amplitude/speed encodes confidence.
- **SDM counter magnitude / reconstruction margin** (Kanerva 1988).
- **Predictive-coding precision** (Feldman & Friston 2010) — graded confidence from the dynamics, *but* precision is often implemented as a parameter, which risks being exactly the "separate stored score" the spec forbids. **The line between "graded property of the evocation" and "a precision parameter" is not sharp in the literature — decide it explicitly rather than inherit it.**

**Hub:** basin-geometry sharpening gives 5 *and* is the same substrate as 2/3/9 (basin shape = the association).

### 6 — Weakening by disuse, coordinated with controllable drift/decay (fading = dynamics; drift a first-class, cortex-independent parameter)

First leg of the critical triad.

- **Palimpsest memory models** (Nadal, Toulouse, Changeux & Dehaene 1986; Parisi 1986) — arguably the *most native single mechanism*: memory that intrinsically overwrites old with new and is recency-biased by construction. Fade-as-dynamics, favour-recent, no deletion step — a direct match to the spec's wording. **persistence-in-weights.**
- **Decaying Hebbian / fast-weight traces** with an explicit decay constant λ that is a single first-class parameter independent of any cortex's rule (Hinton & Plaut 1987; Ba et al. 2016).
- **Multi-timescale / cascade synaptic consolidation** (Fusi, Drew & Abbott 2005; Benna & Fusi 2016) — *needed* so decay (6) coexists with recurrence-strengthening (5) without erasing consolidated material. Single-rate decay gives recency but kills often-recurred associations.
- **Homeostatic plasticity** (Turrigiano et al. 1998) — relative-influence loss without deletion.
- **Representational-drift-as-storage** (Ornstein–Uhlenbeck formulations, *Scientific Reports* 2025) — casts decay as a tunable diffusion with an explicit time-constant.
- **Active-inference forgetting** — a tunable forgetting rate ω on Dirichlet concentration parameters (Smith, Friston & Whyte 2022) plus structural pruning by Bayesian model reduction (Smith et al. 2020). The nearest realisation of decay as an explicit knob.

**No-fit flag:** the spec wants decay *independent of any cortex's update rule*. Every candidate attaches decay to the substrate it lives on; active-inference ω is nearest but decays *parameters/counts*, not a free-standing representation space.

**Tension (6 vs 5, and 6 vs continual-learning):** the anti-forgetting literature (EWC, Kirkpatrick et al. 2017; synaptic intelligence, Zenke et al. 2017; CLS, McClelland et al. 1995) is built to *prevent* the exact fading 6 wants — useful for stability, directly opposed to disuse-fade unless reworked into controlled decay.

### 7 — No phase separation (every wave both uses and adjusts; no train/run split)

- **Online local plasticity** (STDP: Bi & Poo 1998; Song, Miller & Abbott 2000); sequence-memory models are explicitly continual with no train/test split (Hawkins & Ahmad 2016). **online.**
- **Adaptive Resonance Theory** (Carpenter & Grossberg 1987) — stable online category learning with no batch phase; its vigilance mechanism re-appears under 8 and 9. **online.**
- **Online predictive coding / active inference** (Rao & Ballard 1999; Friston 2005) — inference (use) and learning (adjust) under one continuously-evaluated objective. **online.**
- **Fast weights** as the canonical adjust-while-running substrate.
- **Continual learning without task boundaries** (stability-plasticity reviews; utility-perturbed gradient methods).

**Sharpest breakage in the whole map (7 vs 3/4/11):** RSSM/Dreamer — the strongest fit for sequence evocation and reach — is trained in a *separate optimization phase*. The mechanism that best satisfies 3/4/11 most cleanly violates 7. Reconciliations: online/continual world-model learning, predictive-coding dynamic models (online but weaker at long-horizon rollout), or sparse sequence-memory (online but representationally thinner). **Note:** a slow-learning/fast-inference *timescale* split in some predictive-coding accounts is **not** a train/run split — handle that distinction carefully rather than rejecting PC on it.

### 8 — Tolerance of a moving/drifting space (associations stay usable as vectors shift; favour recent material)

Second leg of the triad.

- **Neuroscience of representational drift + stable readout** (Ziv et al. 2013; Driscoll et al. 2017; Rule, O'Leary & Harvey 2019; Deitch, Rubin & Ziv 2021). The **self-healing-code result (Rule & O'Leary, PNAS 2022)** is the existence proof the triad needs: a downstream readout *can* track a continually reconfiguring upstream code via Hebbian/homeostatic adaptation, sometimes without an explicit error signal. Coordinated-drift work (2025) adds that drift can be a structured translation/rotation preserving population geometry, enabling stable readout.
- **Adaptive-prototype systems** — SOM (Kohonen 1982), Growing Neural Gas (Fritzke 1995), Grow-When-Required (Marsland et al. 2002), ART (Carpenter & Grossberg 1987) — prototypes track moving distributions online.
- **Recency bias is automatic** in any decaying associative substrate (fast weights, reservoir fading memory) — which is why 8's "favour recent" and 6's decay couple naturally.

**Tension (8 vs 2):** fixed attractors are robust to *noise* but not to *systematic coordinate drift*; they need moving basins / online plasticity, and drift-tolerance bought through redundancy can blunt sharp within-wave completion (2).

### 9 — Refinement by splitting (coarse association divides into finer ones, no global rebuild)

- **ART with vigilance control** (Carpenter & Grossberg 1987) — one of the aptest fits: raising vigilance splits a broad category into finer ones (*ball → red-ball, green-ball*) incrementally. **online; native splitting.**
- **Growing Neural Gas / Grow-When-Required** (Fritzke 1995; Marsland et al. 2002) — insert units locally where representation error is high.
- **Progressive differentiation** (Rogers & McClelland; Saxe, McClelland & Ganguli 2013/2019 — deep linear nets provably differentiate coarse→fine from hierarchical statistics).
- **Context-specific cell allocation** in sparse sequence-memory — the same code represented by different cells in different contexts, effectively splitting without rebuild.
- **Dynamically Expandable Networks** (Yoon et al. 2018) — literally split/duplicate a unit when its role drifts past threshold; note this needs a *local* retrain, so whether it counts as "no global rebuild" depends on locality.
- **Nonparametric Bayesian models** (Teh et al. 2006, HDP) — grow complexity with evidence, but explicit structural inference can read as a *distinct* operation; flag against the one-operation lean.

**Tension (9 vs 5/6):** splitting redistributes "confidence mass." A naive energy model lets a newly-split fine basin cannibalise the parent's depth, and decay (6) can erase the rarer child (green-ball) before it consolidates. Couples 9's splitting schedule to 6's decay schedule and 5's consolidation.

### 10 — Native-slice consumption (modality-agnostic; whole bundle evoked; command/prediction lives in the cortex)

Third leg of the triad — cleanest anchor is the active-inference stance that **motor output is just another prediction**.

- **"Predictions not commands"** (Adams, Shipp & Friston 2013, *Brain Structure and Function*) — in hierarchical active inference, motor signals are processed in analogy to perceptual signals. *Exactly* characteristic 10: the centre emits one expected bundle; a motor cortex treats its slice as a target to fulfil (the command), a sensory cortex treats its slice as an expectation to test, and the central process is blind to which is which. **No other family has already committed to "command and prediction are the same kind of object."**
- **Active Predictive Coding / sensory-motor theory of neocortex** (Rao 2024, *Nature Neuroscience*) — each cortical area estimates both sensory states and actions in one scheme, and coupled to a hippocampus-like associative store it binds multimodal activations. The closest existing thing to the whole architecture's shape.
- **Resonator networks** (Frady, Kent & Olshausen 2020) — the most targeted tool for *factorising multiple superposed factors out of one bundle*, i.e. recovering each cortex's slice from the whole. None of the standard families name this; it is the right tool for the 2/10 "recover each slice from a superposition" problem. **own-space-compatible.**
- **Bidirectional / hetero-associative memory** (Kosko 1988) and **binding across separate encoder spaces** (HEN, Kashyap et al. 2024 — binds CLIP-text ↔ D-VAE-image without a common embedding, relying on association uniqueness) — the right shape for native slices, **own-space-compatible**, though HEN relaxes rather than eliminates the encoded-space requirement.
- **The "blind to which is which" requirement** is met by VSA/Hopfield evocation: the evoked bundle is just a vector; each cortex's tag/slice is interpreted locally. The whole-bundle-at-once requirement favours the **superposition/attractor** read over an autoregressive per-slice decoder.
- **Ideomotor / Theory of Event Coding** (Prinz 1997; Hommel et al. 2001) — cognitive-science cousin, but "common coding" risks collapsing the native spaces; use carefully.

**Load-bearing tension (10 vs common-latent):** every family that solves multimodal integration via a *shared latent cause* (most predictive-coding, world models — BayesPCN implements hetero-association by forming a *joint* key-value object) helps 2/3/11/12 but threatens "each cortex keeps its own space" and "central operation modality-agnostic." The integration story and the own-space story pull against each other.

### 11 — Growing reach (early: correction-only; mature: bias perception before arrival; same operation, more reach)

- **Predictive coding gives priming for free** — top-down predictions descend *before* input arrives and pre-shape lower-level activity (Rao & Ballard 1999; Kok, Jehee & de Lange 2012; Summerfield & de Lange 2014; Bar 2007). Increasing reach = the generative model's dynamic order/horizon deepening while the *operation* (minimise discrepancy) is unchanged — the best fit for "same operation, what grows is reach."
- **Developmental predictive processing** (Köster et al. 2020; Schwarzer 2024; neonatal top-down prediction; "infants process prediction errors at the theta rhythm") — empirical grounding for prediction/priming maturing with experience and motor development.
- **Successor representation** (Dayan 1993; Stachenfeld et al. 2017) — naturally extends beyond one step.
- **Expected-free-energy / anticipatory active inference** — formalises the shift from after-the-fact correction to before-arrival biasing, and supplies the hook toward *surfacing-for-arbitration* the downstream-action question requires.
- **Sparse sequence-memory chaining** and **reservoir rollout** also extend reach as dynamics stabilise.

**Warning:** "early = correction, mature = priming" is the *same* loop at different horizon/precision settings — but it is *two* mechanisms if early-regime is reservoir-style surprise detection and mature-regime is trained rollout/planning. Flag any design that swaps reactive error for a trained planner across the regimes.

**Extensibility flag:** predictive-coding/active-inference candidates extend toward priming and toward surfacing-for-arbitration (predicted states feed a downstream selector). A pure pattern-completer or bare early-surprise reservoir does **not** extend this way — a dead-end even if it wins the early predictive task.

### 12 — Coherence as learned, not imposed (cross-cortex mismatch surfaces as error; integration is learned)

- **Cross-modal predictive coding** (Rao & Ballard 1999; Friston 2005; Bastos et al. 2012) — each modality predicts and is predicted by the others through the central state, so mismatch *is* the discrepancy that gets minimised; coherence emerges because incoherence is surprising.
- **Bayesian multisensory causal inference** (Ernst & Banks 2002; Körding et al. 2007) — the key nuance: supports *learned non-integration*, i.e. deciding whether two streams even share a cause. The correct grounding for "coherence not wired in," versus forced fusion.
- **Self-supervised cross-modal alignment** (Owens & Efros 2018 — learns from detecting audio-visual misalignment) and **developmental multisensory recalibration** (temporal synchrony as the early glue).
- **Hebbian cross-modal association** (Hebb 1949) and **sensorimotor contingency theory** (O'Regan & Noë 2001) as alternative routes.
- **Global workspace** supplies broadcast/routing but *imposes* unity rather than learning it.

**Tension (8 vs 12):** drift-tolerance achieved via *compensatory error signals between regions* can *implicitly enforce* coherence — making integration a side-effect of compensation rather than something learned-because-surprising. Watch that the mechanism used for 8 doesn't quietly wire in the coherence 12 says must be learned.

---

## Synergy hubs (one mechanism, several characteristics)

| Hub | Covers | Native strengths |
|---|---|---|
| **Dense/modern associative memory + VSA binding/bundling** | 1, 2, 3 (under the unifying reading), 5, 9 — and the substrate for the 6/8/10 store | set-completion (2); confidence-as-basin-geometry (5); unordered superposition (1); own-space binding (10) |
| **Predictive coding / active inference** | 7, 10, 11, 12 — under one discrepancy-minimising objective | "predictions not commands" (10); cross-modal error (12); precision-and-horizon (5, 11); priming-for-free (11) |

---

## The critical triad — can ONE approach satisfy 6 + 8 + 10 at once?

**[CONFIRMED] No off-the-shelf architecture does, and the three pull in opposing directions.** This is the central result, agreed across all four passes and the deep-research sweep.

- **6** wants the central substrate to have *its own* parameterised dynamics — a space that decays/drifts on a clock the cortices don't control → argues for an explicit, parameterised association field.
- **8** wants evocation *robust to the very drift 6 introduces* — small input shifts → small retrieval shifts → argues for distributed, high-dimensional, similarity-based storage.
- **10** wants evocation to produce *one modality-agnostic vector object*, not a typed structure → argues against anything that must know which slice is a target vs an expectation.

**Why no single mechanism bridges all three.** Drift/decay-tolerant associative dynamics (6+8) are almost always formulated in a *single shared* space with a common metric (hetero-association typically reduces to auto-association on a concatenated *joint* vector — BayesPCN) — conflicting with 10's modality-blindness and no-shared-space. Conversely, the cleanest 10 mechanisms (active inference, common coding, Active Predictive Coding) assume a *stable generative model* whose structure does not itself drift; their decay acts on slow parameters, not a continuously drifting embedding. Closest partial bridges: BayesPCN (6 + partial 10, no action side), Rao's Active Predictive Coding (10 + partial cross-modal binding, no decay/drift knob), OU-drift storage (6+8, no action), active-inference-with-ω (6 + 10, but parameter-decay not embedding-drift). **None unites all three.**

### [PROPOSED] The closest constructible candidate, and its three open seams

A fusion — held provisionally, not ratified: a **sparse, high-dimensional distributed associative store (VSA/SDM-flavoured) with multi-timescale homeostatic decay, drifting in a readout-orthogonal subspace, read by attractor/similarity dynamics that emit whole bundles consumed slice-wise by modality-agnostic cortices.** Every component is real and citable; the integration is not in the literature. Three seams are exactly where original work is needed:

- **Seam A — 6 and 8 are co-satisfiable *only if* the controllable drift is confined to readout-irrelevant (null-space) directions.** The drift literature gives the handle (drift as diffusion in null-space directions) *and* the warning that empirical drift is **not generally orthogonal** to the readout manifold (Rule & O'Leary 2022). A concrete, falsifiable design constraint, not a free lunch: constrained-drift = co-satisfiable; uncontrolled drift = 6 and 8 fight.
- **Seam B — decay must be consolidating, not single-rate.** Pure exponential decay gives 6's recency but cannot keep often-recurred material (5) stable under drift (8). The reconciliation is multi-timescale plasticity (Benna & Fusi 2016) plus reactivation/refresh — so 6 couples to 5 and 8 through the consolidation schedule.
- **Seam C — the 10-specific risk: drift degrades clean whole-bundle retrieval.** Dense associative memories enter **spurious metastable states** as pattern separability changes, and a drifting space (8) continuously changes separability — so the very drift wanted for 6/8 *worsens* the single-shot bundle read of 10. Mitigation: route 10 through a **sparse** distributed store (SDM / sparse coding, Olshausen & Field 1996), where patterns stay separable, rather than a dense one when drift is aggressive.

**Separate-store residue to decide consciously:** VSA's cleanup item-store and SDM's address decoder quietly reintroduce the very separate store the spec wants folded into the operation (see the persistence question).

**Stated plainly:** there is no existing architecture whose single native operation is "evoke a whole modality-agnostic bundle from a set-valued cue over a deliberately drifting, intrinsically-decaying space." The 6+8+10 triad is a real gap and must be constructed.

---

## Tension table (where satisfying one characteristic damages another)

| Tension | Mechanism that helps one… | …but breaks |
|---|---|---|
| **7 vs 3/4/11** | RSSM/Dreamer offline-trained rollout (best sequence/reach) | no train/run split |
| **8 vs 10** | drift (good for 6/8) | increases spurious metastable states → degrades clean whole-bundle read |
| **6 vs 5/8** | single-rate decay (recency) | erases consolidated/recurred associations |
| **3/4 vs 8** | asymmetric sequence attractors (high-fidelity succession) | assume stationary patterns; stale under drift |
| **9 vs 5/6** | basin-splitting (refinement) | rarer child decays before consolidating |
| **5 vs 6 vs 9** | deepening a basin (confidence) | entrenches against both fade (6) and split (9) — three-way |
| **1 vs 2/3** | wave-quantization | discards sub-wave timing STDP/reservoirs need |
| **10 vs 2/3/12** | shared latent cause (clean integration) | collapses each cortex's own space |
| **8 vs 12** | compensatory cross-region error (drift-tracking) | implicitly *imposes* coherence rather than learning it |
| **2 vs 10** | shared-space completion (easy cross-modal recall) | violates no-shared-space; resonator/BAM needed instead |

---

## Honest gaps (where forcing a familiar mechanism would be the only way to claim coverage)

- **Decay as a substrate-independent first-class parameter (6).** No mechanism cleanly separates the decay knob from the representation it acts on. Active-inference ω is nearest but parameter-bound.
- **The 6+8+10 triad jointly** — as above. Genuine open design space.
- **Modality-agnostic associative binding with no common space.** HEN/resonator relax but do not eliminate the encoded-space requirement; a truly metric-free version is unattested.
- **Decay-tolerant high-capacity sequence storage.** Sequence attractors assume stationary patterns; no candidate combines long-sequence capacity with graceful drift.
- **Asynchronous cortex rates vs a fixed central wave.** No surveyed mechanism addresses the *resampling/aliasing* problem of a fixed-rhythm central poll over peripherals emitting at different rates — what sets wave duration relative to per-channel dynamics. **Neural ODEs / continuous-time recurrent dynamics** (Chen et al. 2018; Beer 1995) are the natural substrate but are barely developed for this role. An under-served corner, and it sits at the foundational wave↔cortex interface.
- **Capacity/scaling under continual drift.** No literature bounds how many whole-bundle associations survive a given decay rate and drift speed. Characterise empirically.
- **Operational metrics.** How to *test* whether a built system exhibits each characteristic (measuring reach-growth, drift-tolerance, fade) is absent from all source literatures — worth specifying alongside the design.

---

## Open questions — surfaced, not resolved

1. **Within-wave (2) vs across-wave (3): one mechanism or two?** *Open.* Associative/VSA/sequence-memory families unify them; world-model families split them. Unification is more parsimonious and more consistent with the one-operation doctrine, but no evidence forces it. *Candidates tagged unified vs split above.*
2. **Single-step iterated vs distinct trajectory-emitting operation.** *Open, with a warning.* Iterated single-step is the parsimonious reading and what sequence-memory/PC/closed-loop reservoirs do. One-act trajectory emission exists (RSSM rollout, heteroclinic chains) but the strongest versions add horizon-extension machinery (value models) — a silent architecture addition. Prefer iterated single-step whose forward range grows because the space is better-shaped, not a swap to trained rollout. *Candidates tagged iterated vs one-shot above.*
3. **Unit of the called-forth thing.** *Open.* Working assumption (whole bundle) is supported by VSA superposition and Hopfield set-completion. Granularity genuinely undetermined: whole bundle (one vector), per-cortex slice set, or hierarchical bundle-of-bundles. The drift/sparsity analysis slightly favours *sparse whole-bundle* units for 10's blindness requirement.
4. **Where persistence lives.** *Open, but the spec's own logic leans one way.* "Confidence is a graded property, not a stored score" (5) and "fading is dynamics, not deletion" (6) both argue that **associations ARE the persistence** — folded into the operation's structure (energy landscape / fast-weight field / drifting manifold). Attractor/Hopfield/PC candidates fold persistence into weights; CLS and hippocampal-index theory imply a separate store. The one place a separate store sneaks back is the **VSA cleanup dictionary / SDM address decoder** — decide that explicitly. *Candidates tagged in-weights vs separate-store above.*
5. **Downstream arbitration extensibility.** Predictive coding / active inference satisfies "must extend toward priming and arbitration" — the same machinery already separates perceptual updating from preference/action selection (expected free energy). A pure early-surprise reservoir or a bare auto-associative completer does **not** — flag any such mechanism as a dead-end even if it wins the early predictive task.

---

## [PROPOSED] One staged build order, with revisit-triggers

Not a committed architecture — decision scaffolding, held provisionally. If you were to stage a build, this order is defensible, and each step names the observation that would force a rethink:

1. **Implement 10 (modality-agnostic evocation) first, on a quasi-stationary space** — Active Predictive Coding or active-inference common coding, with resonator-network slice-recovery for the 2/10 problem. *Revisit-trigger:* if whole-bundle reads cannot be recovered per-cortex without a shared embedding, the own-space constraint forces a VSA/BAM substrate from the start.
2. **Adopt an attractor-with-asymmetric-terms substrate for 2–5**, folding persistence into weights (addresses the persistence question without a separate store). *Revisit-trigger:* if sequence capacity under drift collapses (the 3/4-vs-8 tension), add hidden-neuron sequence attractors or a CLS-style fast store with **online interleaved** replay — never an offline phase, to preserve 7.
3. **Introduce controllable decay (6)** as multi-timescale/consolidating (Seam B), not single-rate. *Revisit-trigger:* if recency-favouring recall degrades sequence fidelity below task threshold under drift, abandon the shared-space assumption for per-cortex binding despite its uniqueness limitation.
4. **Stress-test under induced drift (8)**, confining drift to readout-null-space directions (Seam A); if drift is aggressive, route 10 through a sparse store (Seam C). *Revisit-trigger:* if empirical drift won't stay orthogonal to the readout manifold, 6 and 8 fight and the decay schedule must be coupled to the readout geometry directly.
5. **Use prediction-error magnitude as the universal currency** tying 1 (segmentation), 11 (priming-vs-correcting), and 12 (learned coherence) — the most synergistic single design decision.
6. **Reject any core-operation candidate that cannot extend to priming and arbitration**, even strong early predictors.

---

## Caveats

- Several key sources are 2024–2026 preprints (OU-drift-as-storage, Active Predictive Coding's preprint, coordinated-drift) — treat their specific quantitative claims as provisional.
- The fused inputs are partly model-generated; the citations inspected here are canonical and correctly attributed, and the deep-research subset was retrieved with several claims verified in-source (the basin-steepness result, the joint-object mechanism, the separate-spaces binding). The standard caveat applies: spot-check the few recent/specific references before leaning on them.
- The spec's deliberately neutral vocabulary makes some mappings interpretive — e.g. whether DEN's local retrain counts as "no global rebuild," or whether active-inference parameter decay counts as "drift on the representation space." These are judgment calls, flagged in-text.
- Coverage across twelve large literatures is necessarily uneven; absence of a cited candidate for a sub-claim reflects search scope, not proof of non-existence.
- The **[PROPOSED]** seams and the staged build are this-round bets. They belong in the same provisional box as the routing-layer move — strong leads to sit with, not settled. Only the **[CONFIRMED]** items (the 6+8+10 gap, the two-hub split, the major tensions) carry cross-method weight.
