# MOTOR COMMISSIONING PREPARATION — M1 / M2 v0.1

**PREPARED, NOT EXECUTED. No candidate selected. Separate Jason authorization is required.**

The fixed comparison is the original FS-001, FS-002 and FS-003 birth states crossed with CURRENT, M1 and M2, each with a 90-second ceiling. It compares temporal organization and its bodily consequences. It does not test developmental efficacy or initiate Founder Search or Nursery-0.

The ordinary uniform-rejection birth law is retained. No fresh birth, prehistory, world case, learning handoff or organism loop ran. Standalone motor/regulator components were exercised with manufactured inputs; preserved current records were read, and scalar distribution integrals were evaluated. This distinction is explicit: “no simulation” does not mean “no component calculations.”

## 1. Exact process laws

Let $c$ be common drive and $d$ differential drive. Both candidates supply only the old spontaneous summand:

$$o_L=0.35\tanh(c-d),\qquad o_R=0.35\tanh(c+d).$$

The predeclared latent scale is $\sigma=0.5$ for each independent coordinate. **Common mean is zero**. There is no forward bias, source input, reward, target coordinate, place memory, movement-magnitude correction or outcome-dependent normalization. The final spontaneous term remains within the current generator's $[-0.35,0.35]$ envelope.

### M1 — correlated common/differential drive

At each 0.5-second refresh after birth:

$$c_{k+1}=a_c c_k+0.5\sqrt{1-a_c^2}\,\xi_{c,k},\quad a_c=\exp(-0.5/16),$$
$$d_{k+1}=a_d d_k+0.5\sqrt{1-a_d^2}\,\xi_{d,k},\quad a_d=\exp(-0.5/8).$$

The innovations are independent standard Gaussian coordinates. At birth, $c_0,d_0$ are independent $N(0,0.25)$ draws, so the latent marginal is stationary immediately. This chooses Gaussian innovations from the earlier unspecified continuous family. The latent values have no hard bound; the spontaneous output does. No claim of bounded latent innovations is made.

Each spontaneous value is held between refreshes. At native tick 50, 100, … the new latent applies before that tick's command calculation. Tick zero uses the birth draw and consumes no innovation. The $\sqrt{1-a^2}$ term is a fixed analytical stationary-variance coefficient, not adaptive magnitude balancing.

### M2 — smooth tendencies, irregular renewal

At birth and each renewal, draw independent targets $C,D\sim N(0,0.25)$ and an independent integer $N$ uniformly from $\{8,9,\ldots,24\}$. The next renewal follows $N\times0.5$ seconds later: 4–12 seconds, mean 8 seconds. Both targets renew together. There is no label for forward, turn, rest or explore.

Between renewals:

$$c(t+\delta)=c(t)+(1-e^{-\delta/1})(C-c(t)),\qquad d(t+\delta)=d(t)+(1-e^{-\delta/1})(D-d(t)).$$

At birth set $c=C,d=D$ using the first target draw and start a **fresh** duration. This is an explicit newborn initialization, not a stationary residual-life claim. It does not force an initial rest, a positive drive or an advantageous direction. The original motor tendency, command and integral still start at their preserved zero values.

The current latent produces the command; the exponential follow then advances over the actual native interval. At a renewal boundary the targets change before this follow, so the spontaneous signal remains continuous and begins responding over subsequent native samples. Scheduling uses integer native ticks; a terminal fractional step uses its actual $\delta$ for the follow and cannot trigger continuation.

### Unchanged motor coupling

For both candidates, the existing motor implementation still computes:

$$z=o+F[\mathrm{proprioception};\mathrm{contact}]+q_m[2{:}4]+i,$$
$$\tau=\tanh(z),\qquad v'=v+(1-e^{-\delta/0.1})(\tau-v),\qquad u=(1-\alpha)v'.$$

Here $F$ is the original anatomical feedback matrix, $q_m$ the existing associative return, $i$ the existing regulatory current and $\alpha$ attenuation. All continue to affect commands every **0.01 s**. The 0.1 s number is the original motor relaxation time, not a human-controller command hold. Wave cadence remains 0.2 s, field cadence 0.01 s, and the original learning, packets, regulator and body mechanics are untouched.

## 2. Why these parameters

| Quantity | Predetermined choice | Outcome-independent ground |
|---|---|---|
| Reference motor period | $(7+9)/2=8$ s | Existing generator periods; the observed roughly 3.4 s body reversal regime is close to a half-period, not a magnitude diagnosis. |
| M1 common correlation | 16 s | Two reference periods: retain a tendency across several reversals of the old regime. |
| M1 differential correlation | 8 s | One reference period: imbalance can wander within a longer common tendency; no directional preference. |
| M2 duration | 4–12 s, in 0.5 s increments | Reference period ± its half-period; broad irregular timing without a deterministic rhythm. |
| M2 follow time | 1 s | Body translation relaxation $m/\gamma=1/1$ s; angular relaxation is $0.125/0.2=0.625$ s; motor relaxation remains 0.1 s. |
| Output envelope | 0.35 | Current maximum $0.25+0.10$; no stronger peak drive. |
| Latent SD | 0.5 each | Per-wheel latent variance 0.5 produces spontaneous RMS 0.1831 under the fixed output transform, close to the existing 0.1827. |
| Refresh clock | 0.5 s / 50 native steps | Existing spontaneous-noise refresh cadence; no new world clock. |
| Common mean | 0 | Preserves bidirectional possibility and avoids an unreviewed forward bias. |

These constants were specified before the current-record comparison and were not revised after it. No candidate-world outcome exists. They are engineering comparison choices, not established optima. Ninety seconds spans 5.6 common correlation times for M1 and about eleven M2 duration intervals in expectation, enough to pose a gross screen but not to establish long-run reliability.

M1's expected sampled latent sign-run lengths are about 6.32 s (common) and 4.49 s (differential), from $0.5\pi/\arccos(e^{-0.5/T})$. M2's target-sign run averages 16 s because each renewal has probability one half of changing a sign. These are **process descriptors, not predicted body bouts**. Actual velocity reversals are affected by the other motor inputs, smoothing and mechanics. Ordinary negative drive, reversals, reorientation and values near zero remain possible; neither family guarantees a rest schedule or long straight path.

## 3. Magnitude and ordinary-effort comparison

The current filtered-sign noise has native-sampled stationary variance 0.213074435. Independent phase and noise therefore give spontaneous variance $0.25^2/2+0.10^2(0.213074435)$ and RMS **0.182703980**. This is an ensemble reference, not an assumption that each short case realizes that mean.

| Process | Spontaneous bound | Stationary spontaneous RMS | Neutral effort-rate proxy |
|---|---:|---:|---:|
| CURRENT | ±0.35 | 0.182704 | approximately 0.00012752 |
| M1 | ±0.35 | 0.183099 | 0.00012402 |
| M2 | ±0.35 | 0.175001–0.175174 | 0.00011776–0.00011790 |

The proxy applies $u=0.8\tanh(o)$ with no direct/associative/current input and before the original motor smoothing, then uses $0.001\,E|u|$. It is a reference for ordinary effort, **not measured candidate expenditure or a closed-loop forecast**. The M2 range comes from stationary renewal-boundary conditional-variance bounds propagated over exact native pre-update ages. Its newborn distribution initially matches M1 and is not claimed stationary.

M1 is about 0.22% above the analytical current RMS; M2 is approximately 4.1–4.2% below. M2's neutral effort proxy is about 7.5–7.7% below the current proxy. The smoothing loss is left intact; no compensation or outcome-adaptive rescaling is applied. Temporal changes can still alter actual effort, contact and damage substantially.

Actual first-90-second reference records, two actuator coordinates pooled:

| Preserved life | Spontaneous RMS | Actual command RMS | Actual mean absolute command | Actual effort loss |
|---|---:|---:|---:|---:|
| FS-001 | 0.18488007 | 0.14689234 | 0.13128710 | 0.01181584 |
| FS-002 | 0.18868155 | 0.14927381 | 0.13296420 | 0.01196678 |
| FS-003 | 0.18291512 | 0.14486086 | 0.12921196 | 0.01162908 |

Basal loss over 90 s is separately 0.135 under the unchanged law. Spontaneous terms were reconstructed only from the prescribed old phase/noise equations and recorded birth stream, with exact phase/noise/drive agreement at the preserved 60 s checkpoint. Commands are the existing native records. No body, field or P trajectory was replayed. Approximate current-distribution absolute moments and their quadrature/tail qualifications are in `AMPLITUDE_EFFORT_REFERENCE.json`; they are not exact-cost claims.

## 4. Component checks and remaining influence

**26 component tests passed.** They cover original motor bit identity on manufactured sensory inputs; both candidates' downstream equations; direct proprioceptive/contact feedback; associative input; additive current across the spontaneous range; full-current-background sensitivity; attenuation; actual legal regulator-bank perturbations; process blindness; reset/reproducibility; stream separation; native refresh/renewal boundaries; terminal fractional component updates; rollback safety; serialization/restart; strict new grant rejection; runner resource/deadline/terminal ownership.

The process receives no sensory, reserve, learned or world arguments. Those inputs continue through the original motor coupling. With only spontaneous drive and the full ±0.5 regulatory-current range, $|z|\le0.85$, so $\operatorname{sech}^2 z\ge0.5224$ before attenuation and motor relaxation. Existing feedback and associative terms may add further saturation; no universal influence floor is claimed under arbitrarily large combined inputs or attenuation approaching one. Full attenuation must still suppress commands. The component results show meaningful available influence, not successful learned use of it.

Learning can oppose or suppress the resulting commands through those existing pathways. It does not edit a candidate's latent drift, correlation time or renewal deadline. This is the previously proposed minimal coupling, not a newly added learned scheduler. M2's fresh-renewal birth transient is part of its declared design; a 90-second comparison cannot isolate stationary temporal statistics from that initialization difference.

Production world/field/organism evolution entry points were blocked during component tests and snapshot preparation. The manufactured terminal test changed only a fake index/time object to exercise runner branching. No candidate-world smoke was run. The original full-world scheduler and terminal root search were reused by source identity, not re-audited through an unauthorized world test. See `COMPONENT_TEST_REPORT.md` and `COMPONENT_TESTS.xml`.

## 5. Matched starts, initial state and streams

Each triplet reuses its exact original FS birth snapshot, including position, heading, mover phase, fields, stocks, body state, anatomy, blank learned state, raw sensory values, source history and original RNG counters. No safety rejection is rerun. The entire original engine is byte-identical under the typed encoding after removing only the new candidate process attribute. `MATCHED_INITIAL_STATE_PROOF.json` records the comparisons and exact initial latent/target/duration/counter values. The original snapshot files remain unchanged.

CURRENT retains its original phase/noise state. Candidate process streams use the existing SHA-256 indexed `Streams` algorithm, original master seed 5284097 and original life IDs 1, 2, 3, in a **separate saved Streams object**. Labels are `motor-screen-v1-m1-initial`, `motor-screen-v1-m1-innovation`, `motor-screen-v1-m2-initial`, `motor-screen-v1-m2-target`, and `motor-screen-v1-m2-duration`. Counters start absent/zero for every case. Exactly one birth Gaussian pair is drawn; M2 additionally draws one duration. There is no seed search or rejection of a process draw.

For Gaussian pairs, two interior uniforms produce $r=\sqrt{-2\log U_1}$, angle $2\pi U_2$, then $(r\cos\theta,r\sin\theta)$. Uniforms follow the original finite-precision SHA stream mapping. M2 uses $N=8+\min(16,\lfloor17U\rfloor)$. Integer tick zero is the original birth. M1 first innovation is at tick 50. M2 first renewal is at tick $50N$; each renewal draws targets and the next duration. Candidate arrays/counters are replaced without in-place mutation of the rollback copy. Full checkpoints preserve all latent/target/tick/RNG state. No continuation is authorized, even though lossless state recovery is component-tested.

Original `motor-noise` draws and old phase/noise bookkeeping continue on the original schedule but do not contribute to candidate spontaneous output. This keeps original stream/counter semantics explicit and leaves the regulatory streams untouched. The candidate RNG namespace never consumes an original anatomical, world or regulatory draw.

## 6. Execution identities and nine proposed authorities

- Frozen P baseline: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`.
- Unchanged lean runner base: `87abae34e19d4e46234402a6b1ba776814956ec1`.
- Frozen P source hash: `63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9`.
- Configuration identity: `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`.
- Prepared runtime + motor-overlay identity: `d1b14d75dc30e2934c76e209e0354ca236ac0115f381b4cbbf5c15093ba9a41a`.
- Parameter identity: `f028166e2a74fd5458176918d66c5038b06014af16851819f54e6924eb8e2aa1`.

This is a content-addressed commissioning overlay in the preparation directory, **not a new canonical P commit**. CURRENT delegates to the original motor. M1/M2 explicitly replace its spontaneous summand; their complete executed organism must not be described as identical to frozen P. P learning/core, body/world/sensor/source laws and all baseline source files remain unchanged. There are no Git writes or commits in this task. The existing code checkout remains on `build/p-developmental-runner-20260929` at the stated base.

The overlay source is in `loom_motor_commissioning/`. Its runner/codec/verification changes versus the frozen lean implementation are supplied as `.diff` files; motor and compact-wave evidence modules are new files. The codec accepts the explicitly identified subclass without editing the original P registry. Runtime identity binds all overlay modules plus the existing numerical distributions, Python native runtime, frozen P and lean modules. Each authority also binds the executor, preflight, path adapter, execution/analysis plans, resources, configuration and original contract.

Every case independently binds its original and prepared all-state snapshots, process, exact initial process state, seed/stream, parameters, 90 s / 9000 native-step limit, evidence policy and resource envelope. These are proposals, not permissions. No historical authority is reused.

| Order | Case (90 s each) | Canonical authority SHA-256 |
|---:|---|---|
| 1 | MC-FS-001-CURRENT | `d21c492ceb73a0c14dc40ba3506226cdba6386c919663a33c823f2ed5ad80d0a` |
| 2 | MC-FS-001-M1 | `e50f8590373c13bd435546eac629ac6f4e7e33d2c99af0cea0e919a433a690b3` |
| 3 | MC-FS-001-M2 | `5cd0ebdd0822ae74384e692dff05298ca35fc3fa6fa16cd6e569cb56dd5e0921` |
| 4 | MC-FS-002-CURRENT | `12b60ec39d1089bf82e758f1799588540e03f765c2a9f36e3ad44d2305847b04` |
| 5 | MC-FS-002-M1 | `3366db2959084dfbc730ae697dd9f5fc13798bf7c6379c614e0ba373389cdf87` |
| 6 | MC-FS-002-M2 | `47d2b7d86b892c770bea678b9e563c701e93ab60cca6a76b403084a89f19224d` |
| 7 | MC-FS-003-CURRENT | `74dc6736aaba1289b21fa55b196d1fe996a2e7cb17922a8d7c969b7fee78d74e` |
| 8 | MC-FS-003-M1 | `8cdf2288a55312e118ada0c25c15b8d9037d7ffc4256c0ee4a0446a0e0c9739f` |
| 9 | MC-FS-003-M2 | `a317a0aa2b15b13d56234b5deb3197737ee9ced0416bdf20c3798ea0e222590a` |

Canonical files are UTF-8 JSON, sorted keys, compact separators and finite numbers only. Hash the exact file bytes. No case substitutes for another. The single-use executor requires a separately recorded Jason instruction containing the exact ordered nine hashes; preparation supplies no approval file. `EXECUTION_PROTOCOL.md` defines preflight and stop behavior.

The inherited recording field `P_endpoint_sha256` hashes the whole recorded organism, including candidate process state when present. Its historical field name is not a claim that an M1/M2 organism is intact baseline P. The complete execution identity is the bound baseline plus overlay, process, state, configuration and runtime.

## 7. Resource envelope and evidence

The 59 completed Founder receipts imply an active linear projection of **281.75 s (4.70 min)** for 810 simulated seconds, with historical-rate range **257.53–850.22 s (4.29–14.17 min)**. Primary evidence projects **61.27 MB**, range **58.95–76.64 MB**, before short-case fixed costs and new compact motor-wave fields. Allow an additional **2 MB/case** for those fields. These are estimates, not candidate benchmarks; contact workload and short-run setup can differ.

Reserve 300 active wall seconds and 32 MB per case, including the runner's 16 MB closure reserve; 2700 s / 288 MB for nine cases. The earlier 25 MB sketch was provisional: 32 MB leaves room for the existing closure reserve, the historical upper recording rate and declared diagnostics. Full-runtime preflight has a separate 300 s total allowance, verification 600 s total, and archive/reporting a 300 s planning reserve: a **65-minute total planning envelope**, not an invitation to extend any case. Require 2 GB free before launch and 1 GB before each case. Native recording is not reduced.

The static full-runtime gate completed in 0.949 s and passed all nine prepared zero-age snapshots. That measured preparation check is not a world-performance benchmark. Before a later launch it must run again against then-current files/runtime. The old FS-060 unclosed interruption remains an unresolved execution-reliability caution; this preparation neither explains it nor silently repairs the runner.

All native physical facts, E/I, commands, position/orientation, actual mover poses, source stocks, raw signals and contact/impulse/transfer/damage ledgers remain recorded. Already-computed motor contributions and small process state are appended at existing waves. Complete checkpoints contain candidate process state. No live renderer, external feedback path or live deep-diagnostic pass is added.

## 8. Review boundary

Judge the eventual screen through the predeclared excursion, coverage, bout/reversal, velocity-persistence, revisitation, displacement/path, cost, contact/damage and motor-coupling observations in `ANALYSIS_PLAN.md`. Source encounters are descriptive only and cannot rank candidates. There is no automatic winner, no useful-learning/survival gate and no authority for extra cases, retries, tuning, continuation or nursery changes.

**Nursery-0 geometry, original uniform-rejection birth law, viability/resilience, repair/source laws, P learning and preserved Founder evidence remain untouched.** The stratified-random proposal remains a later optional cohort-design dial. No world case, new life, new prehistory or learning trajectory executed. Jason's review and separate execution authorization are the next boundary.

## Source trail and status separation

The directly accepted scope is Jason's latest motor-commissioning preparation instruction. Numerical motor constants in this packet are assistant proposals for that authorized preparation; they are not an adopted new canonical motor mechanism. Current-record summaries are observations. Candidate behavior in a world remains unobserved.

The preceding families and interpretation constraints are preserved in `nursery_birth_motor_review_20260930_v0_1/NEWBORN_SPONTANEOUS_MOTOR_DESIGN_REVIEW_v0_1.md`. The uniform-birth evidence is `BIRTH_GEOGRAPHY_AUDIT_v0_1.md` in that same directory. The approximately 3.4 s reversal result and its thresholds are in `nursery_0_design_20260930_v0_1/NEWBORN_EXPLORATION_DYNAMICS_AUDIT_v0_1.md` and `EXPLORATION_AUDIT_RESULTS.json`; the prior layout proposals remain in `NURSERY_CANDIDATE_PROPOSALS.json` unchanged.

Implementation grounds are the original `developmental_ecology/loom_p/neural.py` (Motor, Regulator, Organism), `schema.py` (configuration and Streams), `physics.py` (actuators, expenditure and mechanics), and `loom_developmental/core.py`, `runner.py`, `codec.py`, `evidence.py`, `verify.py` at the bound checkpoint. The exact prior birth/prehistory files and original native chunks used for current-reference moments are hashed in the authority objects and `REFERENCE_INPUT_HASHES.json`. Important inputs and previous deliveries are rechecked in `FINAL_VERIFICATION.json`.
