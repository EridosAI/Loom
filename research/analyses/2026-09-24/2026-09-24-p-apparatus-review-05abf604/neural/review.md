# Independent fixed-structure, D5 and neural-boundary apparatus review

Reviewed apparatus checkpoint: `05abf60401d08f38750bca589b1c040e10513d7b`.
Reviewed P parent: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`.
Target: `C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405`.

No MUST-FIX BEFORE COMMISSIONING defect was found in this bounded scope. This is supporting evidence for the primary review, not a disposition on authority, reconstruction, package custody or other agents' scopes.

The target was read only. This audit used detached neural components, manufactured one-native fixtures and the existing apparatus test definitions as references. No commissioning case, prehistory generation, freely acting life, tuning, or scientific trial was performed. The complete test suites and delivered 16 fault pairs were assigned to the primary reviewer and were not duplicated here.

## Findings and source map

All source references below are in the target's `developmental_ecology` directory.

| Classification | Finding | Exact source lines and independent evidence |
|---|---|---|
| VERIFIED | Frozen structure matches the design exactly: sensory `shared`, `fine`, `shared_ref`, `fine_ref`; association `H`, `use`; regulator `theta`, `reference`. Restoration produces copied arrays, not live aliases of frozen storage. | `loom_commissioning/adapter.py:10–27`; per-family and combined poison checks plus `np.shares_memory` assertions in `independent_checks.py`. |
| VERIFIED | Sensory structural changes cannot affect the native transient RHS or the following read. The existing cortex snapshots activity, effective weights and residual before updating structures, then computes activity from those snapshots. Restoration immediately follows the native call. | `loom_p/neural.py:46–68`; `loom_commissioning/adapter.py:32–37`. All four sensory structural arrays were poisoned after their ordinary update; subsequent causal state and RNG remained identical. |
| VERIFIED | Bank restoration occurs between credit and output, and map/use restoration follows the hypothetical write before the next read. The code preserves ordinary packet centring, traces, body filter, eligibility, four associative sweeps, fresh regulatory draw and packet means. | `loom_commissioning/adapter.py:39–66`; compare `loom_p/neural.py:218–230`. A deliberately late bank restore restored the structural hash but changed controls by `0.07729363526569996`, demonstrating consequential detection. |
| VERIFIED | Structural freeze does not freeze intended transient dynamics. | The 40-native, two-handoff detached synthetic-input sequence changed all 29 named transient fields tested. Sensory/motor integrals accumulated and reset at handoff; native/wave/map-write counts reached 40/2/2. Frozen H/banks remained zero. Exact causal hash for the unpoisoned and all correctly restored variants: `77b57f151a82c52b0e7c49d9a542e1e00e2310545173cab9acf3895c6d4fcca5`. |
| VERIFIED | Discarded updates remain inspectable without a causal route back. Native hypothetical structures and wave credit/map diagnostics are copied; applied structural increments are explicitly zero. | `loom_commissioning/adapter.py:35–37,50–64`; `loom_commissioning/diagnostics.py:73–93`. The discarded diagnostic objects necessarily differ under poison; the comparison excludes only diagnostics, retaining all causal state and the complete RNG object. |
| VERIFIED | The fixed arm has a distinct label and newborn entry constraint. | `loom_commissioning/contract.py:11–13,51–53`; `loom_commissioning/runner.py:51–58,138–141`; `loom_commissioning/adapter.py:63`. No fixed call delegates to the intact label. This does not claim survival or innate competence. |
| VERIFIED | D5 selection is predetermined: every wave, native index divisible by 100, with motor reconstruction also on wave steps. It has no magnitude, error, survival or outcome selector. | `loom_commissioning/contract.py:14,41,59–60`; `loom_commissioning/diagnostics.py:84–96`. Observer-only manufactured indices 1/99/100/101/200 selected false/false/true/false/true; wave selection was present regardless of the native-only rule. |
| VERIFIED | D5 reconstructs baseline outputs first, then removes one declared contribution. Query/context omission and support-to-zero recompute gates, query gains, all four sweeps and final q on detached prior association state. | `loom_commissioning/diagnostics.py:24–60`; `loom_p/neural.py:96–124,164–175`. Independent explicit equations matched all returned regulator baseline/omission features, weighted logits and controls; query/support alternatives were nonzero and matched. Corrupting the recorded baseline q or control vector was rejected by its intended reconstruction check. |
| VERIFIED | Motor receiver reconstruction uses the appropriate old phase, old noise state, old tendency and old attenuation, together with contributions actually used in the native update. Noise-drive refresh does not replace the old `nu` used in the immediate command. Wave output controls do not retrospectively affect that command. | `loom_commissioning/diagnostics.py:9–22`; `loom_p/neural.py:187–197,209–215`. Explicit motor equations matched all baseline/omission target, tendency and command vectors. The strengthened fixture gave all six omissions nonzero command effects. |
| VERIFIED | Detached receiver probes do not evolve a world, consume live random draws, write gains or alter live state. | `loom_commissioning/diagnostics.py:27–30,38–60,64,97`. Complete before/after state hashes, which include RNG state, were unchanged by the observer; the code contains no gain-write path. |
| VERIFIED | Native records distinguish step-start neural input from endpoint transduction. Old means/activity/weights, formation, references, support/opening and signed applied deltas are aligned. Wave packets are actual trapezoidal cortical integrals plus endpoint activity; packet mean, beta, trace/query, association contributions and separate E/I operands are retained. | `loom_commissioning/diagnostics.py:65–93`; `loom_p/engine.py:65–71,106–110`; `loom_p/neural.py:49–69,90–95,124,163,230`; `loom_commissioning/runner.py:130–147`. The manufactured moving-body handoff had distinct start/end raw values, and independent residual, formation, delta and packet calculations matched exactly. |
| VERIFIED | Representative executable information boundaries withstand mutation and metadata attacks. | `loom_commissioning/controllers.py:25–36,94–115`; `loom_commissioning/adapter.py:87–88`. Recursive mutation of privileged controller inputs left the engine unchanged; sensor displays are detached copies. Contradictory AV/SO/private metadata and opposite external command arguments produced identical intact neural/body/field states when the permitted input and physical state were held equal. The private sentinel was absent from sensor output. |
| VERIFIED | Relevant parent P files and prior engineering tests are unchanged by this checkpoint. | Read-only `git diff 6bc9683b... 05abf604... --name-status -- developmental_ecology/loom_p developmental_ecology/configuration.json developmental_ecology/tests` returned no changes. The primary review owns the complete repository/package identity audit. |
| LIMITATION / EXPECTED PROVISIONAL CHOICE | The boundary tests demonstrate representative executable routes; they are not a general security proof against arbitrary Python code or a privileged machine owner. The D5 results are immediate receiver sensitivities, not counterfactual trajectories or evidence of useful control. | Scope required by the user request and declared by `loom_commissioning/diagnostics.py:22,60`; no hold follows from these limits. |
| SCIENTIFIC / COMMISSIONING QUESTION, NOT AN APPARATUS DEFECT | Whether intact/fixed P survives, whether association is useful, capacity is sufficient, or omitted contributions matter ecologically remains untested. | No ecological interpretation follows from the manufactured nonzero fixture or the poison checks. |

## Independent numerical evidence

The definitive receiver fixture used heterogeneous manufactured H and bank parameters, nonzero retained association activity and evocation, and manufactured body velocity/rotation. The resulting current-wave q norm was `0.00032818861375509854`.

| Omitted regulator contribution | Maximum absolute control change |
|---|---:|
| evoked feature input | `3.0416409509126385e-08` |
| actual-body feature input | `0.0013580344218542349` |
| bias | `0.00045968850019662694` |
| learned E bank | `0.0008118059252332221` |
| learned I bank | `0.0011014356092149402` |
| E exploration | `0.01187431880703127` |
| I exploration | `0.009997958663999662` |

Motor omission effects were also all nonzero: oscillator `0.01840110169634974`, noise `0.0057766288092570735`, direct feedback `0.00020753983050081012`, motor evocation `0.0005996567708801311`, regulatory current `0.0015905914576236045`, and attenuation `0.004565228514420393`. These values establish consequential arithmetic coverage in the fixture, not a biological effect threshold.

## Reproduction

Run from any working directory using the existing pinned environment. This script imports target modules read-only and writes only its JSON result alongside itself. It does not invoke a recorder or pytest, so there is no pytest cache or trajectory output.

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
& 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe' -B 'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\exports\2026-09-24-p-apparatus-review-05abf604\neural\independent_checks.py'
```

Definitive run: `independent_checks-final-002.log`, exit 0, 7.22 seconds. Machine-readable output: `independent_checks.json`. Source: `independent_checks.py`.

Two earlier review logs are preserved. `independent_checks.log` passed the initial checks. `independent_checks-final.log` contains a reviewer-fixture assertion failure after requiring every motor omission to be nonzero: its stationary manufactured body supplied zero direct feedback. The final fixture adds disclosed manufactured velocity/rotation and nonzero prior motor evocation, without changing target code. This was fixture coverage refinement, not an apparatus failure.

The full design, matrix, walkthrough, configuration-change rules, decisions document, build report, request and relevant neural/apparatus source were read. The source-level reasoning uses the unchanged P operations directly, not only the builder's labels or assertions. Saved-record reconstruction and the complete portable package suite remain the separately assigned primary/provenance reviewers' evidence.
