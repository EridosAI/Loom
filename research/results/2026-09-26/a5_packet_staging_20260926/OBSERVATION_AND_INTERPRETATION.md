# A5 predeclared observations and interpretation

**Held proposal; no A5 measurements yet.** Evidence class AV, privileged external physical witness. Use saved full-fidelity records only for post-run analysis after a separately resolved and authorized launch. Never feed observers, labels, plots or reported balances back into control. Preserve every failed approach, mistimed contact, impact, reserve cost and administrative stop.

## Event and visit accounting

Retain all eight stocks, every source contact/support interval, every impact and release, every source debit/body credit and both renewal half-increments. Distinguish a zero-duration touch/impact, positive-duration support, and positive transfer. For every source and planned visit record initial stock, first geometric approach and actual contact, stock immediately before/after each event, total and first-contact transfer, expenditure, E/I, forces/impulses, damage/repair and all contact interruptions. Do not merge A3-like microgaps out of the raw record.

The four planned source windows in `PROCEDURES.md` define visit groups, independent of their realized success. All other source contacts remain separately reported. A macro-departure requires actual release followed by observed surface clearance of at least one body diameter (1 m) from that source, before the next planned visit. Record the first native clearance sample and the preceding sample; this is a geometric reporting criterion, not a control input. A meaningful revisit then requires actual renewed positive-duration source contact in a later planned visit. A micro-release/recontact within a dwell is not a completed circuit.

For each candidate revisit, retain the final actual source-contact endpoint before the unattended interval, the entire away interval, all recontacts if they prevent an uninterrupted interval, the next actual contact endpoint, and time/stock brackets when only a native sample supports a boundary. Define away time from that final contact endpoint to the next contact start. Verify zero debit during an asserted unattended interval, and sum renewal directly over its recorded ledger subdivisions. If an exact boundary is unresolved, preserve its bracket and mark the attribution uncertain; do not manufacture an interpolated stock or delete residual flags. Planned departure time and actual release time are separate fields.

Record actual body path length as the sum of successive native position increments, with event positions where available; report it as sampled path length, not a continuous-time convergence proof. Retain approach, turn, travel, contact and away durations, all 0.2-second fixed-window reserve/intake/cost summaries, and planned versus realized stages. Record the complete initial and final E/I plus milestones and minima, mover pose/phase and any mover impact/damage, natural repair, and all controller/record/physical/admin failures. Destination productive source contact and contact quality must not be replaced by proximity alone.

## Renewal and origin accounting without inventing a mixing law

For each source $j$, use the actual event operands to check

$$S_{j,after}=S_{j,before}+R_{j,first}+R_{j,second}-D_j,$$

and for cumulative totals

$$S_j(t)=S_j(0)+R_j(t)-D_j(t).$$

The two renewal increments occur around the debit in the accepted accounting law. Keep that order. Verify each debit equals the source's credited body intake, the body energy ledger $E(t)-E(0)=\sum_jD_j(t)-C(t)$, and the integrity ledger from all damage and repair. Report maximum/accumulated residuals and numeric precision, without moving raw times or stock values.

The stock has no molecule-origin tags, so a unique split between original and regenerated energy would require an extra convention. Report conservative attribution intervals for every source:

$$D_{initial,j}\in[\max(0,D_j-R_j),\min(D_j,S_j(0))],$$

$$D_{renewed,j}\in[\max(0,D_j-S_j(0)),\min(D_j,R_j)].$$

Sum source-specific intervals for totals; do not use unused initial stocks at other sources to obscure forced renewal contribution at a visited source. The upper initial-stock bound is also the explicitly labelled **initial-first bookkeeping** amount, with the complementary lower renewed amount. It is a conservative accounting convention, not an implemented physical mixing or tracer law. Report full interval widths whenever provenance remains ambiguous.

For an uninterrupted unattended period, let $S_d$ be departure stock, $R_a$ the measured renewal while away, and $S_a$ stock immediately before revisit. Check $S_a=S_d+R_a$, with zero away debit. Let $T_v$ be transfer over the revisit window and $R_v$ all renewal during that window, including contact gaps. A conservative lower bound on uptake of the **away-restored stock** is

$$L_{away}=\max(0,T_v-S_d-R_v),$$

with upper bound $\min(T_v,R_a)$. Also report $\max(0,T_v-S_d)$ for post-departure renewal of any timing and $\max(0,D_j-S_j(0))$ for cumulative forced renewed uptake. These lower bounds may be loose; if they remain zero, actual recorded restored availability and subsequent transfer still remain observations, but specific origin/necessity is unresolved. Do not simulate a no-renewal comparator or change the transfer law to tag stock.

Quantify renewal benefit as absolute energy, fractions of revisit intake/whole-case expenditure, and basal-cost-equivalent seconds (energy/0.0015). Keep availability, productive use, provably renewed uptake, and necessity for remaining nonterminal distinct. No survival counterfactual or indefinite claim follows from these ledgers. Use residual-aware arithmetic positivity only; no newly invented usefulness percentile, exact-zero depletion target or tuning gate.

## Interpretation table

| Outcome | Evidence to report | Bounded interpretation / limit |
|---|---|---|
| A — productive renewed revisit | Actual partial depletion, meaningful departure, positive measured unattended renewal, restored stock at revisit, positive later debit/credit, completed planned observation nonterminal; report attribution bounds | Physically witnessed bounded renewal-supported recurrence at the recorded conditions. State whether renewed uptake is compelled by the bounds or only availability plus productive use is observed. No learning or indefinite support claim. |
| B — renewal small on this circuit | Report all restored stock, revisit transfer, attribution intervals and fractions of actual cost; productive returns may still occur | Quantify how little renewal contributed over this horizon. Do not invent a binary materiality threshold, tune dwell or infer ecological impossibility. |
| C — reserve-limited or physically terminal | Exact E/I terminal event, earlier intake/cost/damage/repair and route progress; low nonterminal E/I alone is not terminal | The prescribed case did not complete nonterminal; distinguish reserve budget, contact damage and controller/route limitations. No automatic world change. |
| D — controller or apparatus limitation | Missed release/arrival, excessive turning, unintended contact, timing/hold failure, record failure or the present static clock incompatibility | Report the limitation and missing observations. This does not establish physical/ecological impossibility. The present hold is static apparatus evidence, not an executed A5 outcome. |
| E — initial-stock support remains sufficient explanation | Initial-origin intervals allow all consumed energy to be initial; renewal provenance or productive renewed revisit not demonstrated | Continued nonterminal operation alone leaves the A5 renewal-supported question unresolved. Preserve any measured renewal separately. |
| Administrative/incomplete | Wall/storage/630-second stop, observed prefix, missing planned visits and exact reason | A prescribed full cutoff can bound a completed observation; an early resource stop may leave the question unresolved. No resume, extension or replacement. |

Report component claims separately rather than forcing every case into one exclusive success label. A renewed productive revisit before a later terminal event is still a local observation, but does not meet the entire nonterminal bounded-circuit conjunction. A partial controller miss does not erase prior transfer evidence. No row authorizes a patch, retry, new phase, extra case, experiment number or scientific efficacy conclusion.
