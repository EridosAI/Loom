---
id: P-IMPLEMENTATION-OBSERVATION-SPEC-83a00674
revision: v0.1-review-draft
authority_status: assistant-proposal-under-accepted-commission
work_status: ready-for-design-review
evidence_status: unimplemented-uncommissioned-untested
---

# P implementation and observation specification v0.1

This is a proposed construction contract for intact P in the accepted Base World. Jason has accepted the two separate research questions, permitted P's bounded bodily-learning scaffold, and selected P first for specification. The quantities and engineering completions below are proposals for review, not approved settings or evidence that the organism works. No implementation or scientific execution is authorised.

Read alongside the [plain-language walkthrough](P_PLAIN_LANGUAGE_DATA_FLOW_v0_1_REVIEW_DRAFT.md), [decision record](../../40_DECISIONS/DECISION-P-SPECIFICATION-2026-09-20-83a00674.md) and [source identities](SOURCE_IDENTITIES.json).

## 1. Authority, parent and classification

The controlling authority is the [handoff, sections 1–6](../../90_SOURCES/p_specification_authority_2026-09-20_83a00674/LOOM_P_SPECIFICATION_HANDOFF_2026-09-20.md) and Jason's present instruction reconfirming its scope. D1 keeps useful history-dependent regulation separate from a useful contribution of lasting sensory change. D2 admits only P's separate perturbation/consequence updates of the two regulatory banks. D3 selects the complete P v0.1 parent for this specification. R and every other family remain available; none is a compulsory control.

The exact [parent P](../../90_SOURCES/p_specification_authority_2026-09-20_83a00674/exact_parent/LOOM_ASSOCIATIVE_REGULATORY_CANDIDATE_v0_1_DISCUSSION_DRAFT.md) is 38,379 bytes, SHA-256 **34bd519bb01253f783521204c9e6358b11703282ec322f4707e5ece1bb6a4da4**. It was recovered byte-for-byte from the verified local setup checkpoint because the live reading copy has since received authorised MathJax delimiters and equation 3 whitespace changes. The [live reading copy](../../90_SOURCES/candidate_comparison_2026-09-20/sources/participation_retention/LOOM_ASSOCIATIVE_REGULATORY_CANDIDATE_v0_1_DISCUSSION_DRAFT.md) has identical mathematical tokens after those changes are accounted for; it is not falsely described as hash-identical. Both remain untouched in this commission. The new exact-parent custody copy is SRC-052; the registered handoff is SRC-051. Original conditional headers are historical, with permission supplied by the later decision.

The accepted world/body reference is the five-file local set associated with commit **7ada2b300fa12a26b0daf40b1fa5682243ff6625**. This is not a remote-main check. The [direction draft](../../90_SOURCES/direction_2026-09-18/LOOM_DEVELOPMENTAL_DIRECTION_v0_1_REVIEW_DRAFT.md) informs interpretation within its own attributed scope; later D1–D3 supersede its pending P-scaffold wording only as explicitly stated.

Four labels govern this document:

| Label | Meaning |
|---|---|
| Retained law | P's defined operation or an accepted Base World functional requirement, cited to its source. |
| Analytical consequence | A deduction from the stated law/configuration, not an observation. |
| Proposed completion | A concrete value, discretization, interface choice or physical realization where the parent/foundation left a slot open. |
| Proposed departure | A changed P mechanism or accepted functional choice requiring a separate ruling. None is adopted here; section 13 exposes the choices most liable to become departures. |

All numerical values, random initialisation recipes, sampling conventions, solver choices, physical formulas, file formats and inspector details in this document are **proposed completions**, even where that label is not repeated in every table cell. P equations are reproduced below with their original numbers. Extra mathematical definitions have descriptive labels, not experiment identifiers.

A possible result would be development under a disclosed bodily preference and asymmetric learning rule. Neither survival, a changed response, larger weights, persistent coefficients, nor frequent recall alone establishes useful lasting sensory change. Nothing here claims emergence of preference, a desire to exist, reliable episodic recall, transferred regulation or unrestricted imagination.

## 2. Coordinates, anatomy and ownership

Use body diameter $D_b$ as the length unit, seconds as physical time, one body mass unit, and separate normalised reserve units for $E$ and $I$. The proposed capacities are $E_{\max}=I_{\max}=1$. Numerical indices are observer/scheduler addresses; no index, clock, position, object identity or source stock enters the organism.

Channel order is fixed: light $L$, chemistry $C$, contact $T$, proprioception $P_r$, energy $E$, integrity $I$, motor $M$, applied regulation $R_g$. The subscript $P_r$ avoids confusing the proprioceptive channel with candidate P; $R_g$ is a channel of P, not candidate R. All arrays and rows have declared anatomical ordering without concept labels.

### 2.1 Dimensions and ranges

| Channel | Raw input width | Cortical width | Packet $b_m$ | Central block $\psi_m=[\beta_m,z_m]$ | Physical/provenance meaning |
|---|---:|---:|---:|---:|---|
| Light | 10 | 8 | 16 | 32 | Five forward sectors × two intensities |
| Chemistry | 4 | 8 | 16 | 32 | Two anterior sites × two overlapping chemical sensitivities |
| Contact | 8 | 8 | 16 | 32 | Eight body sectors measuring contact load |
| Proprioception | 7 | 8 | 16 | 32 | Commands and actual body-relative motion/effort discrepancy |
| Energy | 1 | none | 1 | 2 | Endpoint actual $v_E=E$ |
| Integrity | 1 | none | 1 | 2 | Endpoint actual $v_I=I$ |
| Motor | 2 commands | separate motor dynamics | 4 | 8 | Mean two commands, then endpoint two commands |
| Applied regulation | 12 held controls | no recurrent regulator added | 12 | 24 | Eight support, two currents, two attenuations actually applied |

There are 82 packet coordinates and 164 central coordinates. Every learned sensory channel has two fixed four-unit pools: units 0–3 and 4–7. One pooling level is sufficient to instantiate P's explicitly permitted one-level case; it does not silently replace P with a hierarchical-basis law.

For a sensory channel $W_m\in\mathbb R^{8\times d_m}$, $A_m,C_m\in\mathbb R^{8\times8}$. There are 232 effective sensory-weight entries; storing two shared rows plus eight residual rows per channel uses 290 scalar slots subject to centring constraints. Each directed map is $H_{mn,j}\in\mathbb R^{p_m\times p_n}$ with $m\ne n$, $p_m=\dim\psi_m$, and four context branches. Thus there are 224 maps and 88,608 map coefficients. No diagonal maps and no transpose constraint are supplied.

Each target/context gate vector has width $164-p_m$. The fixed regulator features have 32 nonlinear coordinates plus a constant: $\phi\in\mathbb R^{33}$. $B_q$ is $32\times164$, $B_v$ is $32\times2$, and each of $\Theta_E,\Theta_I,\bar\Theta_E,\bar\Theta_I,Z_E,Z_I$ is $12\times33$. A bank's output rows are ordered eight $h$, left/right $j$, left/right $\kappa$. Both banks have all 12 rows.

Raw light, chemical and contact readings lie in $[0,1]$; proprioception and command readings lie in $[-1,1]$. Cortical $x$ and associative $a$ lie in $[-1,1]$ under the specified convex updates. Sensory packets lie in $[-1,1]$, centred packets/traces can reach $[-2,2]$. Bodily packets lie in $[0,1]$ and their centred blocks in $[-1,1]$. Applied currents lie in $[-0.5,0.5]$, support/attenuation in $(0,1)$. A return $q$ is a bounded map output in these declared native coordinates, not a reconstructed physical reading. Never clip or reinterpret it as actual reserves.

### 2.2 State life cycle

Every state persists across handoffs unless explicitly marked as a turning-over accumulator. An independent new life resets all learned, transient and physical state according to section 9. A pause preserves all of it without advancing clocks.

| State | Owner and input | Output/effect | Persistence and initialization |
|---|---|---|---|
| Geometry, pose, velocity, source stocks, chemical fields, $E,I$ | Physical world/body | Raw transducers and real capability/consequence | Persistent within life; lawful newborn world, no learned inheritance |
| $s_m,\bar s_m,r_m,x_m,C_m$ | Sensory-local process; actual raw input | Receptor-centred activity and local formation pressure | Filters/activity/coactivity transient; $\bar s_0=s_0$, $x_0=C_0=0$ |
| Shared rows $\mu^W_g$, residuals $\delta_{g,i}$ and their references | Sensory process only | Reconstruct $W$; change future receptor response | Lasting, bounded; small untrained birth values and matching references |
| $o_g$ | Private opening physiology | Pool spring term | Slow capacity availability; starts 0, not a learner clock input |
| Packet accumulators and endpoint caches | Channel emission process | Completed $b_m$ | Accumulators reset each handoff; activity does not |
| Packet means $\mu^b_m$, contexts $z_m$, $\beta_m,\psi_m$ | Completed actual packets | Gates, query and coactivity write | Finite context/means persist; actual birth baselines, context 0 |
| $H_{mn,j}$ | Association, from actual $\psi$ | Cross-channel return | Lasting; starts 0; independent directed maps |
| Map-use state $v^{use}_{mn,j}$ | Actual old-map retrieval contribution | Reduces that map's decay | Slow trace, starts 0; not an occurrence count |
| $a,q,y,g$ | Association | Returned content and transient computation | Persistent $a$ starts 0; final $q$ held during native interval |
| $\Theta_d,\bar\Theta_d$ | Corresponding bodily adapter | Regulatory response parameters | Lasting, separate, start 0 |
| $\ell_d,Z_d$ and previous $\xi_d,\phi$ | Actual sensed body plus applied perturbation history | Dimension-specific update | Finite filters/eligibility; $\ell_0=v_0$, $Z_0=0$; no fictional predecessor |
| $\phi,L_d,h,j,\kappa$ | Stateless feature/output calculation using learned banks | Applied control settings | Held for one ensuing interval; actual controls become next packet |
| Motor phase, $\nu_i,z_i^M,\chi_i,u_i$ | Spontaneous generator plus declared feedback/return | Paired command to body | Transient persistent generator; bounded random birth states; $z^M_0=0$ |
| Fixed matrices, biases, pool memberships, constants | Supplied anatomy/configuration | Define capacities and transformations | Never trained or outcome-selected during life |
| Seeds, counters, next event times, partial records | Scheduler/observer | Reproducibility and inspection only | Must survive pause; no route into representation |

Here $\mu^b$ denotes P's packet mean and $\mu^W$ its shared sensory row; they are different arrays despite the parent using $\mu$ in both contexts. Likewise $v_d$, gate vectors $v_{mj}$, map-use $v^{use}$ and physical velocity are distinct. These disambiguations add no state or operation.

## 3. Native sensory processing and packets

Retain [P section 3 and equations 1–3](../../90_SOURCES/p_specification_authority_2026-09-20_83a00674/exact_parent/LOOM_ASSOCIATIVE_REGULATORY_CANDIDATE_v0_1_DISCUSSION_DRAFT.md#3-native-sensory-processing-and-packet-formation):

$$
\tau_{s,m}\dot{\bar s}_m=s_m-\bar s_m,\qquad r_m=s_m-\bar s_m.
$$

$$
\tau_{x,m}\dot x_m=-x_m+\tanh(W_mr_m+A_mx_m).
\tag{1}
$$

$$
b_{m,k}=\left[\frac1\Delta\int_{t_{k-1}}^{t_k}x_m(t)\,dt,\ x_m(t_k)\right].
\tag{2}
$$

$$
\tau_C\dot C_m=x_mx_m^\top-C_m,
$$

$$
F_{m,i}=x_{m,i}r_m^\top-x_{m,i}^{2}w_{m,i}
-\chi\sum_{j\ne i}C_{m,ij}w_{m,j}.
\tag{3}
$$

Rows of $F$ have the same coordinate shape as rows of $W$. The coefficient $\chi=0.1$ in (3) is distinct from the motor-noise process $\chi_i(t)$. This is an Oja-type local pressure with competition and nonlinear recurrence; it is not Oja's proved linear model and is not body-scored sensory training. Neither $q$ nor $m_E,m_I$ appears in $F$. Section 6 supplies the actual bounded change of $W$.

For each native step $h_n=0.01$ s, evaluate $r$, $F$ and all right-hand sides from the step's old state and actual current raw readings. Use exponential Euler for leaky activity:
$x^+=e^{-h_n/\tau_x}x+(1-e^{-h_n/\tau_x})\tanh(Wr+Ax)$.
Update the receptor mean toward current $s$, and $C$ toward old $xx^\top$, by their exact frozen-input exponential filters. Accumulate $h_n(x+x^+)/2$ for each sensory packet integral; append endpoint $x^+$ at the handoff. This is declared numerical quadrature, not an extra observation. No receptor-level tonic bypass is added.

The motor packet is exactly $[\operatorname{mean}(u_L,u_R),u_L(t_k^-),u_R(t_k^-)]$, using the two-value mean block followed by the two-value endpoint block. Commands are the values actually delivered to the actuator interface, before physical strength/impairment turns them into force. Record resulting motion separately. Do not append internal motor tendency, force, an antisymmetric temporal signature or an inferred intended action to this packet.

Proposed packet completions where P leaves the emission statistic open:

- $b_{E,k}=v_E(t_k)$ and $b_{I,k}=v_I(t_k)$, the actual endpoint readings. These also reach the regulator directly.
- $b_{R_g,k}=[h_{k-1},j_{k-1},\kappa_{k-1}]$, a 12-vector. These controls were constant over the completed interval, so an extra identical mean/endpoint block would only duplicate them. No recalled $q_{R_g}$ is inserted.
- Raw sensed movement enters association through P's receptor-driven proprioceptive cortex, not by appending privileged physical coordinates.

Forces, source labels and field grids remain outside the learner even though the observer retains them.

## 4. Association and map preservation

Retain [P section 4](../../90_SOURCES/p_specification_authority_2026-09-20_83a00674/exact_parent/LOOM_ASSOCIATIVE_REGULATORY_CANDIDATE_v0_1_DISCUSSION_DRAFT.md#4-the-central-operation-conditioned-coactivity-not-next-wave-prediction). At each real handoff:

$$
\beta_{m,k}=b_{m,k}-\mu^b_{m,k-1},\qquad
z_{m,k}=e^{-\Delta/\tau_z}z_{m,k-1}+(1-e^{-\Delta/\tau_z})\beta_{m,k},
\qquad \psi_{m,k}=[\beta_{m,k},z_{m,k}].
\tag{4}
$$

The packet mean is written only after the read, as
$\mu^b_{m,k}=\mu^b_{m,k-1}+(1-e^{-\Delta/\tau_\mu})\beta_{m,k}$.
It is never subtracted twice.

$$
g_{mj}=
\frac{\epsilon_g+\sigma(v_{mj}^{\top}\psi_{-m}+c_{mj})}
{\sum_r[\epsilon_g+\sigma(v_{mr}^{\top}\psi_{-m}+c_{mr})]}.
\tag{5}
$$

Here $r$ in the denominator indexes the four branches. Gate vectors and biases are fixed generic anatomy. Gates use other channels' **ungated actual** $\psi$, excluding the target channel $m$ only. Thus sensory support does not suppress all influence of a channel on the centre.

The single post-read map update is:

$$
H_{mn,j}^{new}=\operatorname{Proj}_{\mathcal H}
\left[H_{mn,j}^{old}+\Delta\left(
\eta_Hg_{mj}\psi_m\psi_n^\top-\lambda_H(v^{use,old}_{mn,j})H_{mn,j}^{old}
\right)\right],\quad m\ne n.
\tag{6}
$$

P's use-dependent law is retained:

$$
\tau_v\dot v^{use}_{mn,j}
=-v^{use}_{mn,j}
+\frac{\|g_{mj}H_{mn,j}a_n\|^2}
{\epsilon_v+\|g_{mj}H_{mn,j}a_n\|^2},
\qquad
\lambda_H(v)=\lambda_{H,\min}+\lambda_{\rm unused}(1-v).
\tag{7}
$$

The numerical completion samples its drive once from the **final old-map read**:
$c^{use}_{mn,j}=g_{mj}H^{old}_{mn,j}a_n^{(S)}$,
$u^{use}=\|c^{use}\|^2/(\epsilon_v+\|c^{use}\|^2)$.
After (6), set
$v^{use,new}=e^{-\Delta/\tau_v}v^{use,old}+(1-e^{-\Delta/\tau_v})u^{use}$.
This is a declared wave-clock sample-and-hold realization of (7), resolving P's use-ODE versus handoff-order gap. Its new value affects later decay. Do not recompute this score from newly written $H$, integrate one full $\Delta$ per relaxation sweep, or turn use into a positive coactivity write. It can preserve mistaken recall.

For each sensory unit, repeat its anatomical group's gain over its mean, endpoint and both trace copies:

$$
G_{m,g}=g_{\min}+(1-g_{\min})h_{m,g},\qquad
y_m=G_m(h_{k-1})\psi_m.
\tag{8}
$$

Other channels use unit gain. With old maps and fixed $g,y$ during the handoff, start $a^{(0)}=a_{k-1}$ and perform exactly four **simultaneous** sweeps:

$$
q_m^{(r)}=\sum_{n\ne m,j}g_{mj}H^{old}_{mn,j}a_n^{(r)},
\qquad
a_m^{(r+1)}=(1-\alpha_a)a_m^{(r)}
+\alpha_a\tanh(y_m+q_m^{(r)}),
\quad r=0,\ldots,S-1.
\tag{9}
$$

Then recompute $q_{m,k}=\sum g_{mj}H^{old}_{mn,j}a_n^{(S)}$ without taking a fifth activity update. Persist $a_k=a^{(S)}$. No new $H$ is read during this handoff, and there is no convergence-based early exit.

The proposed joint timing is $\Delta=0.2$ s, $S=4$, $\tau_a=0.2$ s and
$\alpha_a=1-\exp[-\Delta/(S\tau_a)]\simeq0.2211992169$.
This assigns one wave-duration relaxation budget to the batched centre. Internal substeps do not advance world time or represent imagined future events. Freezing an input over those sweeps is an approximation with a declared physical scale. Changing $S$ alone at fixed $\alpha_a$ changes the effective dynamics; even changing $S$ with the formula preserved changes the finite nonlinear realization and requires a recorded revised configuration. It is not a free performance setting.

Each map's Frobenius radius is proposed as 0.10. In the maximum-over-channels Euclidean block norm, $\|\sum_jg_{mj}H_{mn,j}\|\le0.10$ and seven source channels give a frozen-read Lipschitz bound 0.70. The nonlinear sweep is therefore contractive under frozen inputs in this proposed regime. That is an analytical bound, not whole-loop stability or useful learning. This configuration deliberately begins with fading cue-driven association; it does not claim unrestricted multistability.


## 5. Regulatory response and separate bodily credit

Retain [P sections 5 and 8](../../90_SOURCES/p_specification_authority_2026-09-20_83a00674/exact_parent/LOOM_ASSOCIATIVE_REGULATORY_CANDIDATE_v0_1_DISCUSSION_DRAFT.md#5-regulation-a-learned-response-to-evocation). Full final $q$ and actual current $v_E,v_I$ enter the fixed feature map:

$$
\phi_k=\left[1,\ \tanh(B_qq_k+B_v[v_E,v_I]^\top+b_R)\right].
\tag{10}
$$

There is no extra direct raw-scene, contact or proprioceptive input to this feature map. The direct fast motor feedback in section 6 is a different route. With zero maps, $q=0$, so body-only and bias-dependent regulatory habits remain possible.

For each bank $d\in\{E,I\}$:

$$
L_{d,k}=\Theta_{d,k}\phi_k+\sigma_d\xi_{d,k}.
\tag{11}
$$

$$
D_d(v_d)=d_{0,d}+(1-d_{0,d})(1-v_d).
\tag{12}
$$

Each new $\xi$ coordinate is an independent pseudorandom sign, drawn once at the handoff after the preceding participation receives its update. Both banks' perturbations are applied, rather than being hypothetical alternatives.

$$
h_{m,g}=\sigma\left(b^h_{m,g}+D_E L^h_{E,m,g}+D_I L^h_{I,m,g}\right).
\tag{13}
$$

$$
j_i=\frac{J_{\max}}2\left[\tanh(D_E L^j_{E,i})+\tanh(D_I L^j_{I,i})\right],
\qquad
\kappa_i=\sigma\left(b^\kappa_i+D_E L^\kappa_{E,i}+D_I L^\kappa_{I,i}\right).
\tag{14}
$$

The physical superposition in (13)–(14) is P's supplied anatomy. It can cancel or reinforce the banks' effects. It is not a learned common objective, a shared critic or proof that arbitration emerged. Hold $h,j,\kappa$ constant until the next handoff; the newly calculated $D_d$ is incorporated into those held values, not recomputed continuously behind their backs.

Credit is evaluated **before** the new draw. Retain:

$$
m_{d,k}=\frac{v_{d,k}-\ell_{d,k-1}}{\tau_{b,d}},
\qquad
\ell_{d,k}=\ell_{d,k-1}+
(1-e^{-\Delta/\tau_{b,d}})(v_{d,k}-\ell_{d,k-1}).
\tag{19}
$$

$$
Z_{d,k}=e^{-\Delta/\tau_e}Z_{d,k-1}
+(1-e^{-\Delta/\tau_e})\xi_{d,k-1}\phi_{k-1}^{\top}.
\tag{20}
$$

$$
\Theta_{d,k}=\operatorname{Proj}_{\mathcal T_d}
\left[\Theta_{d,k-1}+\eta_d\Delta m_{d,k}Z_{d,k}
-\rho_d\Delta(\Theta_{d,k-1}-\bar\Theta_{d,k-1})\right].
\tag{21}
$$

Then update the reference:

$$
\bar\Theta_{d,k}=\bar\Theta_{d,k-1}+
(1-e^{-\Delta/\tau_{\rm ref,d}})(\Theta_{d,k}-\bar\Theta_{d,k-1}).
$$

Each row is projected onto a Euclidean ball of radius 1. The scalar $m_d$ has units $\mathrm{s}^{-1}$ because the actual reading is normalised; $\eta_d$ is dimensionless and $\rho_d$ has units $\mathrm{s}^{-1}$. A positive or negative bodily trend is not an event label or a source of counterfactual knowledge. Energy drift, damage, costly travel, delayed repair and coincident intake can all enter ambiguous credit.

Only the corresponding bank receives its $m_dZ_d$ term. There is no combined energy–integrity learning score and no route from either bodily term into $F$ or the positive $H$ write. The adapter's indirect effects on motor exposure, query gain, sensory retention and future packets remain substantial.

## 6. Sensory retention and ongoing motor output

### 6.1 Local formation, coarsening and references

Retain [P section 6](../../90_SOURCES/p_specification_authority_2026-09-20_83a00674/exact_parent/LOOM_ASSOCIATIVE_REGULATORY_CANDIDATE_v0_1_DISCUSSION_DRAFT.md#6-the-sensory-participationretention-link), with the shared-row name made explicit:

$$
w_{g,i}=\mu^W_g+\delta_{g,i},\qquad \sum_{i=0}^3\delta_{g,i}=0,\qquad
\bar F_g=\frac14\sum_{i=0}^3 F_{g,i}.
$$

$$
\dot\mu^W_g=\eta_0\bar F_g-\rho_0(\mu^W_g-\bar\mu^W_g),
\qquad
\dot\delta_{g,i}=\eta_1(F_{g,i}-\bar F_g)-\Lambda_g\delta_{g,i}
-\rho_1(\delta_{g,i}-\bar\delta_{g,i}).
\tag{15}
$$

$$
\tau_{\rm ref,0}\dot{\bar\mu}^W_g=\mu^W_g-\bar\mu^W_g,\qquad
\tau_{\rm ref,1}\dot{\bar\delta}_{g,i}=\delta_{g,i}-\bar\delta_{g,i}.
$$

$$
\Lambda_g=\lambda_{W,\min}+\lambda_{\rm immature}(1-o_g)
+\lambda_{\rm reclaim}(1-h_g),\qquad
\tau_{\rm open}\dot o_g=1-o_g.
\tag{16}
$$

The parent reuses $\lambda_{\min}$ in different contexts; the specification names independent $H$ and $W$ constants to prevent accidental parameter tying. One opening scalar per group is initialized to zero with the same supplied time constant. It remains private physiological state. No learned trigger, disagreement detector or semantic capacity request is added.

Define $D_g$ as the four-row residual stack. Its convex admissible set is
$\sum_i\delta_i=0,\ \|D_g\|_F\le0.08$; shared rows satisfy $\|\mu^W_g\|_2\le0.30$.
These are component bounds on the chosen shared/residual representation. Euclidean projection of the residual stack first subtracts its row mean, then scales radially only if the Frobenius bound is exceeded. The shared projection is radial clipping to its ball.

For the continuous sensory law, tangent-project its velocity. Centre residual velocity; at a norm boundary remove an outward radial component $\langle D,V\rangle D/R^2$ when that inner product is positive. Treat the shared row analogously. Take the declared native step and apply the same Euclidean projection to maintain finite-step feasibility. Record the raw velocity, removed radial contribution and feasibility correction. This is a numerical realization of P's tangent-projected law, not a body-dependent projection or a new sensory target. References follow the **old** shared/residual values with exact frozen-input exponential filters during each native step; centring is preserved. Opening follows its exact exponential solution.

The three terms in (15) have different meanings: local formation, support-dependent contraction of fine residuals, and attraction to a slow reference. High support reduces one spring. It neither writes desired features nor proves that fine differences caused useful behaviour. The group common signal could earn support while useless residuals share its protection.

### 6.2 Motor tendency, command and physical enactment

Retain [P section 7](../../90_SOURCES/p_specification_authority_2026-09-20_83a00674/exact_parent/LOOM_ASSOCIATIVE_REGULATORY_CANDIDATE_v0_1_DISCUSSION_DRAFT.md#7-ongoing-motor-activity-not-trajectory-playback):

$$
o_i(t)=a_i\sin\varphi_i(t)+b_i\nu_i(t),\qquad
\dot\varphi_i=\omega_i,\qquad
\tau_\nu\dot\nu_i=-\nu_i+\chi_i(t).
\tag{17}
$$

$$
\tau_M\dot z_i^M=-z_i^M+
\tanh\left(o_i+[K_pp(t)]_i+[D_Mq_M]_i+j_i\right),
\qquad
u_i=u_{\max,i}(1-\kappa_i)z_i^M.
\tag{18}
$$

The feedback vector is $p=[s_{P_r},s_T]\in\mathbb R^{15}$: current raw proprioception and contact only. $K_p$ is a fixed generic $2\times15$ anatomical map, not an installed collision-avoidance controller. Its contact/proprioceptive route is available without going through association and remains so under sustained sensory adaptation.

With zero-based motor block order
$q_M=[q_{\beta,\text{mean},L/R},q_{\beta,\text{end},L/R},q_{z,\text{mean},L/R},q_{z,\text{end},L/R}]$,
the proposed $D_M$ selects coordinates 2 and 3 with unit coefficient. They are the **centred endpoint-command return**, not an absolute physical command estimate. No packet mean is added back; no trace is played as a motor tape. This selection completes the parent's “native current-command block” wording explicitly.

The motor-noise drive changes every 0.5 s, independently for each actuator, with $\chi_i=\pm1$ held between changes. $\nu$ uses its exponential frozen-drive update. Phase advances analytically. Evaluate (18) using the step's old phase/$\nu$, actual current $p$, and held $q,j,\kappa$; use exponential Euler for $z^M$. The resulting $u$ is held on the next native physical subinterval and is the actual command recorded in the motor packet. Sensor activity and motor activity persist across handoffs. Braking remains logistic, not an unreported exact-stop command.

## 7. Exact scheduling contract

Let handoffs be $t_k=k\Delta$. Interval $k$ means $[t_k,t_{k+1})$. No semantic encounter boundary follows from it.

### 7.1 A real handoff at $t_k$, for $k\ge1$

| Order | Reads | Writes and permitted effect |
|---:|---|---|
| 1 | The completed interval under $q_{k-1},h_{k-1},j_{k-1},\kappa_{k-1}$; actual endpoint body state | Finalize eight $b_{m,k}$; form $\beta_k$ from old means, then $z_k,\psi_k$. Turn over packet accumulators only. |
| 2 | $v_{d,k},\ell_{d,k-1},Z_{d,k-1},\xi_{d,k-1},\phi_{k-1},\Theta_{d,k-1},\bar\Theta_{d,k-1}$ | Compute $m$, then $\ell$, $Z$, projected $\Theta$, then its reference, in that order. The new random variation does not yet exist. |
| 3 | Ungated $\psi_k$; old $H$; old map-use state; $h_{k-1}$; persistent prior $a$ | Form fixed gates, old-support query, four simultaneous relaxations, final recomputed $q_k$ and final-read use contributions. No $H$ write. |
| 4 | Full $q_k$, actual $v_{E,k},v_{I,k}$ and the updated banks | Form $\phi_k$; draw $\xi_{E,k},\xi_{I,k}$; calculate and hold $h_k,j_k,\kappa_k$. |
| 5 | Actual $\psi_k$, gates, old $H$, old use, final-read use contributions | Write every $H$ once by (6); update use by the declared sampled (7); update packet means. Do not read the new maps again at this handoff. |
| 6 | New held return/controls and uninterrupted native states | Begin interval $k$. New support changes the coarsening coefficient now; its direct query effect waits for $t_{k+1}$. |

A direct $j_k$ or $\kappa_k$ variation can affect the body during interval $k$ and enter $m_{k+1}$. A support variation $h_k$ first changes a direct query at $t_{k+1}$; that query's ensuing motor consequences first enter an endpoint score at $t_{k+2}$. Retention starts during interval $k$ but its useful behavioural consequence is not assigned a guaranteed latency. The proposed five-second eligibility trace covers many handoffs; it neither identifies the cause of a change nor guarantees useful credit.

### 7.2 Native physical step

There are exactly 20 native steps per handoff. When a native boundary is also a handoff, finish the preceding physical step and its packet contributions first, perform section 7.1, then begin the next native step.

1. Read transducers from the physical state at the native boundary. Proprioceptive/contact caches contain the preceding solved native interval's commands, endpoint movement and contact impulse rates.
2. If a motor-noise refresh is due, draw only the new held $\chi$; do not reset $\nu$. Evaluate sensory local dynamics, references/opening and motor dynamics from their old native states with current raw inputs and held wave controls. Each subsystem uses a consistent frozen old-state right-hand side.
3. Advance those native states by the declared filters/projections. Accumulate trapezoidal sensory activity. Produce the new paired command from updated $z^M$ and held $\kappa$.
4. Solve the body's rigid motion/contact under that command for the physical step, resolving swept impacts and any time-of-impact splits. Integrate the physical source, expenditure, stress and repair laws on the same contact subintervals. These physical subdivisions do not redraw neural noise, advance extra neural learning steps or generate extra handoffs.
5. Advance chemical fields with the declared fixed field step and ending geometry/stocks; retain the concentration state. Sample the next raw readings from that resulting world. Record actual commands as a piecewise-constant integral and the final commanded value.
6. Process terminal/non-finite events according to section 11; never let renderer timing alter simulated time.

Treat the full native advance as tentative until physical event handling finishes. If nonviability occurs inside the step, retain its complete pre-step checkpoint and recompute the shortened coupled step for the candidate elapsed time using the same actual starting inputs and already drawn/held noise. Locate the earliest terminal time consistently with the recomputed motor command, physical consequences and shortened field/neural updates; discarded solver iterations are not additional learning, elapsed time or draws. Commit only the shortened state and packet integral. End as a terminal partial wave without inventing a completed handoff or bodily-credit update. An unresolvable event is an apparatus failure with the last coherent checkpoint retained.

This operator order is a proposed deterministic first implementation, not a claim of numerical convergence. Contact subdivisions preserve physical elapsed time. No hidden repeat-until-success, adaptive neural relaxation count or mid-life timestep adjustment is permitted in an evidential configuration.


## 8. Proposed body and accepted Base World realization

The functional requirements come from [Coupling sections 4–14](../../90_SOURCES/reference_7ada2b300fa1/docs/developmental_ecology/PRIMITIVE_ORGANISM_WORLD_COUPLING_SPEC_v0_1.md#4-the-organisms-body), [Base World sections 1–13](../../90_SOURCES/reference_7ada2b300fa1/docs/developmental_ecology/BASE_WORLD_COMPLETION_v0_1.md#1-accepted-starting-world-at-a-glance), the [Design Frame](../../90_SOURCES/reference_7ada2b300fa1/docs/developmental_ecology/DEVELOPMENTAL_ECOLOGY_DESIGN_FRAME_v0_2.md), and the [decision ledger](../../90_SOURCES/reference_7ada2b300fa1/docs/developmental_ecology/DEVELOPMENTAL_ECOLOGY_DECISION_LEDGER_v0_2.md). This section supplies previously open constitutive laws and quantities. They are not measured calibration or accepted numerical doctrine.

### 8.1 Geometry and materials

The closed interior is $[0,20]\times[0,20]\,D_b^2$, without wrapping. The organism is a homogeneous rigid disk of radius $0.5D_b$, mass 1, inertia 0.125 and oriented paired actuators at lateral lever arms $\pm0.35D_b$. The wall-only centre-accessible nominal area is $A_U=(20-1)^2=361D_b^2$.

Proposed count rules are $N_E=\max(2,\lfloor A_U/45+0.5\rfloor)=8$ and $N_R=\max(2,\lfloor A_U/120+0.5\rfloor)=3$. These are newly proposed density realizations, not revived numerical gates. The fixed layout is:

- Eight identical anchored source disks of radius $0.5D_b$, centred at $(3,3),(10,3),(17,3),(3,10),(17,10),(3,17),(10,17),(17,17)$.
- Three separate homogeneous anchored restorative bodies: rectangles $[0,0.25]\times[8,12]$, $[19.75,20]\times[8,12]$ and $[8,12]\times[19.75,20]$. Each is wall-adjacent with a four-diameter exposed long face; initially non-depleting.
- One homogeneous rigid non-agentive block of width 2 and height 1, orientation zero, centre $(10+4\sin(2\pi t/30+\phi_B),10)$. It moves back and forth on a fixed straight line with a 30 s period, with smooth reversals. Uniform $\phi_B$ is uniform time-phase. It does not choose its motion in response to the organism.

No other pushable objects or behavioural fixtures are added. A small palette is shared by role:

| Material | Use | Two-band reflectance | Total chemical emission vector |
|---|---|---|---|
| M0 | Background | $(0.20,0.20)$ | zero |
| M1 | Walls and mover | $(0.45,0.45)$ | zero |
| M2 | Every energy source | $(0.70,0.35)$ | $0.05(0.1+0.9S/0.20)(1,0.5)$ |
| M3 | Every restorative body | $(0.35,0.65)$ | $0.05(0.25,0.35)$ |
| M4 | Organism | $(0.40,0.40)$ | zero |

Chemical emission units are concentration × area per second per whole emitting body, distributed uniformly over its area. Mixtures overlap; they are not receptor-visible one-hot class codes. A depleted source remains visible and emits a residual mixture; no stock meter is installed in light or a semantic chemical channel.

### 8.2 Mechanics, impairment and real consequence

Let $e_\theta$ be body-forward direction, $v$ planar velocity, $\omega$ angular velocity and $u_L,u_R$ the delivered dimensionless commands. Proposed actuator forces are
$f_L=0.5(0.2+0.8E)(0.4+0.6I)u_L$ and
$f_R=0.5(0.2+0.8E)(0.7+0.3I)u_R$.
The two factors express disclosed physical reserve-dependent capacity and integrity asymmetry, not a combined utility or learning signal. They recover continuously when the actual corresponding reserve recovers.

Between contacts,
$\dot x_{\rm body}=v$,
$\dot\theta=\omega$,
$m\dot v=(f_L+f_R)e_\theta-\gamma_vv$ and
$J\dot\omega=0.35(f_R-f_L)-\gamma_\omega\omega$,
with $\gamma_v=1$, $\gamma_\omega=0.2$, $m=1$, $J=0.125$.
Healthy constant equal full commands give a free-motion steady speed of $1D_b/\mathrm{s}$; opposite full commands give $1.75$ rad/s. These are analytical scales, not observed behaviour under P's spontaneous commands.

Contacts are unilateral, frictionless in the normal constraint solve, with zero restitution; floor drag remains present. Rigid nonoverlap is mandatory. Use swept disk/fixture collision detection with the mover's analytic trajectory and time-of-impact subdivision. At simultaneous contacts project the free generalized velocity in the mass/inertia metric onto all non-closing normal-velocity constraints, accounting for mover surface velocity. The resulting nonnegative normal impulses are the physical contact impulses. Integrate free drag exactly with frozen force/orientation on a native physical subinterval, then use the corrected velocities to advance pose. A later implementation must record its contact ordering/tolerances and fail on an unsolved constraint, missed overlap or non-finite result; it cannot teleport to a favourable pose. This is a mechanics constraint solve, not an organism action optimiser.

Separate zero-duration impacts from positive-duration sustained contact. An instantaneous impact contributes immediate damage $-0.02J_{n,c}$, with no transfer or repair duration; never average that impact over preceding free flight to create fictitious contact. For sustained contact $c$ over a positive physical subinterval $\delta t$, define $F_c=J_{n,c}/\delta t$ and relative surface-speed magnitude $v_{\rm rel,c}$, including rotation and mover motion. Use the same stress law for every collider:
$\Delta I_{\rm damage}=-0.02\sum_c\max(J_{n,c}-0.25\delta t,0)$.
The coefficient has integrity-per-impulse units. For the native contact-receptor cache, include both instantaneous and sustained-contact impulses divided by the actual native interval duration. Counting impulse rather than a squared instantaneous impact rate avoids defining damage that diverges simply because an impact is resolved over a shorter substep. It still requires later numerical commissioning.

Energy expenditure is
$P_E=0.0015+0.001(|u_L|+|u_R|)/2$
reserve units/s, with positive basal expenditure and cost for stalled or impaired attempted effort. No passive integrity decay or energy-funded integrity repair is present.

Each source has capacity $C_S=0.20$ and renewal time $\tau_S=400$ s:
$\dot S_i=(C_S-S_i)/\tau_S-U_i$ and $\dot E=\sum_iU_i-P_E$.
At actual source contact propose
$Q_i=\max_{c\in i}\{F_c/(F_c+0.1)\,[1+(v_{\rm rel,c}/0.25)^2]^{-1}\}$,
with $Q_i=0$ if there is no such contact, and
$U_i^{req}=0.04(S_i/0.20)(1-E)Q_i$.
This contact factor is a physical exchange law. Its identity-bearing contact data do not enter the learner.

For each solved physical subinterval: apply exact half-step renewal; calculate requested transfer at that state and current $E$; cap each requested debit by its available stock; if their sum exceeds bodily headroom plus that subinterval's expenditure, scale all debits by one common proportional factor. Use exactly those actual debits as body credits, subtract expenditure, then apply the second half-step renewal. Record both renewal increments and every requested/actual transfer. The transfer cap is physical conservation, not reward normalization. Locate a terminal $E=0$ crossing before continuing the life; do not revive it by crediting a later subinterval. Roundoff cannot be silently converted into extra energy.

Restorative contacts have
$Q_R=\max_{c\in M3}\{F_c/(F_c+0.1)\max(1-F_c/0.25,0)/[1+(v_{\rm rel,c}/0.25)^2]\}$,
or zero without contact. Apply damage first, stop if it is terminal, and otherwise use
$\dot I_{\rm repair}=0.02(1-I)Q_R$,
integrated as the exact frozen-$Q_R$ exponential approach to 1 for the remaining subinterval. No repair is credited for forceful contact above the threshold. Energy keeps falling unless separate actual source transfer offsets it. These numerical stress thresholds are proposed constitutive parameters, not scientific pass/fail gates.

A single source's maximum renewal is $0.0005$ reserve/s, below basal expenditure $0.0015$; eight sources have aggregate maximum $0.004$. This rules out indefinite support by renewal from one perpetually depleted source under these formulas. It does not prove accessible multi-source sufficiency, timely departure, usable damaged-state repair or indefinite viability. Initial stocks can fund finite behaviour.

### 8.3 Physical transducers

All sensors are deterministic in this proposed configuration: additional sensor-noise amplitude is zero, an explicit simplifying assumption. Capability impairment is physical as above; no extra sensory degradation is silently added.

**Light, 10 values.** Place the optical origin at the forward body boundary. Five sectors of width $24^\circ$ span $[-60^\circ,60^\circ]$; sample three rays per sector at centre offsets $-8^\circ,0,+8^\circ$. For each first solid hit within $12D_b$, band intensity is
$\rho_b[0.1+0.9\max(n\cdot\ell,0)V_{\rm light}]L_b e^{-d/(8D_b)}$,
where $\ell=(1,1)/\sqrt2$, $L=(1,0.8)$, $n$ is the physical outward surface normal, and $V_{\rm light}$ is visibility toward the distant light. Ignore the organism's own body for outgoing visual rays. With no hit, return the background ambient value $0.1\rho_{M0,b}L_b$. Average the three intensities per sector/band. Geometry, hit identity, distance, normal and occlusion tests are renderer internals; only ten intensities enter $s_L$. The rear $240^\circ$ is blind. Ambient and directional illumination have the same spectral profile.

**Chemistry, 4 values.** Sample two persistent fields at the anterior body-boundary angles $\pm45^\circ$, offset outward by $0.001D_b$ as a declared sampling convention. Bilinear field samples feed the fixed sensitivity matrix
$\begin{bmatrix}1&0.5\\0.5&1\end{bmatrix}$.
For each resulting nonnegative mixture $z$, output $z/(0.05+z)$. Location and sensitivity ordering are fixed receptor anatomy, not shared semantic coordinates.

**Contact, 8 values.** Receptor-sector centres are $2\pi j/8$ around the entire body. Distribute each preceding native interval's solved normal impulse rate linearly to the two adjacent sector centres in body-relative angle. Sum sector force $F_j$ and output $1-\exp(-F_j/0.25)$. Raw contact has no object/material identifier.

**Proprioception, 7 values.** Use
$[u_L,u_R,\tanh(v_f/1),\tanh(v_{\rm lat}/1),\tanh(\omega/1.75),\tanh(u_L-(v_f-0.35\omega)/1),\tanh(u_R-(v_f+0.35\omega)/1)]$.
The speed divisors are $1D_b/\mathrm{s}$ and the angular divisor is $1.75$ rad/s; the lever in the discrepancy terms is $0.35D_b$. Values combine the preceding delivered commands and actual endpoint body-relative motion. The last two coordinates are fixed motor-equivalent discrepancies, not a desired trajectory or hidden policy. Actual world velocity and force remain observer records; no global position enters the sensor.

**Interoception.** $v_E=E$ and $v_I=I$ are separate exact monotonic readings of actual reserves. They bypass sensory centring only through P's declared body-to-regulator/adapter route.

### 8.4 Persistent chemistry and lawful prehistory

For each chemical component use the whole closed square, including permeable solid interiors:

$$
\partial_t c_a=\nabla\cdot(D(x,t)\nabla c_a)-0.02c_a+q_a(x,t),
\qquad n\cdot D\nabla c_a=0\ \text{on the outer boundary}.
$$

$D=0.5D_b^2/\mathrm{s}$ in medium and $0.025D_b^2/\mathrm{s}$ in every solid, including the chemically silent mover and organism. There is no added advection, absorption or displacement term. Moving solids change diffusion coefficients; they do not delete or manufacture the concentration already present. Finite permeability is one explicit realization of the accepted solid-aware requirement, not a claim that impermeability was accepted.

Use an $80\times80$ finite-volume grid with cell width $0.25D_b$ and field step $0.01$ s. Integrate occupied cell area geometrically; combine solid/medium diffusivities harmonically using their area fractions, and adjacent cell coefficients harmonically at faces. Integrate emitter area within each cell to conserve declared total emission. Backward Euler uses ending geometry and source stock, with conservative face fluxes, decay and emission. Proposed linear-system acceptance uses relative residual $10^{-10}$ and a declared floating-point tolerance $10^{-12}$ for diagnostic classification, not a scientific success threshold. The nonnegative-system solution must not be repaired by silently clipping negative concentrations; a negative/non-finite field outside declared arithmetic error is an apparatus failure, and even an arithmetic-level anomaly is recorded for solver review.

At birth, first choose a uniform mover time-phase and retain it. Start fields at zero at $t=-600$ s and evolve the same field law with the same moving block trajectory to $t=0$, with full sources and no organism. Sources remain full because there is no extraction. The 600 s proposed prehistory covers 20 mover periods and 12 chemical decay times; it is a specified finite physical history, not an asserted equilibrium or a convergence test. Insert the organism at $t=0$ without resetting concentration; its finite-permeability footprint changes $D$ lawfully. No organism state is evolved during prehistory.

## 9. Birth, random streams, pause and life boundaries

Choose body position uniformly by rejection from the nominal centre region, retaining only positions with at least $0.25D_b$ surface gap from walls, sources, restorative bodies and the mover at birth. Keep the selected mover phase fixed during position rejection; otherwise phase frequencies would be biased by acceptance area. Draw orientation uniformly and independently from $[0,2\pi)$; start physical velocities at zero. Set $E=0.70$, $I=1$ and every source stock to capacity. Retain sampled positions and all rejected proposals as observer provenance. A fixed 10,000-proposal preparation limit may signal an invalid initial manifest; it must not trigger an easier ecology or a new phase selected for success. Geometric safety is not proof of a reachable first foothold.

Use a proposed deterministic indexed random stream based on SHA-256: hash UTF-8 records consisting of the fixed master seed, stream label, life identifier, draw index and coordinate index, separated by a colon with decimal integer indices and no spaces. Master seed is **0x50A101**. Interpret the first eight digest bytes as an unsigned big-endian integer $n$; use $(n+0.5)/2^{64}$ for a uniform variate and its half-interval for a sign. Fixed anatomical streams omit the life identifier, so the anatomy is one reproducible untrained draw; birth/noise streams include the independent life identifier. Record the complete encoding, digest algorithm identifier and counters. No seed is drawn, inspected for behaviour or selected by this documentation task.

Separate labels cover fixed sensory weights, each fixed matrix/bias, world phase/position/orientation, initial motor phases/$\nu$, each motor-noise drive, and each bank's regulatory perturbations. Native subdivisions, rendering, logging and solver iterations never consume draws. Use the same specified anatomy for independently reset lives; do not inherit learned arrays or secretly search anatomies.

Initialize $\bar s$ from the actual birth transducers; $x=C=0$. Shared sensory rows are independent generic signed directions scaled to norm 0.05. Draw residual entries at signed amplitude 0.001, subtract their group mean and, if needed, scale their group Frobenius norm to at most 0.004. References are exact copies. $H$, use states, $a$, $Z$, $\Theta$ and $\bar\Theta$ start at zero; opening starts at zero. Set each bodily filter to its actual birth reading, avoiding a fictitious improvement pulse.

At $t_0$ there is **no completed wave**, coactivity write or bodily learning update. Set $q_0=0$; form $\phi_0$ from this and actual reserves, draw $\xi_0$, and calculate the first controls. Set packet-mean baselines from instantaneous actual birth emissions: $[x_0,x_0]$, $[u_0,u_0]$ with $z^M_0=u_0=0$, the first applied regulation vector and actual $v_E,v_I$. Contexts start at zero. Motor phases are independent uniform angles; $\nu_0$ is uniform in $[-1,1]$, within its invariant bound but not claimed to be a stationary distribution. Draw the first motor-noise drive, and start the first real interval. The first map write occurs at $t_1$ and cannot influence a read until $t_2$.

Within a life, world state, learned arrays and all traces persist; nothing resets on source contact, separation, repair or a display pause. Nonviability is actual $E\le0$ or $I\le0$; stop at the located terminal physical event and preserve the last valid state. Administrative termination is separately labelled, with no reward or fabricated death event. A proposed local observation-container horizon is 600 s of organism time, an unapproved finite inspection bound rather than a scientific success gate or selected experiment; any later evidential horizon needs explicit authorisation in its run record. Pausing advances neither this horizon nor physical/neural/noise clocks. Reopening a life resumes every state and pending accumulator exactly; a new life begins from newborn conditions.


## 10. One proposed numerical configuration

This annex is one reviewable configuration, not a sweep or an approved adjustment corridor. All values are dimensionless unless a unit is shown. Changing a listed value requires a new manifest and explanation; no automatic outcome-driven tuning is supplied.

| Quantity | Proposed value | Ground, dependence and unverified assumption |
|---|---|---|
| Native body/field/sensor/learning step; wave | $h_n=0.01$ s; $\Delta=0.20$ s | Twenty native samples per wave; numerical adequacy uncommissioned |
| Sensory and motor activity | $\tau_x=\tau_M=0.10$ s | Within-wave response with boundary carryover; not a guarantee of order resolution |
| Receptor means; sensory coactivity | $\tau_s=30$ s; $\tau_C=10$ s | Separate adaptation/coactivity scales; sustained input can disappear |
| All packet means and central traces | $\tau_\mu=60$ s; $\tau_z=5$ s | Fixed across eight channels for this first proposal; finite context only |
| Association relaxation | $S=4,\tau_a=0.20$ s; $\alpha_a=1-e^{-0.25}$ | Section 4's fixed batched dynamics |
| Anatomy | Four sensory channels × 8 units; two four-unit groups/channel; four gate branches; 32 mixed regulatory features | No semantic addresses; fixed limited capacity |
| Sensory recurrence | Each $A_m$ is a signed generic matrix scaled to Frobenius norm 0.25 | Induced Euclidean norm is at most 0.25; isolated bound, not whole-organism proof |
| Context anatomy | Each gate vector norm 0.20, biases independent signs × 0.10; $\epsilon_g=0.05$ | Nonzero mixed-context capacity; can alias important conditions |
| Regulator anatomy | Each $B_q$ row norm 0.25; each $B_v$ row norm 0.50; $b_R$ entries signs × 0.10 | Generic fixed mixing, no learned features or object detector |
| Sensory local formation | $\eta_0=10^{-4}/\mathrm{s}$, $\eta_1=10^{-3}/\mathrm{s}$, $\chi=0.10$ | Coarse changes slower than fine; no behavioural calibration |
| Sensory reference force | $\rho_0=10^{-5}/\mathrm{s}$, $\rho_1=5\times10^{-5}/\mathrm{s}$ | Nonzero coarse drift; references can preserve errors |
| Sensory reference following | Shared 10,000 s; residual 5,000 s | Slower than native exposure and initial opening |
| Pool spring | $\lambda_{W,\min}=10^{-4}/\mathrm{s}$; immature/reclaim each $0.005/\mathrm{s}$ | At birth with $h=0.5$, nominal $\Lambda=0.0076/\mathrm{s}$; this is a rate calculation, not observed retention |
| Opening | $\tau_{\rm open}=300$ s, $o_0=0$ | Supplied continuous availability; no classifier trigger |
| Sensory bounds | Shared norm 0.30; centred residual group norm 0.08 | Exact convex sets in section 6 |
| Sensory initialization | Shared norm 0.05; residual draw amplitude 0.001 and group cap 0.004 | Small generic untrained structure with exact matching references |
| Query floor | $g_{\min}=0.10$ | Access floor at association input, not recovery of erased receptor information |
| Association formation | $\eta_H=10^{-4}/\mathrm{s}$ | Conservative uncalibrated rate; maximum sensory outer-product norm is 128, giving pre-gate per-wave increment at most 0.00256 |
| Association preservation | $\lambda_{H,\min}=10^{-4}/\mathrm{s}$, $\lambda_{\rm unused}=0.001/\mathrm{s}$, $\tau_v=30$ s, $\epsilon_v=0.01$ squared activity units | Nonzero decay and explicit sampled use; no confidence score |
| Association bound | Frobenius radius 0.10/map | Deliberately fading frozen-query regime; weak initial association remains a risk |
| Bodily filtering and eligibility | $\tau_b=2$ s per need; $\tau_e=5$ s | Credit trace spans 25 waves, including P's extra query latency; causation still ambiguous |
| Bodily learning/reference | $\eta_E=\eta_I=0.05$; $\rho_E=\rho_I=10^{-4}/\mathrm{s}$; reference time 5,000 s | Separate but equal proposed rates, not a combined need |
| Bank bounds and exploration | Row radius 1; $\sigma_E=\sigma_I=0.10$ | Applied independent signs once per wave; saturation/credit bias remain visible |
| Need and output biases | $d_{0,E}=d_{0,I}=0.25$; $b^h=0$; $b^\kappa=\log(0.2/0.8)$; $J_{\max}=0.50$ | Without trial/learned effects, support 0.5 and attenuation 0.2; these are supplied biases |
| Motor generation | $a_L=a_R=0.25$, $b_L=b_R=0.10$; periods 7 s and 9 s; $\tau_\nu=1$ s; drive refresh 0.5 s | Unequal untrained rhythms, no source-following |
| Motor feedback and output | $K_p$ signed generic Frobenius norm 0.10; $D_M$ endpoint selector; $u_{\max}=1$ | Weak raw body feedback; no richer packet or extra regulator input |
| Physical configuration | Geometry/materials, force/cost/transfer/repair/field parameters exactly as section 8 | All constitutive values unmeasured and uncommissioned |
| Arithmetic and storage | IEEE-754 binary64 for state, equations and exact snapshots; integer scheduler counters; deterministic array order | Same-version resume required; cross-platform bit identity not presumed |

Generic signed directions mean fixed sign entries from the declared random stream, normalized to the stated norm. If a centred initialization is identically zero it remains zero rather than redrawing until a “better” pattern appears; the rule does not inspect outcomes. Numeric constants named differently in this document are distinct configuration fields even when their proposed values coincide.

The association-rate bound above limits one raw write relative to the map radius under the extreme coordinate bounds; it does not establish a biologically meaningful rate. Small initial cortical responses may make actual association much weaker. That is a visible risk of this uncalibrated proposal, not grounds for covertly increasing gain until learning appears.

Implement later, if separately authorised, as one local CPU process with explicit fixed arrays, one local inspection window and ordinary configuration/record files. The construction contract is the equations, ordering and record schemas here; its later implementation manifest must pin language/runtime, array and display-library versions and the arithmetic/contact/field solver implementation. There is no service architecture, database, cloud account, Atlas schema, plugin system or job platform to construct.

## 11. Observation, inspection and future verification

### 11.1 Record contract and cost

Use a human-readable configuration/identity JSON, binary64 array snapshots, append-only native/wave tables and variable-length physical event records. Files have explicit schema/version, units, coordinate order, physical timestamps, life/record identifiers, seed/counter state and completeness checksums. These identifiers belong to the observer, not the learner. Keep independent lives separate without calling this an experiment registration.

| Cadence | Required record |
|---|---|
| Every native boundary, 100 Hz | All 29 raw sensory values, actual separate E/I, body pose/velocity, delivered commands and actuator forces, cortical $x$, motor tendency/generator state, applied controls, source stock/exchange summaries, integrity damage/repair, and component-wise formation/coarsening/reference/projection summaries by group |
| Every actual contact subinterval/event | Collider identity for observer only, geometry/time/normal impulse/relative speed, material, requested/actual transfer, source debit/body credit, two renewal increments, effort/basal cost, damage, repair and terminal-event location |
| Every handoff, 5 Hz | Actual $b$, old means, $\beta,z,\psi$, $g,G,y$, initial/final $a$, final $q$, applied old/new controls, $\phi$, old/new perturbations, separate $m,\ell,Z,\Theta,\bar\Theta$, map-use scores/states, map norm/update/projection summaries, and ordering counters |
| Every 10 s and at pause/end/failure | Full reconstructible body/world/organism state: fields, stocks, source/mover phase, raw/contact/proprioceptive caches, $x,\bar s,C$, all $W$ components/references, packet endpoint caches and currently delivered command, $H$, use, $a$, packet means/traces/partial accumulators, $\Theta$/references/eligibility, motor phases/noise/filter state, held return/controls/features/perturbations, random counters and next scheduled events |
| Per manifest and record boundary | Exact sources/decision/spec hashes, code/runtime identity when it exists, settings, initialization samples/rejections, record-loss status, start/stop reason and administrative horizon |

Full $H$ matrices need not be duplicated at every wave. Exact snapshots plus recorded physical inputs, draws and deterministic update order must permit reconstruction of intermediate structural changes and their separate terms. Verify that capability before claiming it; sampled norm plots alone are insufficient. A selected time in the inspector can reconstruct detailed rows from a snapshot rather than pretending they were logged at higher resolution. Preserve both the reconstructed-state provenance and any numerical mismatch.

For storage planning, $H$ occupies 708,864 bytes in binary64; two $80\times80$ fields occupy 102,400 bytes. A complete snapshot is approximately 1 MB including remaining states. A conservative planning allowance of 256 binary64 native scalars, 8,192 wave scalars and a 1 MB snapshot every 10 s is about 2.3 GB/hour uncompressed, plus contact/event metadata; actual schema widths must be counted and reported. This is an estimate, not measured throughput. The proposed 600 s inspection container is roughly 380 MB before variable events/compression. Lossless compression is allowed, silent downsampling is not. On storage failure, mark an incomplete record and stop safely; do not continue an apparently complete evidential life.

### 11.2 One inspectable visual interface

Provide three synchronized views, with pause, single-step after verified state continuity, replay of saved records and a selectable physical time.

1. **World/body:** actual pose/path, square walls, sources and stocks, restorative surfaces, moving block, contacts, actual E/I and optional light/chemical overlays. Labels, material/source IDs and stocks are prominently observer-only.
2. **Organism:** raw inputs; receptor mean/residual and cortical activity; completed/centred packet and trace; ungated gate inputs versus gained direct query; final evoked content; separate bank logits/consequence terms; applied support/current/attenuation; internal motor tendency, command, force and achieved motion.
3. **Development:** shared/fine sensory parameters, local-formation/spring/reference contributions, opening, association/use/decay, separate regulatory learning/references, together with physical context and record completeness. Distinguish displayed measurements from reconstructions.

Display speed never changes simulated time, draw indices or update counts. Do not expose live “helpfulness,” reward tuning, body refill, parameter rescue or source relocation controls on the organism view. A future authorised diagnostic alteration creates a separate preserved-state record; it cannot alter the original life.

### 11.3 Evidence distinctions and accounting

D1 requires separate reporting of:

- Immediate participation and motor effects from already-existing learned parameters.
- Lasting changes in $H$ and $\Theta$ and their references.
- Lasting sensory $W$/fine-residual/capacity changes, and whether those changes contribute functionally.
- Persistent physical context, bodily condition and transient $x,a,z,\ell,Z$, which can change later response without establishing sensory development.

At every inspected recurrence, compare actual accessible inputs, trace history, current support and physical circumstances before attributing altered response to a weight change. Preserve the functional input/output calculation as well as coefficient magnitudes. Group support can be useful because of a common signal; norms of fine residuals do not establish their usefulness. Direct body/bias regulatory competence must not be relabelled sensory co-development.

Record encounter opportunities and nonencounters without exposing event labels to the organism. For each geometric source and restorative body, record first actual contact, contact intervals, absence of contact, intake/repair amount, departure and subsequent contact. Use “revisit” only after a positive-duration separation; keep raw intervals so a different later observer definition is recoverable. Separate fractions over all lives, over lives with an opportunity, and over lives that already encountered the object. Never report a conditional statistic as unconditional, omit failures before first encounter, or hide censoring at the administrative horizon.

Record $A_U$, static centre-free area, time-dependent free area under the mover and the intersection of free regions over a complete mover cycle as distinct quantities. Use exact fixture Minkowski geometry with the organism disk; numerical area estimates must state approximation resolution. The fixed layout suggests bypasses but is not a commissioned navigation or repair-access proof.

Stock accounting includes source renewal during residence, so total intake need not be bounded by stock observed at arrival. For repair, distinguish gentle contact at full integrity from actual positive recovery under damage. Record energy cost during restoration and subsequent departure; mere wall residence is not proof of a usable repair route.

### 11.4 Proposed verification obligations, not executed tests

Before a later commissioned claim, verify source-to-array dimensions, read-before-write order, no hidden input routes, reserve conservation, correct contact stress/repair, sensor visibility, solid-aware field continuity, newborn baselines and exact pause/resume. Numerical tolerances evaluate arithmetic/solver correctness, not developmental success.

Any independently controlled trajectory used to inspect physical reachability, a diagnostic source/controller or an observer replay remains separately identified apparatus work. It is not installed as P, counted as P's experience or used to pretrain the organism. Commissioning must inspect the complete coupling, including usable recovery from damaged states and return to energy; a convenient pristine-body path is insufficient.

Passive records establish chronology and association, not causal attribution to lasting sensory change. Preserve the capability for a later, separately authorised comparison of acute return dependence, pathway influence during development, and functional contributions of sensory versus associative/regulatory structure on preserved state. No intervention matrix, trial sequence, allocation, statistical success threshold or preregistration is selected here. Observer replay never becomes learner replay or a hidden episode store.

No automatic adjustment corridor is proposed. Apparatus findings can motivate a documented batch revision with its grounds and exact difference; an evidential configuration cannot be patched retrospectively or tuned mid-life to rescue the candidate.

## 12. Analytical and documentation checks

The following are contract checks, not numerical experiments:

| Check | Result or obligation |
|---|---|
| Matrix dimensions | Sensory $8\times d_m$ rows, native recurrent $8\times8$, gate $164-p_m$, map $p_m\times p_n$, regulator $32\times164$/$32\times2$, bank $12\times33$, feedback $2\times15$ and selector $2\times8$ are compatible. |
| Pool centring | Mean-subtracted local residual pressure, common group spring, matching centred references and centred projections preserve the declared subspace. |
| Bounded fast states | Frozen-input exponential sensory/motor updates and convex associative updates preserve their stated activity bounds; learned projections bound the relevant parameters. This is not whole-loop stability. |
| Clock dependence | Native learning increments use elapsed seconds; coactivity and bodily learning happen once per real wave; map use receives one $\Delta$ update. Four relaxation sweeps do not create four encounters. |
| No instantaneous support loop | Query at $t_k$ reads $h_{k-1}$; new $h_k$ first changes the following query. The walkthrough follows the same indices. |
| Credit causality | $m_k$ uses old $\ell$; $Z_k$ uses previous applied $\xi,\phi$; new draws occur after the bank update. |
| Sustained input limitation | If all relevant receptor residuals fade and all accessible traces/centred packets lose a distinction, a positive query floor cannot recreate it. Actual E/I and current motor feedback remain their declared separate routes. |
| No physical evocation credit | Only actual exchange/repair changes physical reserves. Recalled bodily/regulatory content can change controls, not accounting. |
| Identity | Exact P parent and handoff verified; current formatted supporting versions separately identified. Historical hashes are not misrepresented as current-file hashes. |

## 13. Remaining review choices and departures

D1–D3 and the walkthrough requirement are accepted and are not pending again. The complete specification is now a proposal to review, with the following tightly scoped completion choices visible:

| Item / source gap | Proposed completion and why it matters | Strongest relevant alternative / consequence |
|---|---|---|
| Packet emission details — P section 3 | Endpoint E/I; one held regulation vector. Fixes dimensions and available temporal content. | Mean/endpoint body emissions or duplicated controls require a separately recorded packet configuration and dimension review; not silently borrowed from R. |
| Motor-return decoder — P section 7 | Select centred endpoint-command block, without adding back a mean. Makes exact motor arithmetic inspectable. | Another explicitly declared native block/combination changes this completion; no richer R packet is installed. |
| Use ODE/handoff interface — P sections 4.3, 9 | One sampled final old-map use score; old use determines current decay. Resolves timing without extra read/write confirmation. | Substep-integrated use under a fully specified physical realization may differ and needs a reviewed timing revision. |
| Frozen associative regime — P section 4.4 | Four sweeps, linked $\alpha/\Delta$, map radius 0.10 and conservative formation rate. Intentionally fading and uncalibrated. | A less restrictive P norm/dynamical regime is a quantitative alternative; it cannot inherit this contraction argument or be tuned invisibly. |
| Constitutive world laws — Base World section 14.1 | Section 8's complete proposed laws/configuration retain accepted geometry and functional ecology. | Different explicit physical realizations can be reviewed; no authority here to change them after observing failure or to reopen accepted choices without a concrete conflict. |
| Numerical and tooling fidelity | Binary64, deterministic ordering, complete records; actual implementation/runtime versions remain a later build-manifest obligation. | Another implementation must demonstrate the same contract or record differences; documentation does not claim execution equivalence. |

**No changed P mechanism or accepted Base World functional choice is adopted.** We found gaps in emission, discretization and physical realization, not a contradiction requiring a P–R synthesis. The current P source-hash discrepancy was reconciled as formatting/whitespace, with an exact parent recovered; it does not remain a parent-selection question.

Review should decide whether these proposed completions, restrictive initial associative regime and physical configuration accurately express the intended first P construction. Eventual usefulness, sensory accessibility under adaptation, delayed credit, nuisance retention, bank interference and repair discoverability remain empirical uncertainties. They do not require proof before this specification can be reviewed, and they must not be hidden by a successful-sounding walkthrough.

## 14. Sources and stopping boundary

Primary references are the [exact P parent](../../90_SOURCES/p_specification_authority_2026-09-20_83a00674/exact_parent/LOOM_ASSOCIATIVE_REGULATORY_CANDIDATE_v0_1_DISCUSSION_DRAFT.md), [authority handoff](../../90_SOURCES/p_specification_authority_2026-09-20_83a00674/LOOM_P_SPECIFICATION_HANDOFF_2026-09-20.md), [new decision](../../40_DECISIONS/DECISION-P-SPECIFICATION-2026-09-20-83a00674.md), [direction](../../90_SOURCES/direction_2026-09-18/LOOM_DEVELOPMENTAL_DIRECTION_v0_1_REVIEW_DRAFT.md), [Current State](../../90_SOURCES/reference_7ada2b300fa1/00_LOOM_CURRENT_STATE.md), [Design Frame](../../90_SOURCES/reference_7ada2b300fa1/docs/developmental_ecology/DEVELOPMENTAL_ECOLOGY_DESIGN_FRAME_v0_2.md), [Coupling](../../90_SOURCES/reference_7ada2b300fa1/docs/developmental_ecology/PRIMITIVE_ORGANISM_WORLD_COUPLING_SPEC_v0_1.md), [Base World](../../90_SOURCES/reference_7ada2b300fa1/docs/developmental_ecology/BASE_WORLD_COMPLETION_v0_1.md), [decision ledger](../../90_SOURCES/reference_7ada2b300fa1/docs/developmental_ecology/DEVELOPMENTAL_ECOLOGY_DECISION_LEDGER_v0_2.md), [comparison](../../90_SOURCES/candidate_comparison_2026-09-20/REVIEW_AND_RECONCILIATION_NOTES.md) and unchanged [readiness review](../../50_SESSIONS/2026-09-20-readiness-01ad3c47/DESIGN_TO_TEST_READINESS_REVIEW.md). R is preserved as an alternative, not a component source.

[SOURCE_IDENTITIES.json](SOURCE_IDENTITIES.json) gives filenames, exact current/original hashes, recovered-parent custody, author labels and source scope. [The completion report](COMPLETION_REPORT.md) records actual read coverage and checks. Missing full original-chat material and earlier user notes limit historical attribution; the present explicit commission supplies the authority needed here. No missing source prevents this draft within its stated scope.

This document and its walkthrough are ready for design review. Nothing has been implemented, simulated, commissioned, preregistered or run; no experiment identifier, Git operation or actual Loom-repository change is created by this commission.
