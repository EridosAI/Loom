---
id: REVIEW-P-SPECIFICATION-2026-09-20-DESIGN-CHAT
revision: v0.1
authority_status: assistant-review-not-jason-decision
work_status: ready-for-jason-review
evidence_status: source-review-and-analytical-deductions-not-organism-experiment
---

# P specification: design-side review

**Prepared:** 2026-09-20.  
**Reviewer:** primary design Chat, Astra.  
**Reviewed session:** `2026-09-20-p-specification-83a00674`.  
**Disposition:** retain P and the proposed data flow. The two reading documents are a useful first engineering-build target, subject to Jason accepting the proposed completions and separately authorising the build. Do not treat the numerical annex as a commissioned developmental configuration. No new architecture search, P–R merger or reconsideration of D1–D3 is recommended.

This is a review contribution, not an amendment, configuration acceptance, implementation authorisation, commissioning protocol or run instruction. Preserve the original specification and walkthrough. The numerical calculations below evaluate their stated formulas; they are not a simulation or experimental observations.

## 1. Sources and access

Read the supplied merged-reference Current State first. Read the complete implementation specification, complete plain-language walkthrough and complete P parent, with the D1–D3 handoff and relevant accepted world/body sections. Read the completion report, integration-change record and validation record. This review does not re-audit all historical experiments, inspect the Windows workbench, verify its live navigation or reproduce its local link/export checks. No remote-main check was performed.

Source identities were recomputed from the attached bytes:

| Source | Bytes | SHA-256 |
|---|---:|---|
| `P_IMPLEMENTATION_AND_OBSERVATION_SPEC_v0_1_REVIEW_DRAFT.md` | 68773 | `f1af7cf234e15c0215848c5775d7f84c2d8edbeea389dce53b889b1cfa9c64ba` |
| `P_PLAIN_LANGUAGE_DATA_FLOW_v0_1_REVIEW_DRAFT.md` | 32906 | `c31218c3f65bb4e5d35d02a9030978c25504f3d93a7a95682e2255d701d8294b` |
| `LOOM_ASSOCIATIVE_REGULATORY_CANDIDATE_v0_1_DISCUSSION_DRAFT.md` | 38379 | `34bd519bb01253f783521204c9e6358b11703282ec322f4707e5ece1bb6a4da4` |
| `LOOM_P_SPECIFICATION_HANDOFF_2026-09-20.md` | 21878 | `c133f2114a1b41254c5965f61ae202c9b198733173bdc9e9d8193164be12be33` |
| `COMPLETION_REPORT.md` | 5013 | `78abc6f4ec1030254d28f6bb82d2f490777c01cc154aa02ca5cf6591d6b42196` |
| `VALIDATION.json` | 6328 | `a435990afec7a69c3a15e15fbe1b19fb92eac020511bd8d2a1b2dcaeac5b51d9` |
| `INTEGRATION_CHANGES.json` | 2849 | `e0c86e614773ff3b21910d76209d3868e8a666c977014589d9e9ad53c1b67bfb` |

The uploaded P parent matches the commissioned exact-parent identity. This does not independently verify the other session's checkpoint-recovery procedure. The separately linked decision note and updated research map were not uploaded for this review; acceptance itself is available in the current conversation and the exact handoff.

References below use these basenames and section numbers, which are portable even when the exported workbench-relative links cannot resolve.

## 2. What the specification preserves

The substantive operation remains P, not a covert P–R combination:

- Receptor-local activity and local weight formation use actual transduced inputs; association does not supply a visual reconstruction target.
- The mean-plus-endpoint sensory packet is retained. R's antisymmetric temporal packet, reciprocal map constraint and additional regulator inputs are not installed.
- Association writes actual packet/context coactivity once per physical wave. Internal relaxation has no next-wave target and creates no additional external observations.
- Current support regulates a specified direct-query route, not every route from that sensory channel. Other-channel gates use ungated actual input.
- The same group support reduces fine-residual coarsening. Useful common group activity does not certify useful fine differences.
- The regulator receives full evocation plus actual separate energy/integrity. Its two consequence-learning banks remain separate, with P's supplied output superposition.
- Actual applied regulation enters later association. Recalling regulation is not identical to performing it.
- Motor commands go through the physical body. Recalled replenishment cannot change reserves.
- D1 keeps current regulation, lasting associative/regulatory change and useful lasting sensory change distinct.

**Sources:** Specification §§2–7 and 11; walkthrough §§1–3 and 5; exact P §§3–9; authority handoff §1.

The dimensional counts check: 82 packet coordinates, 164 central coordinates, 224 directed context-specific maps and 88,608 map coefficients. Two groups of four sensory units per channel instantiate P's allowed one-level case; this is not an implementation of the fuller eventual hierarchy.

The handoff timing is clear. Old controls generated the completed interval. Old maps are read before a single new write. Prior perturbations receive the new bodily trend before new perturbations are drawn. New sensory support changes the coarsening spring immediately in the ensuing interval and the direct query only at the following handoff. The prose and equations preserve these distinctions.

No new conceptual contradiction was found that requires abandoning P or importing a different mechanism. This is not a proof of developmental adequacy or exhaustive numerical correctness.

## 3. Three numerical choices that materially define this first organism

### 3.1 Fading associative activity is a real, narrower capability choice

Specification §4 proposes a Frobenius bound of 0.10 for each directed context map, four branches with nonnegative coefficients summing to one, and seven source channels per target. Under fixed maps, gates and input, the return operator therefore has block-norm Lipschitz bound at most 0.70.

The activity sweep uses:

$$
\alpha=1-e^{-0.25}\approx0.2211992169.
$$

Consequently, differences between two activity states under the same frozen query contract by at most

$$
c=1-\alpha+0.70\alpha\approx0.9336402349
$$

per sweep, and by at most $c^4\approx0.7598331497$ per 0.2-second handoff. Twenty sweeps, corresponding to one second under this fixed-query assumption, leave at most 0.253274 of the initial activity-state difference. Sixty sweeps leave at most 0.016247 after three seconds.

These are conditional norm bounds, not measured decay trajectories. A changing body, input, gates and learned weights do not satisfy the frozen-system comparison automatically. The five-second context trace and the learning processes are separate states.

With zero query and fixed maps/gates, zero associative activity is the unique attracting equilibrium in this regime. With a cue, learned weights can still call forth related content. Persistent memory in weights is not abolished by fading transient activity.

**Recommendation:** acceptable as an explicitly limited first engineering instantiation of P, if Jason accepts that scope. Do not describe it as unrestricted internally self-sustaining imagination or treat lack of that behaviour as an unexpected failure. Do not raise the bounds silently to obtain richer activity. P itself permits this restrictive regime; it is not a departure merely because a later candidate could relax it.

### 3.2 Sensory adaptation changes availability, not only learning speed

Specification §§3 and 10 set a 30-second receptor mean and a 60-second packet mean. For a step followed by a constant receptor input, the receptor residual alone obeys

$$
r(t)=r(0)e^{-t/30}.
$$

It is approximately 36.8% of its initial residual after 30 seconds and 5.0% after 90 seconds. These percentages are not a bound on the entire packet, which also depends on recurrence, weights and later centring.

The important point is that this pathway increasingly emphasises change relative to a baseline. It is not a uniformly available representation of the current raw sensory level. The raw inputs are still recorded; the memory weights can persist; direct bodily and raw motor-feedback routes remain. But the regulator does not have a raw light/chemical bypass, and the positive query floor cannot restore a distinction removed upstream.

**Recommendation:** keep P's declared route for the first engineering implementation rather than silently adding a tonic channel. Explicitly inspect persistent as well as changing sensory conditions during later authorised commissioning. If a required distinction is unavailable on every legitimate route, propose a named revision rather than attributing the failure automatically to weak learning. This is not a renewed demand to solve every ambiguity before building.

### 3.3 Small initial signals can make the associative route operationally negligible

Specification §10 combines sensory shared-row norm 0.05, tiny fine residuals, zero initial H, map-learning rate $10^{-4}/\mathrm{s}$, a 0.10 map cap, and fixed small projections of q into regulator features. The direct actual-body input remains available even if association contributes very little.

The maximum-coordinate update bound in the specification is an overflow/scale ceiling, not evidence of typical signal strength.

For an explicitly hypothetical scalar component, take two packet/context coordinates with sustained product $0.05\times0.05$, gate 0.25, zero initial map weight, and ignore decay. Its map write accumulated over 600 seconds is only

$$
10^{-4}\times0.25\times0.05\times0.05\times600=3.75\times10^{-5}.
$$

Under constant unused-map decay 0.0011/s, the continuous-time analogue would instead give about $2.7452\times10^{-5}$. Neither is a simulated P trajectory. Actual signals vary; maps have many coordinates and paths; their effects can accumulate or cancel. The example simply shows why a norm cap is not the same as an achieved return strength.

**Recommendation:** the first engineering/commissioning records should expose actual packet magnitudes, map writes/decay, returned q, $B_q q$ versus the separately present bodily/bias contribution, learned versus exploratory regulatory output, and local-formation versus spring/reference terms. Most operands are already in the record contract and can be calculated offline. No new learner input, success score or automatic gain-tuning rule is needed.

Do not require learning success in order to accept the code. Do require the implementation to make it possible to distinguish an inadequate learning hypothesis from a numerically negligible pathway. Any calibration change remains a recorded proposal, not a rescue performed inside a life.

## 4. The body/world proposal is coherent in scope, but recovery has a substantial cost

The square, eight persistent identical sources, three wall-restorative bodies, one fixed-track mover and shared small material palette remain compatible with the accepted functional choices. A regular layout is not itself disallowed. The prescribed mover remains autonomous rather than responsive to the creature. **Source:** specification §8.1; Base World §§2–5 and 9.

The proposed chemical law is a clear realization of solid-aware transport: diffusion is reduced inside solids, not eliminated, and chemistry is not advected with the body. Pre-evolution uses the selected mover phase and the same field law; the organism is inserted without resetting concentration. This is an explicit preparation history, not a claim that a stationary equilibrium was attained. **Source:** specification §8.4.

The source accounting also preserves the intended distinction between finite startup stocks and renewable support. Maximum replenishment is $0.20/400=0.0005$ reserve/s per source, less than basal expenditure 0.0015. The eight-source sum of maxima is 0.004, which does not prove the body can harvest that rate. **Source:** specification §8.2.

### 4.1 No-intake energy runway

With birth energy 0.70 and $|u_i|\le1$:

$$
0.0015\le P_E\le0.0025.
$$

Therefore the time to energy exhaustion with no intake lies between 280 and 466.6667 seconds, conditional on no earlier integrity termination. The 600-second administrative horizon is longer than this no-intake interval; reaching it while physically viable would require actual uptake. This is not an evidential survival threshold.

At 280 and 466.6667 seconds, the private opening state $o=1-e^{-t/300}$ is approximately 0.6068 and 0.7889 respectively. At 600 seconds it is approximately 0.8647. The chosen life-scale and opening-scale are therefore materially linked. None of these values proves that useful fine structure has formed.

### 4.2 Best-case repair bound

For zero relative surface speed and a single gently loaded repair contact, the specification's contact factor is

$$
Q(F)=\frac{F}{F+0.1}\left(1-\frac F{0.25}\right),\quad 0\le F\le0.25.
$$

Its maximum occurs at

$$
F_*=\sqrt{0.1(0.1+0.25)}-0.1\approx0.08708287,
$$

and $Q_{\max}\approx0.30333705$. Taking the maximum across contacts cannot exceed that value. Motion reduces it further.

Since $\dot I=0.02(1-I)Q$ in damage-free repair, halving an existing integrity deficit takes at least

$$
T_{1/2}\ge\frac{\ln2}{0.02Q_{\max}}\approx114.2536\ \mathrm{s}.
$$

Even basal expenditure alone over that interval consumes at least 0.1713804 reserve units, before actuation and travel. The bound assumes no coincident energy intake, no additional damage, and ideal sustained contact. The proposed layout separates energy bodies from repair surfaces.

This does not prove the repair ecology is impossible. Partial repair may be sufficient, the body can arrive well supplied, and the candidate may learn suitable contact. It does show that “gentle repair” is a long and energetically significant interaction in this proposed numerical world, not a quick touch.

**Recommendation:** retain the formula as a proposed physical hypothesis, but make its force dependence and energetic timescale explicit in the plain-language account. Later commissioning must inspect damaged-state contact, useful partial repair, departure and return to energy. Avoiding damage perfectly is not a check of repair. No new arbitrary recovery percentage or pass/fail bar is proposed here.

The bodily trend/eligibility pair (two and five seconds) need not span the entire repair interval: repair can produce ongoing bodily changes while contact is maintained. The harder case is costly travel whose relevant benefit arrives much later. Do not confuse those two credit situations.

## 5. Engineering ambiguities should be closed explicitly, not disguised as new research

The specification already says the eventual build must name its runtime and contact-solver tolerances/order. That is a bounded engineering obligation, not another architectural fork. It remains incomplete until those choices are recorded.

The build manifest should also spell out:

- the exact seed serialization (including the representation of the hexadecimal master seed, field order and omission of the life field for anatomical streams);
- the conversion of the 64-bit digest integer to binary64 and endpoint handling; $(n+0.5)/2^{64}$ is interior in exact arithmetic but can round to 1 in binary64 near the upper end;
- geometric/time-of-impact precision, simultaneous-contact ordering, field residual norm/zero-right-hand-side convention, and shortened terminal-step convergence/failure handling;
- explicit configuration-field names for recycled symbols, plus the exact motor block selection.

These details should be fixed in a recorded implementation annex and covered by engineering checks. They do not justify changing learning laws or silently importing another candidate. They do not require a separate extended human decision for every tolerance if a bounded completion task is explicitly authorised.

## 6. Plain-language walkthrough assessment

The required walkthrough materially succeeds: it traces source-to-recipient data, distinguishes supplied anatomy from learned organisation, and repeatedly separates a hypothetical good outcome from what the equations actually ensure. Its handoff table aligns with the specification's read/write order. **Source:** walkthrough §§1–5.

Small additions would make the impending review easier:

1. Add a short “what this exact first creature is” opening: four eight-unit learned sensory cortices, native 100 Hz activity, 5 Hz packet handoff, fixed mixed context anatomy, fading cue-driven association, learned 12-output regulation and no mature motor hierarchy or episodic store.
2. State the numerical meanings of “fading,” “adapting” and “slow repair” from §§3–4 of this review with their assumptions. These are consequences of proposed settings, not proofs of real trajectories.
3. Describe the competition term as *intended to discourage redundancy* rather than as a guaranteed differentiator.
4. Explicitly distinguish a four-computation associative handoff from four remembered future moments, and contrast fading activity with persistent H weights. The draft already gives the first distinction; the second deserves equal prominence.

No full rewrite is needed. Adding these explanations does not authorise changing the formulas.

## 7. Disposition and next authority

### Retain for the first engineering target

P's unchanged learning/return laws, one-level anatomy, defined packet/block choices, read-before-write timing, separate bodily credit, actual-regulation channel, explicit physical accounting, finite-permeability field model, truthful state records and synchronized visual inspector.

### Treat as proposed initial settings, not scientific adequacy

The fading associative regime, signal amplitudes/rates, sensory adaptation, repair law/time, birth reserve, layout, 600-second administrative bound and all other numerical annex values. Their uptake into a build needs Jason's acceptance; their suitability requires separately scoped commissioning. Acceptance for construction does not freeze an evidential experiment or grant adaptive tuning permission.

### Keep genuinely empirical

Whether the local sensory rule provides useful provisional differences; whether the associative maps are rich enough; whether the regulator learns useful participation; whether group-level use protects useful fine structure; whether repair and travel can be discovered; whether gains are chiefly body-only habits or lasting sensory contribution. Do not demand that these be settled before constructing the specified candidate.

**Recommended next decision:** accept the two reading documents, with the small explanatory/engineering annex above, as the exact target for a bounded engineering build. This is a recommendation, not an action already authorised. A subsequent build commission should enumerate implementation, deterministic component/contract checks and UI smoke scope, require return of the pinned code/configuration and verification report, and stop before unrestricted commissioning or scientific lifetimes.

No reapproval of D1–D3 is needed. No P–R synthesis is required. R and all other alternatives remain preserved. No organism code, world simulation, commissioning, experiment identifier, preregistration, scientific run, Git operation, remote repository change or local workbench write was performed by this review.
