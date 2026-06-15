# Mechanism Map Against the Central-Operation Specification

A coverage map, not a recommendation. The headline finding, on which everything converges: **no single existing architecture satisfies all twelve characteristics, and the triad you flagged (6 + 8 + 10) is genuinely the least-served combination in the literature — it has to be constructed, not retrieved.** Below I work through each characteristic with candidate mechanisms and citations, mark where one mechanism does several jobs, and — more usefully — mark where satisfying one characteristic damages another. Open questions are surfaced as open. Where there is no fit, I say so.

A framing note before the map. Your "one operation" — *poll → evoke an expected companion/successor bundle → return it → adjust by the discrepancy* — is abstractly a **content-addressable evocation step nested inside a discrepancy-driven loop over a set-valued state**. No existing system is built around exactly that primitive, but it decomposes cleanly into sub-problems that several mature literatures own. Two of those literatures recur as **hubs**: associative-memory/vector-symbolic algebra (covers the part-whole and set-valued side), and predictive-coding/active-inference dynamics (covers the loop, the priming, and the command-as-prediction side). Most of the design tension is between them.

---

## Per-characteristic mapping

### 1 — Wave-bundling (one embedding per cortex per wave; co-arrival = co-occurrence; no finer timing)

This is a **set-valued, permutation-invariant state assembled at a fixed rhythm**, with binding-by-membership rather than binding-by-fine-timing.

- **Vector Symbolic Architectures / Hyperdimensional computing** are the most direct fit. The **bundling (superposition)** operation is commutative and unordered — exactly "no finer time within a wave" — while **binding** can tag *which cortex* a slice came from without imposing temporal order (Plate, *IEEE TNN* 1995, Holographic Reduced Representations; Gayler 2003; Kanerva 2009, hyperdimensional computing; Smolensky 1990 for tensor-product binding). A bundle is then $B_t = \sum_i \text{bind}(\text{role}_i, x^i_t)$.
- A **direct-sum / typed product representation** $X^1 \oplus X^2 \oplus \dots \oplus X^N$, where each slice stays in its native space, preserves the "no shared space" constraint even more cleanly than VSA does — at the cost of being a construct rather than a named architecture.
- The **global workspace** (Baars 1988; Dehaene & Naccache 2001) is the structural analogue of your central unit that "never touches the world, only sees and sends summaries" — a central collection-and-broadcast stage. It supplies the *architecture* but none of the association, decay, or learning.

**Tension flag (1 vs 2/3):** wave-quantization deliberately *discards* the within-window microstructure that spiking/STDP and reservoir methods mine for predictive power. Those can run *inside* a cortex but cannot supply the central operation's timing.

**Caveat on a tempting grounding:** it is easy to reach for *binding-by-synchrony* (von der Malsburg 1981; Singer 1999) to justify "co-arrival = co-occurrence." This is scientifically contested (Shadlen & Movshon 1999; Ray & Maunsell 2010 show gamma synchrony is stimulus-dependent and a poor binding tag). **Wave-membership tagging (VSA roles) is the sounder grounding**; don't lean the spec on synchrony as if it were settled.

---

### 2 — Cued calling-forth within-wave (given part of a bundle, evoke the rest)

This is **pattern completion / hetero-association over a set**.

- **Hopfield networks and modern/dense associative memories.** Classical Hopfield (1982) completes from partial cues via attractor dynamics, but its capacity is too low. The modern/dense variants (Krotov & Hopfield 2016; Demircigil et al. 2017; Ramsauer et al. 2020 for the continuous-input generalization) sharpen the energy function to give super-linear capacity and single-step retrieval over continuous embeddings — directly relevant to your vector summaries. Millidge et al. 2022 ("Universal Hopfield Networks") give a neutral skeleton: *similarity → separation → projection*, i.e. "given part, call forth rest."
- **Sparse Distributed Memory** (Kanerva 1988): partial-cue completion in high-dimensional space, intrinsically noise-tolerant — which matters for characteristic 8.
- **Bidirectional / hetero-associative memories** (Kosko 1988): these associate vectors *across distinct spaces* without collapsing them — a better fit than common-latent methods for your "each cortex keeps its own space" constraint.
- **VSA unbinding + cleanup**: recover a missing slice by binding with the cortex tag's inverse, then cleaning up against an item store.
- **Hippocampal CA3 pattern completion** as the biological exemplar (Marr 1971; Treves & Rolls 1994).

**Multi-characteristic hub:** dense associative memory simultaneously serves **2, 3, 5** (confidence as basin geometry — below) and partly **9**. This is the strongest single-mechanism hub on the perceptual-completion side.

---

### 3 — Cued calling-forth across-wave (current bundle → likely successor)

This is **hetero-association in time / sequence prediction**.

- **HTM / sequence memory** (Hawkins & Ahmad 2016) is arguably the closest *online* fit: high-order next-step prediction over sparse distributed representations, learned continuously with local rules — serving 3, 4, 7 together, on sparse codes relevant to 8.
- **Latent recurrent state-space (world) models** — Ha & Schmidhuber 2018; Hafner et al. 2019 (PlaNet/RSSM), 2020 (Dreamer) — implement "given current latent state, evoke next latent state." But they split observation-model from transition-model and are trained offline, which collides with the open question below and with characteristic 7.
- **Reservoir / echo-state / liquid-state machines** (Jaeger 2001; Maass et al. 2002) carry recent temporal context; readouts evoke the likely next state.
- **Successor representation** (Dayan 1993; Stachenfeld et al. 2017) represents expected *future occupancy* rather than only the next state — a natural bridge to growing reach (11).
- **Predictive coding in generalized coordinates** (Friston & Kiebel 2009) yields successor prediction within one generative loop.

**Open-question flag (2 vs 3 — kept open):** the associative/VSA families *unify* 2 and 3 as one hetero-association whose cue and target differ only by wave index; the world-model families *split* them (observation vs transition model); HTM unifies them via one sequence-memory machinery. **No evidence forces either reading.** (One panel view leaned toward "same mechanism" on HTM/PC grounds — I am explicitly declining to close it, per your instruction.)

---

### 4 — Tracing (called-forth bundle becomes the next cue → multi-step chains, unprompted)

This is **closed-loop autoregressive rollout in the association space**.

- **Iterated attractor transitions / asymmetric-weight chains** (Sompolinsky & Kanter 1986) and **heteroclinic / metastable sequences** (Rabinovich et al. 2008): the current state cues the next, one step at a time — the parsimonious "same operation iterated" reading.
- **Reservoir free-running dynamics** (Jaeger 2001; Sussillo & Abbott 2009, FORCE).
- **Latent imagination / rollout** (Ha & Schmidhuber 2018; Dreamer) does this, but as a distinct generative act.
- **Hippocampal replay / preplay** (Foster & Wilson 2006; Diba & Buzsáki 2007; Dragoi & Tonegawa 2011) as the biological exemplar of self-generated chains.

**Tension flag (4 vs 11, and the silent-swap warning):** iterated single-step evocation drifts off-manifold after a few steps unless the space is well-shaped — *this is the practical ceiling on how far reach can grow*. Note that Dreamer is robust to horizon length precisely because it adds a separate **value model** to estimate returns beyond the imagination horizon. That is a horizon-extension *module* bolted on, exactly the kind of silent architecture swap your central open question exists to catch. If reach is to grow as "the same operation maturing," prefer iterated single-step whose forward range extends because the space is better-shaped — not a switch from reactive correction to a trained rollout-plus-planner.

---

### 5 — Strengthening by recurrence (confidence as a graded property of the evocation, not a stored score)

The "no separate scalar score" clause is sharply discriminating.

- **Energy-based associative memories satisfy this natively.** A frequently-written pattern deepens and sharpens its basin; retrieval is more confident because the attractor is steeper and convergence cleaner. Confidence *is* basin geometry / convergence speed, not a number stored beside the association (Hopfield 1982; Amit 1989; Krotov & Hopfield 2016).
- **Hebbian / fast-weight strengthening** (Hebb 1949; Oja 1982; Ba et al. 2016): repeated co-activation raises efficacy, so the evocation's amplitude/speed encodes confidence.
- **SDM counter magnitude / reconstruction margin** (Kanerva 1988).
- **Predictive-coding precision** (Feldman & Friston 2010) is graded confidence emerging from the dynamics — *but* precision is often implemented as a parameter, which risks being exactly the "separate stored score" you forbid. **The ontological line between "graded property of the evocation" and "a precision parameter" is not sharp in the literature — flag this as something you must decide explicitly, not inherit.**

**Multi-characteristic hub:** basin-geometry sharpening gives 5 *and* is structurally identical to the substrate for 2/3/9 (basin shape = the association).

---

### 6 — Weakening by disuse, coordinated with controllable drift/decay (fading = dynamics; drift a first-class, cortex-independent parameter)

First leg of the critical triad.

- **Palimpsest memory models** (Nadal, Toulouse, Changeux & Dehaene 1986; Parisi 1986) are arguably the *most native single mechanism* here: memory that intrinsically overwrites old with new and is recency-biased by construction — fade-as-dynamics, favour-recent, no deletion step. These deserve a closer look than they usually get.
- **Decaying Hebbian / fast-weight traces** with an explicit decay constant $W_{t+1} = (1-\lambda)W_t + \eta \Delta W_t$, where $\lambda$ is a single first-class parameter independent of any cortex's rule (Hinton & Plaut 1987; Ba et al. 2016).
- **Multi-timescale / cascade synaptic consolidation** (Fusi, Drew & Abbott 2005; Benna & Fusi 2016): *needed* so that decay (6) coexists with recurrence-strengthening (5) without erasing consolidated material. Single-rate decay gives recency but kills often-recurred associations; **6 must be a consolidating, multi-timescale decay, not a single rate.**
- **Homeostatic plasticity** (Turrigiano et al. 1998) for relative-influence loss without deletion.

**Tension flag (6 vs 5, and 6 vs continual-learning):** the anti-forgetting literature (EWC, Kirkpatrick et al. 2017; synaptic intelligence, Zenke et al. 2017) is built to *prevent* the exact fading you want — useful for stability, directly opposed to disuse-fade unless reworked into controlled decay. Complementary Learning Systems (McClelland et al. 1995) likewise tends to *preserve* old associations.

---

### 7 — No phase separation (every wave both uses and adjusts; no train/run split)

- **Online local plasticity**: STDP/Hebbian rules update while running (Bi & Poo 1998; Song, Miller & Abbott 2000). HTM is explicitly continual, no train/test split (Hawkins & Ahmad 2016).
- **Adaptive Resonance Theory** (Carpenter & Grossberg 1987): stable online category learning with no batch phase — and its vigilance mechanism re-appears under 8 and 9.
- **Online predictive coding / active inference** (Rao & Ballard 1999; Friston 2005): inference (use) and learning (adjust) under one continuously-evaluated objective.
- **Fast weights** as the canonical adjust-while-running substrate.

**Sharpest breakage in the whole map (7 vs 3/4/11):** RSSM/Dreamer — your strongest fit for sequence evocation and reach — is trained in a *separate optimization phase* by backpropagation through imagined rollouts. The mechanism that best satisfies 3/4/11 most cleanly violates 7. Candidate reconciliations: online/continual world-model learning, predictive-coding dynamic models (local and online but weaker at long-horizon rollout), or HTM (online but representationally thinner). Note also: a slow-learning/fast-inference *timescale* split in some predictive-coding accounts is **not** the same as a train/run split — handle that distinction carefully rather than rejecting PC on it.

---

### 8 — Tolerance of a moving/drifting space (associations stay usable as vectors shift; favour recent material)

Second leg of the triad. Two literatures:

- **Neuroscience of representational drift + stable readout.** Fixed stimuli and learned tasks show population codes that reconfigure over days while behaviour stays stable (Ziv et al. 2013; Driscoll et al. 2017; Rule, O'Leary & Harvey 2019; Deitch, Rubin & Ziv 2021). The "self-healing code" result (Rule & O'Leary 2022) is the **existence proof your triad needs**: a downstream readout *can* track a continually reconfiguring upstream code via Hebbian/homeostatic adaptation, sometimes without an explicit error signal.
- **Adaptive-prototype systems** — SOM (Kohonen 1982), Growing Neural Gas (Fritzke 1995), Grow-When-Required (Marsland et al. 2002), ART (Carpenter & Grossberg 1987): prototypes track moving distributions online.
- **Recency bias is automatic** in any decaying associative substrate (fast weights, reservoir fading memory), which is why 8's "favour recent" and 6's decay couple naturally.

**Tension flag (8 vs 2):** fixed attractors are robust to *noise* but not to *systematic coordinate drift*; they need moving basins / online plasticity, and drift-tolerance bought through redundancy can blunt sharp within-wave completion (2).

---

### 9 — Refinement by splitting (coarse association divides into finer ones, no global rebuild)

- **ART with vigilance control** (Carpenter & Grossberg 1987) is one of the most apt fits: raising vigilance splits a broad category into finer ones — *ball → red-ball, green-ball* — incrementally.
- **Growing Neural Gas / Grow-When-Required** (Fritzke 1995; Marsland et al. 2002): insert units locally where representation error is high.
- **HTM context-specific minicolumn cells**: the same SDR represented by different cells in different contexts — effectively splitting an association without rebuild.
- **Nonparametric Bayesian models** (Teh et al. 2006, HDP) grow complexity with evidence — but the explicit structural inference can read as a *distinct* operation, worth flagging against your one-operation lean.

**Tension flag (9 vs 5/6):** splitting redistributes "confidence mass." A naive energy model lets a newly-split fine basin cannibalise the parent's depth, and decay (6) can erase the rarer child (green-ball) before it consolidates. This couples 9's splitting schedule to 6's decay schedule and 5's consolidation.

---

### 10 — Native-slice consumption (modality-agnostic; whole bundle evoked; command/prediction lives in the cortex)

Third leg of the triad — and the cleanest conceptual anchor is the active-inference stance that **motor output is just another prediction**.

- **"Predictions not commands"** (Adams, Shipp & Friston 2013): in hierarchical active inference, motor signals are processed in analogy to perceptual signals. This is *exactly* characteristic 10 — the centre emits one expected bundle; a motor cortex treats its slice as a target to fulfil (the command), a sensory cortex treats its slice as an expectation to test (the prediction), and the central process is blind to which is which. **No other family has already committed to "command and prediction are the same kind of object."** Ideomotor / Theory of Event Coding (Prinz 1997; Hommel et al. 2001) is the cognitive-science cousin — though "common coding" risks collapsing the native spaces, so use it carefully.
- **The "blind to which is which" requirement** is met by VSA/Hopfield evocation: the evoked bundle is just a vector; each cortex's tag/slice is interpreted locally. The whole-bundle-at-once requirement favours the **superposition/attractor** read over an autoregressive per-slice decoder.
- **Bidirectional/hetero-associative memory** (Kosko 1988) associates across *distinct* spaces without a common latent — the right shape for native slices.
- **Resonator networks** (Frady, Kent & Olshausen 2020) are the most targeted recent tool for *factorising multiple superposed factors out of one bundle* — i.e. recovering each cortex's slice from the whole. None of the standard families name this; it belongs on your shortlist for the 2/10 "recover each slice from a superposition" problem.

**The load-bearing tension (10 vs common-latent solutions):** every family that solves multimodal integration via a *shared latent cause* (most predictive-coding, world models) helps 2/3/11/12 but threatens the "each cortex keeps its own space" and "central operation modality-agnostic" constraints. The integration story and the own-space story pull against each other.

---

### 11 — Growing reach (early: correction-only; mature: bias perception before arrival; same operation, more reach)

- **Predictive coding gives priming for free**: top-down predictions descend *before* input arrives and pre-shape lower-level activity (Rao & Ballard 1999; Kok, Jehee & de Lange 2012; Summerfield & de Lange 2014; Bar 2007). Increasing reach = the generative model's dynamic order/horizon deepening while the *operation* (minimise discrepancy) is unchanged — the best fit for "same operation, what grows is reach, shifting from correction to anticipation."
- **Successor representation** (Dayan 1993; Stachenfeld et al. 2017) naturally extends beyond one step.
- **Expected-free-energy / anticipatory active inference** formalises the shift from after-the-fact correction to before-arrival biasing — and supplies the hook toward *surfacing-for-arbitration* that your downstream-action open question requires.
- **HTM** chained predictions and **reservoir rollout** also extend reach as dynamics stabilise.

**Warning you asked for:** "early = correction, mature = priming" is the *same* loop at different horizon/precision settings — but it is *two* mechanisms if early-regime is reservoir-style surprise detection and mature-regime is trained rollout/planning. Flag any design that swaps reactive error for a trained planner across the regimes.

---

### 12 — Coherence as learned, not imposed (cross-cortex mismatch surfaces as error; integration is learned)

- **Cross-modal predictive coding** (Rao & Ballard 1999; Friston 2005; Bastos et al. 2012): each modality predicts and is predicted by the others through the central state, so mismatch *is* the discrepancy that gets minimised — coherence emerges because incoherence is surprising, "not wired in."
- **Bayesian multisensory causal inference** (Ernst & Banks 2002; Körding et al. 2007) is the key nuance: it supports *learned non-integration* — deciding whether two streams even share a cause — which is the correct grounding for "coherence not wired in," versus forced fusion.
- **Hebbian cross-modal association** (Hebb 1949) and **sensorimotor contingency theory** (O'Regan & Noë 2001) as alternative routes.
- **Global workspace** supplies broadcast/routing but *imposes* unity rather than learning it — architecture, not learning story.

**Tension flag (8 vs 12):** drift-tolerance achieved via *compensatory error signals between regions* can *implicitly enforce* coherence — which would make integration a side-effect of compensation rather than something genuinely learned-because-surprising. Watch that the mechanism you use for 8 doesn't quietly wire in the coherence that 12 says must be learned.

---

## The critical triad: can ONE approach satisfy 6 + 8 + 10 at once?

You identified this correctly. Here is the honest answer: **no off-the-shelf architecture does, and the reason is that the three pull in opposing directions.**

- **6** wants the central substrate to have *its own* parameterised dynamics — a space that decays/drifts on a clock the cortices don't control. That argues for an explicit, parameterised association field.
- **8** wants evocation to be *robust to the very drift 6 introduces* — small input shifts must cause small retrieval shifts. That argues for distributed, high-dimensional, similarity-based storage.
- **10** wants evocation to produce *one modality-agnostic vector object*, not a typed structure — arguing against anything that must know which slice is a target vs an expectation.

**The closest constructible candidate** is a fusion: a **sparse, high-dimensional distributed associative store (VSA/SDM-flavoured) with multi-timescale homeostatic decay, drifting in a readout-orthogonal subspace, read by attractor/similarity dynamics that emit whole bundles consumed slice-wise by modality-agnostic cortices.** The components are all real and citable; the integration is not in the literature. Three seams remain genuinely open — and they are exactly where original work is needed:

- **Seam A — 6 and 8 are co-satisfiable *only if* the controllable drift is confined to readout-irrelevant directions** (orthogonal to the stable manifold). The drift literature gives this handle (drift as weight-space diffusion in null-space directions) *and* the warning that empirical drift is **not generally orthogonal** to the read-out manifold (Rule & O'Leary 2022). So this is a concrete, falsifiable design constraint, not a free lunch: constrained-drift = co-satisfiable; uncontrolled drift = 6 and 8 fight.

- **Seam B — decay must be consolidating, not single-rate.** Pure exponential decay gives 6's recency but cannot keep often-recurred material (5) stable under drift (8). The reconciliation is multi-timescale plasticity (Benna & Fusi 2016) plus reactivation/refresh — so 6 couples to 5 and 8 through the consolidation schedule.

- **Seam C — the 10-specific risk: drift degrades clean whole-bundle retrieval.** Dense associative memories enter **spurious metastable states** as pattern separability changes, and a drifting space (8) continuously changes separability — so the very drift wanted for 6/8 *worsens* the single-shot bundle read of 10. The mitigation is to route 10 through a **sparse** distributed store (SDM/sparse coding, Olshausen & Field 1996) where patterns stay separable, rather than a dense one, when drift is aggressive.

There is also a subtle **separate-store residue** to decide consciously: VSA's cleanup item-store and SDM's address decoder quietly reintroduce the very separate store the spec wants folded into the operation. (See the persistence open question.)

**Stated plainly: there is no existing architecture whose single native operation is "evoke a whole modality-agnostic bundle from a set-valued cue over a deliberately drifting, intrinsically-decaying space." The 6+8+10 triad is a real gap in the possibility space and must be constructed.**

---

## Cross-cutting summary

**Two hubs, each covering a cluster:**
- **Dense/modern associative memory + VSA binding/bundling** → covers **1, 2, 3 (under the unifying reading), 5, 9**, and supplies the substrate for the 6/8/10 store. Native strengths: set-completion (2) and confidence-as-basin-geometry (5).
- **Predictive coding / active inference** → covers **7, 10, 11, 12** under one discrepancy-minimising objective. Unique fits: "predictions not commands" (10), cross-modal error (12), precision-and-horizon (5, 11).

**The sharpest breakages (satisfying one damages another):**

| Tension | Mechanism that helps one | …but breaks |
|---|---|---|
| **7 vs 3/4/11** | RSSM/Dreamer offline-trained rollout (best sequence/reach) | no train/run split |
| **8 vs 10** | drift (good for 6/8) | increases spurious metastable states → degrades clean whole-bundle read |
| **6 vs 5/8** | single-rate decay (recency) | erases consolidated/recurred associations |
| **9 vs 5/6** | basin-splitting (refinement) | rarer child decays before consolidating |
| **1 vs 2/3** | wave-quantization | discards sub-wave timing STDP/reservoirs need |
| **10 vs 2/3/12** | shared latent cause (clean integration) | collapses each cortex's own space |
| **8 vs 12** | compensatory cross-region error (drift-tracking) | implicitly *imposes* coherence rather than learning it |

---

## Open questions — surfaced, not resolved

1. **Within-wave (2) vs across-wave (3): one mechanism or two?** *Open.* Associative/VSA/HTM families unify them; world-model families split them. The unification is more parsimonious and more consistent with your one-operation doctrine, but no evidence forces it. (I am explicitly declining to close this even where some grounds point toward "same mechanism.")

2. **Single-step iterated vs distinct trajectory-emitting operation.** *Open, with a warning.* Iterated single-step (tracing) is the parsimonious reading and what HTM/PC/closed-loop reservoirs do. One-act trajectory emission exists (RSSM rollout, heteroclinic chains) but the strongest versions add horizon-extension machinery (value models) — a silent architecture addition. Prefer iterated single-step whose forward range grows because the space is better-shaped, not a swap to trained rollout.

3. **Unit of the called-forth thing.** *Open.* Working assumption (whole bundle) is supported by VSA superposition and Hopfield set-completion. Granularity genuinely undetermined: whole bundle (one vector), per-cortex slice set, or hierarchical bundle-of-bundles. The drift/sparsity analysis slightly favours *sparse whole-bundle* units for 10's blindness requirement.

4. **Where persistence lives.** *Open, but the spec's own logic leans one way.* "Confidence is a graded property, not a stored score" (5) and "fading is dynamics, not deletion" (6) both argue that **associations ARE the memory** — folded into the operation's structure (energy landscape / fast-weight field / drifting manifold). The one place a separate store sneaks back in is the **VSA cleanup dictionary / SDM address decoder** — decide that explicitly.

5. **Downstream arbitration extensibility.** Predictive coding/active inference satisfies your "must be able to extend toward priming and arbitration" requirement, because the same machinery already separates perceptual updating from preference/action selection (expected free energy). A pure early-surprise reservoir or a bare auto-associative completer does **not** extend this way — flag any such mechanism as a dead-end even if it wins the early predictive task.

---

## Honest gaps (where I won't force a fit)

- **Asynchronous cortex rates vs a fixed central wave.** The spec says each cortex runs "at its own rate," but no surveyed mechanism addresses the *resampling/aliasing* problem of a fixed-rhythm central poll over peripherals emitting at different rates — what sets wave duration relative to per-channel dynamics. **Neural ODEs / continuous-time recurrent dynamics** (Chen et al. 2018; Beer 1995) are the natural substrate for variable-rate continuous operation but are barely developed for this role. This is an under-served corner.
- **Capacity/scaling under continual drift.** No literature gives bounds on how many whole-bundle associations survive a given decay rate and drift speed. You will need to characterise this empirically.
- **The 6+8+10 triad itself**, as detailed above — a genuine open design space, not a solved pattern.
- **Operational metrics.** How you would *test* whether a built system exhibits each characteristic (measuring reach-growth, drift-tolerance, fade) is absent from all the source literatures and worth specifying alongside the design.

If it would help, I can next (a) write the fused 6+8+10 mechanism as an explicit update rule with its two null-space/consolidation constraints made formal, or (b) build the full 12×12 tension grid marking synergy/conflict for every pair.