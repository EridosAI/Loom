# Loom — Contextual Association with Learned Participation

**Version:** 0.1 — DISCUSSION DRAFT  
**Prepared:** 2026-09-20  
**Author:** Astra, design seat  
**Status:** One proposed, parameterised mechanism account; not a mechanism ruling or an implementation specification.  
**Authority:** Design discussion only. No organism implementation, experiment number, preregistration, commissioning execution, run, or repository change.  
**Foundation reference:** `EridosAI/Loom@7ada2b300fa12a26b0daf40b1fa5682243ff6625`, from the supplied sources; not a new verification of remote HEAD.  
**Working interpretation:** `LOOM_DEVELOPMENTAL_DIRECTION_v0_1_REVIEW_DRAFT.md` (2026-09-18). Full-chat export audit remains pending and does not block this proposal.

> **Working hypothesis:** Association learns relations among experienced signals. A regulator learns how strongly those relations and presently available sensory distinctions participate. The same learned sensory-participation response can have a rapid expression effect and a much slower retention effect. Bodily consequence changes the regulator through an explicitly supplied learning rule, not through a hidden ability to recognise success.

## 0. Scope and the conditional concession

This document supplies one concrete account rather than another catalogue. It is a new synthesis; its equations are not experimental results or previously accepted Loom laws.

The candidate contains a deliberately conventional element: **separate energy- and integrity-sensitive perturbation/consequence learning of regulatory parameters**. It is reinforcement-like learning of an action-generating process, even though it has no critic, forecast, trajectory optimiser, semantic action set or combined bodily reward. It therefore needs an explicit methodological exception under a strict reading of the existing no-policy-optimiser direction. Jason's agreement to work through a candidate is not that exception's ratification.

The candidate is conditional on considering that concession. Rejecting the concession leaves the bodily-learning link unselected; it does not mean this document has secretly specified an alternative reward-free solution.

The principal new interaction is **shared participation control**: a context-dependent regulatory output both affects a sensory distinction's current contribution to association and reduces the pooling force on the corresponding fine parameters. This is proposed because current participation can have consequences before a tiny structural change becomes behaviourally measurable. Whether expression-use is a sound proxy for retention is an explicit hypothesis, not a theorem.

The first target remains practical history-dependent adaptation, not rich episodic reconstruction. No word channel, curriculum, additional memory cortex, hemispheric split, or explicit replay store is added. No anticipation capability is prohibited, but predicting the next world state is not the central operation's target.

## 1. What stays outside the mechanism

The accepted body/world supplies light, chemistry, contact, proprioception, actual motor consequences, and separate monotonic energy/integrity interoception. It owns physical stocks, transfer, damage, repair, collision, and capability limits. The mechanism receives neither object identities nor privileged resource position, stock, successful-contact flags, or a correct action.

Write the actual sensed reserves as `v_E` and `v_I`, individually scaled into `[0,1]`. This is a proposed fixed monotonic transduction convention, not a combined health coordinate. Both remain directly available to the regulator and its bodily-learning interface. Neither a recalled reserve nor an attention gate can overwrite them.

Paired commands go through real body mechanics. Actual energy transfer and actual gentle restoration alone replenish the physical body. Basal expenditure remains positive; integrity has no passive decay in the starting world. No physical or numerical commissioning values are selected here. [S1–S3]

## 2. States and roles

| Symbol | Meaning | How it changes |
|---|---|---|
| `s_m` | Raw bounded transducer vector of sensory channel m | Physical sensing; not learned by this model |
| `x_m` | Native-rate, receptor-driven cortical activity | Fast leaky recurrent dynamics |
| `W_m` | Sensory sensitivity, represented through pooled parameter components | Slow receptor-local learning and pooling |
| `b_m` | Emission covering the preceding wave interval | A packet readout, not an episode record |
| `mu_m`, `z_m` | Slow packet mean and fading packet context | Local filters; no timestamps |
| `psi_m` | Centred current packet together with its fading context | Input to associative writes and context conditioning |
| `H_mn,j` | Learned map from channel n into channel m under mixed context j | Actual coactivity, decay and norm bounds |
| `a_m`, `q_m` | Associative activity and returned content in m's coordinates | Recurrent use of the learned maps |
| `Theta_E`, `Theta_I` | Disjoint regulatory response parameters | Separate proposed bodily-learning rules |
| `phi` | Bounded regulator input features of evocation and actual bodily condition | Fixed nonlinear mixing of available signals |
| `h_mg` | Sensory participation/support at an anatomical pool group | Fast regulatory output; changes query gain and slow tie strength |
| `j_i`, `kappa_i` | Additional motor current and enactment attenuation | Fast regulatory outputs, for each of two actuators |
| `Z_E`, `Z_I` | Traces of perturbations that actually participated in regulation | Fading traces; not stored action episodes |
| `ell_E`, `ell_I` | Filtered actual bodily readings | Local bodily filters |
| `u` | Bounded paired motor command | Ongoing motor dynamics plus regulation |

A group index is an anatomical address allocated without concepts. It is not a ball, hazard, source or colour label. Concatenating vectors below is bookkeeping over different native spaces, not a demand that their coordinates acquire the same meaning.

`k` indexes the engineering wave schedule. Neither k nor absolute time is supplied as representational content. Numerical integration steps are not extra learning encounters.

## 3. Native sensory processing and packet formation

For each learned distal/contact/proprioceptive channel, take bounded sensor input and a receptor-local mean:

\[
\tau_{s,m}\dot{\bar s}_m=s_m-\bar s_m,\qquad r_m=s_m-\bar s_m.
\]

A concrete sensory activity law is

\[
\tau_{x,m}\dot x_m=-x_m+\tanh(W_mr_m+A_mx_m).
\tag{1}
\]

`A_m` is a small, fixed, nonsemantic recurrent matrix, generally asymmetric, with an induced norm below one for this candidate's isolated sensory dynamics. `W_m` is learned. This choice provides history sensitivity without an intrinsic future-target loss. A fixed recurrent matrix is an admitted initial capacity, not a learned recurrent cortex claimed by name. The whole developing loop is not certified stable by this local restriction.

For wave length `Delta`, emit

\[
b_{m,k}=\left[\frac1\Delta\int_{t_{k-1}}^{t_k}x_m(t)\,dt,\ x_m(t_k)\right].
\tag{2}
\]

The accumulator turns over at the handoff; `x_m` does not hard-reset. These are statistics of a temporally evolving cortical response, not of an orderless collection of raw readings. Native dynamics can cause different orders to produce different packets. Neither (1) nor (2) guarantees preservation of every important order: aliasing of distinct histories remains a concrete possible failure. No frame numbers, analytic velocities or positional features are appended. The principal `tau_x` scale is to be selected near the intended within-wave span; its exact value is not supplied here.

The motor channel emits the interval mean and final value of the **actual command**, in actuator units. Proprioception separately reports what movement occurred. The regulatory channel emits the applied h, j and kappa values over the interval, not merely the return that suggested them. Energy and integrity have direct monotonic emissions in addition to remaining available as actual bodily inputs.

### 3.1 A specified sensory-local learning pressure

For a sensory row i, maintain `C_m`, a running activity-coactivity matrix, and use

\[
\tau_C\dot C_m=x_mx_m^\top-C_m,
\]
\[
F_{m,i}=x_{m,i}r_m^\top-x_{m,i}^{2}w_{m,i}
-\chi\sum_{j\ne i}C_{m,ij}w_{m,j}.
\tag{3}
\]

The first two terms are an Oja-type normalization template; the last is a proposed correlation-dependent competition term. The combination with nonlinear recurrent activity and hierarchical ties is **not Oja's proved linear model**. It is a specific starting pressure towards recurring sensory structure with less duplicated response. It can preserve nuisance variance, miss useful weak signals, or become redundant despite the competition. No object-learning claim follows. [P1]

`F` contains current receptor-driven activity, not a target from association or the body. Bound every learned parameter component and keep changes small in physical time. Pooling directs how F changes shared and finer components, as specified in §6.

These choices are included to avoid leaving “the cortex learns on its own” as an implementation-sized blank. They are not a renewed claim that a familiar local rule has already earned preference for Loom.

## 4. The central operation: conditioned coactivity, not next-wave prediction

### 4.1 Available state

Centre each completed packet against its prior running mean, then update a leaky context:

\[
\beta_{m,k}=b_{m,k}-\mu_{m,k-1},
\]
\[
z_{m,k}=e^{-\Delta/\tau_{z,m}}z_{m,k-1}
 +(1-e^{-\Delta/\tau_{z,m}})\beta_{m,k},
\]
\[
\psi_{m,k}=[\beta_{m,k},z_{m,k}].
\tag{4}
\]

After beta is formed, the mean update is `mu_m,k = mu_m,k-1 + (1-exp(-Delta/tau_mu,m)) beta_m,k`. Filtered current and recent activity are different physical states, not an attached “this happened at time t” code. Context may last beyond a sensory wave in the centre; this is not a second learned associator.

Representing both blocks lets actual current activity become associated with a surviving trace of another channel. A later cue can therefore evoke earlier-related trace content, rather than being restricted to next-item generation. Finite traces still have finite reach. Repeated symbols and longer overlapping histories can alias; weights do not magically reconstruct an erased episode. The first candidate makes no whole-life recall claim.

### 4.2 Unlabelled context capacity

For target channel m, form nonnegative contextual coefficients from all **other** channels' actual psi values:

\[
g_{mj}=\frac{\epsilon_g+\sigma(v_{mj}^{\top}\psi_{-m}+c_{mj})}
 {\sum_r[\epsilon_g+\sigma(v_{mr}^{\top}\psi_{-m}+c_{mr})]}.
\tag{5}
\]

`sigma` is the logistic function. The vectors v and biases c are fixed small random quantities; their number is a finite design parameter. They supply nonlinear mixed-selectivity capacity, not labelled context regions or an object lookup. This is an innate basis and a limitation: it may fail to resolve important contexts. Association weights learn within that basis. Changing the basis adaptively would be another mechanism, not an omitted implementation detail.

Using other-channel context avoids a direct receiving-channel identity shortcut. It does not exclude indirect loops or make any channel infallible.

### 4.3 Learning encountered relationships

For every ordered channel pair m != n and context branch j, update a bounded map once per actual wave:

\[
H_{mn,j}\leftarrow\operatorname{Proj}_{\mathcal H}
\left[H_{mn,j}+\Delta\left(
\eta_Hg_{mj}\psi_m\psi_n^\top-\lambda_H(v_{mn,j})H_{mn,j}\right)\right].
\tag{6}
\]

Here and below, projection means Euclidean projection onto an explicitly specified convex bounded set: a Frobenius-norm ball for each H map, rowwise Euclidean balls for each Theta bank, and the intersection of component-norm bounds with centred residual subspaces for sensory parameters. The radii remain numerical configuration choices. For continuously integrated sensory parameters, use the corresponding tangent-projected dynamics. These operations have no access to outcomes or labels. The map runs from n's own packet/context coordinates to m's; it is not a shared semantic embedding.

Use-dependent preservation may be made explicit through a leaky map-use state:

\[
\tau_v\dot v_{mn,j}=-v_{mn,j}+
\frac{\|g_{mj}H_{mn,j}a_n\|^2}{\epsilon_v+\|g_{mj}H_{mn,j}a_n\|^2},
\]
\[
\lambda_H(v)=\lambda_{\min}+\lambda_{\rm unused}(1-v),\quad\lambda_{\min}>0.
\tag{7}
\]

Actual use reduces loss; it does not add another positive co-occurrence observation. Recalled but mistaken relations can also receive this protection. The nonzero residual decay is a design bias, not a guarantee of correct forgetting.

Writes use actual receptor-compartment packets, current bodily readings and actual motor/regulatory participation. They do not use each recurrent evocation as another delivered encounter. Ordinary static contact still supplies new physical-time observations. Removing invented repeated observations is not a claim that existing representations are untouched by past feedback.

Equation (6) stores contextual second-order relationships. It is not a full joint-density learner or a guarantee of coherent multimodal completion. Multiple relations may superpose into an unrepresentative mixture. Nonlinear context and recurrent use offer capacity, not a proof that this problem is solved.

### 4.4 Calling forth

For a one-level pool, let `G_m(h)` repeat each anatomical sensory-group gain over that group's packet and trace coordinates:

\[
G_{m,g}(h)=g_{\min}+(1-g_{\min})h_{m,g},\qquad 0<g_{\min}<1.
\tag{8}
\]

With nested pools, replace h in (8) for each sensory unit by the product of h values along its pooling path, and repeat that unit gain over its mean, endpoint and central-trace coordinates. This is a specified gating hierarchy, not a claim about semantic levels. This gain is one for bodily, motor and actual-regulation channels in this version; it cannot hide actual bodily state. Query input is `y_m=G_m psi_m`, using the already-applied regulatory state from the previous interval.

Use persistent associative state with S relaxation updates per handoff:

\[
q_m^{(r)}=\sum_{n\ne m,j}g_{mj}H_{mn,j}a_n^{(r)},
\]
\[
a_m^{(r+1)}=(1-\alpha_a)a_m^{(r)}+
\alpha_a\tanh(y_m+q_m^{(r)}),\qquad 0<\alpha_a\le1.
\tag{9}
\]

The final q is recomputed from the final a. S is an implementation-resolution parameter, not recalled sequence length. Start from the preceding associative activity, not from zero every wave. The reads use H before that handoff's new coactivity write.

No desired next packet enters (6) or (9). The internal updates refine present associative activity; they do not advance an imagined world one step each. A cue may activate related earlier or later material according to the learned maps. It is not promised to uniquely recover an ordered whole.

Bounded a and H bound the return. They do not guarantee useful attractors, correct certainty or a stable developing loop. A stricter contraction setting would narrow this to fading cue-driven association; it cannot simultaneously be sold as unrestricted multistable imagination. This candidate leaves the actual coupling regime to quantitative design and makes no confidence claim from settling speed.

**Where recall lives:** q and a can carry channel-related content without matching current receptor input in that channel. Sensory query gain is not expected to manufacture that content; it remains in the associative/return activity. In this version, the sensory cortex does not receive q as a substitute receptor image.

## 5. Regulation: a learned response to evocation

The regulator receives the full evoked q, including recalled regulatory material, plus actual v_E and v_I:

\[
\phi_k=\left[1,\ \tanh(B_q q_k+B_v[v_E,v_I]^\top+b_R)\right].
\tag{10}
\]

The B matrices are fixed generic projections, not semantic feature extractors. The constant permits a tonic response; it is not a self or truth token. The regulator has no direct route from the full raw scene to an independently capable policy: its context arrives through the learned association. Body-only habits remain possible and must not be mistaken for associative development.

For each bodily bank d in {E,I}, produce trial logits

\[
L_{d,k}=\Theta_{d,k}\phi_k+\sigma_d\xi_{d,k}.
\tag{11}
\]

Each xi component is an independent symmetric bounded variation (+1 or -1) at this declared regulatory cadence. It is actually applied. Holding the resulting controls over the next interval gives finite-duration variation; independent noise is not redrawn at every numerical integration substep. The birth motor process is separately temporally structured.

Theta_E and Theta_I are distinct arrays with separate updates. Each bank has access to signed motor-current, brake and sensory-support outputs. No anatomical rule gives energy only “go” or integrity only “stop.”

Let the supplied dimension-specific need gains be

\[
D_d(v_d)=d_{0,d}+(1-d_{0,d})(1-v_d),\quad 0<d_{0,d}\le1.
\tag{12}
\]

A nonzero floor leaves room for anticipatory restraint while intact. The gain is a proposed physiological preference, not a learned route.

For a sensory pool group g,

\[
h_{m,g}=\sigma\left(b^h_{m,g}+D_E L^h_{E,m,g}+D_I L^h_{I,m,g}\right).
\tag{13}
\]

For motor i,

\[
j_i=\frac{J_{\max}}2\left[\tanh(D_E L^j_{E,i})+\tanh(D_I L^j_{I,i})\right],
\]
\[
\kappa_i=\sigma\left(b_i^\kappa+D_E L^\kappa_{E,i}+D_I L^\kappa_{I,i}\right).
\tag{14}
\]

This is physical superposition into several control variables, not computation of a joint desirability score. It can still create cancellation, competition and effective trade-offs; separate arrays are not proof of philosophical independence or absence of optimisation. Both banks remain reinforcement-like under §8.

Applied h, j and kappa—not the suggestion q_R—form the regulator's subsequent packet. A familiar context can then evoke previously participating regulation through H. The regulator must still execute its learned response; remembering its output does not transfer that function elsewhere automatically.

## 6. The sensory participation–retention link

The current query gain in (8) is the immediate effect. For a pooled sensory parameter, h also changes the strength of the force pulling finer differences back together.

For one group, write rows as

\[
w_i=\mu+\delta_i,\qquad\sum_i\delta_i=0.
\]

With `bar F` the group's mean local update tendency from (3), use

\[
\dot\mu=\eta_0\bar F-\rho_0(\mu-\bar\mu),
\]
\[
\dot\delta_i=\eta_1(F_i-\bar F)-\Lambda_g\delta_i
-\rho_1(\delta_i-\bar\delta_i),
\tag{15}
\]
\[
\tau_{\rm ref,0}\dot{\bar\mu}=\mu-\bar\mu,
\qquad
\tau_{\rm ref,1}\dot{\bar\delta}_i=\delta_i-\bar\delta_i.
\]

The pooling coefficient is

\[
\Lambda_g=\lambda_{\min}+\lambda_{\rm immature}(1-o_\ell)
+\lambda_{\rm reclaim}(1-h_g),
\qquad
\tau_{\rm open,\ell}\dot o_\ell=1-o_\ell.
\tag{16}
\]

The opening state is private physiology, initialised at zero, and never an input identifying an encounter. It allows increasing differentiation without a classifier first requesting a missing distinction. High h does not dictate the sign or content of F: it reduces a restoring force on the current fine deviations. Coarse plasticity is slower but not presumed zero; references follow more slowly and can preserve mistakes.

For multiple nested levels, compute each child's mean F minus its parent's mean F and apply the same centred residual law at that level. Use one Lambda per sibling pool, so the centred residual constraint is preserved. Repeat bounded projections within the centred subspace. Fixed equal-size nested groups are an explicit anatomical convenience, not semantic levels. No number of levels is selected. Norm bounds and bounded fine contributions limit parameters, not guarantee preserved functional identity.

This is **not** the historical supervised gradient-disagreement trigger. It is a proposed continuous support-dependent spring. It does not implement a separate low-use AND low-disagreement detector. A well-used distinction can be preserved by local sensory pressure or learned support, while unsupported differences tend to coarsen. No guarantee that all useful rare distinctions survive is claimed. Association-map retention is separately stated in (7); association and regulatory parameter capacity are fixed in this first candidate rather than inheriting every historical pooling law. Those structures still learn; adding their own adaptive pooling would be another stated realization choice, not something this draft silently claims.

### Why couple expression and retention?

An almost imperceptible change to fine sensory weights may not affect a bodily outcome until many encounters later. If the only attempted control is that tiny plasticity change, a short outcome trace has little information with which to learn its importance.

Here h also changes the distinction's current availability to recall and action. Its expression effect, after the explicit handoff latency in §9, can therefore be consequential before the long-term structural change is measurable. The same response subsequently supplies retention support when similar cues recur.

This is an explicit additional hypothesis: **useful current participation is a useful guide to longer-term preservation**. It can fail. A vivid nuisance could affect behaviour without deserving greater retention; suppression can hide evidence; novel details need provisional room before their usefulness is established. Positive query floors and receptor-local learning preserve a route for new input, not guaranteed correction.

## 7. Ongoing motor activity, not trajectory playback

A bounded innate source is

\[
o_i(t)=a_i\sin\varphi_i(t)+b_i\nu_i(t),
\quad\dot\varphi_i=\omega_i,
\quad\tau_\nu\dot\nu_i=-\nu_i+\chi_i(t).
\tag{17}
\]

chi is bounded symmetric variation, held at a declared physical cadence; nu starts in its invariant bound. Phase is private generator state, not an age label. Unequal, untrained left/right initial states provide varied movement, not source-following. Amplitudes and rates remain configuration choices requiring bootstrap checks.

Use a bounded motor state

\[
\tau_M\dot z_i^M=-z_i^M+\tanh\left(o_i+[K_pp(t)]_i+[D_Mq_M]_i+j_i\right),
\]
\[
u_i^{\rm command}=u_{\max,i}(1-\kappa_i)z_i^M.
\tag{18}
\]

The symbol `u_i^command` means the paired actuator command (not the noise state nu in (17)). `p` contains current body-relative proprioception/contact; K_p is a fixed small, explicitly recorded anatomical feedback map, without any object/goal inputs. A generic map is a proposed starting assumption, not acquired motor skill. D_M selects the native current-command block of the motor evocation; recent-context blocks remain available to regulation, not played as a tape.

The body then enforces its actual mechanics and capability limits. Neural activity can continue while command magnitudes become small. Logistic braking approaches but does not reach full suppression at finite logits; exact mechanical stillness depends on the body and command balance. A recoverable gentle-contact regime is not proved by this formula.

The initial motor detail is deliberately small for the paired body. It does not claim a learned articulated motor hierarchy. Learned H and regulatory motor-current/brake maps organise this feedback process. That is already a specified learned motor effect without a prepared successful trajectory.

## 8. Provisional bodily learning scaffold

**This section is a conditional proposal, not current doctrine.** It is included so “the regulator learns what works” has an explicit meaning and can be criticised.

For d separately, retain a low-pass actual bodily reading:

\[
\ell_{d,k}=\ell_{d,k-1}+\alpha_{b,d}(v_{d,k}-\ell_{d,k-1}),
\quad\alpha_{b,d}=1-e^{-\Delta/\tau_{b,d}}.
\]

Use the bounded high-pass change signal

\[
m_{d,k}=\frac{v_{d,k}-\ell_{d,k-1}}{\tau_{b,d}}.
\tag{19}
\]

Initialise ell to the actual birth reading. This avoids a fabricated birth-improvement pulse. This signal mixes the consequences of effort, uptake, damage and repair; it is not privileged knowledge of which event caused them. Constant negative energy drift can still produce negative m. No source-transfer or collision-identity flag enters it.

Before choosing the new perturbation, retain previous actual regulatory participation:

\[
Z_{d,k}=\alpha_e Z_{d,k-1}
+(1-\alpha_e)\xi_{d,k-1}\phi_{k-1}^{\top},
\qquad\alpha_e=e^{-\Delta/\tau_e}.
\tag{20}
\]

Then update only that dimension's regulatory bank:

\[
\Theta_{d,k}\leftarrow\operatorname{Proj}_{\mathcal T_d}
\left[\Theta_{d,k-1}+\eta_d\Delta\,m_{d,k}Z_{d,k}
-\rho_d\Delta(\Theta_{d,k-1}-\bar\Theta_{d,k-1})\right].
\tag{21}
\]

Use `barTheta_d,k = barTheta_d,k-1 + (1-exp(-Delta/tau_ref,d)) (Theta_d,k-barTheta_d,k-1)` after the update. Theta and its references start at zero; Z starts at zero. Generic fixed feature biases and actual trial variation permit later nonzero responses. Initial packet means, receptor means and context filters are set from the first available actual readings without fictional earlier experience; association H, use states and associative activity start at zero. Sensory shared weights start small and untrained, with tiny independent fine residuals and matching references. Birth motor and regulatory biases must permit activity and nonzero sensory access. Exact scales and random seeds are configuration choices, not fitted to developmental success.

There is no update with a shared `m_E + w*m_I`. No H or W receives this bodily score directly. Ordinary associative writes continue for beneficial, harmful and neutral experience. The sensory loop is affected indirectly when a learned h changes expression and pooling support.

The perturbation factor matters. Merely multiplying bodily improvement by the existing response would strengthen whatever happened to be active. A signed exploratory variation gives a hypothesis about which variation changed the outcome. In an ideal one-dimensional, frozen context, the identity

\[
\mathbb E_{\xi\in\{-1,+1\}}[\xi\,f(l+\sigma\xi)]
=\tfrac12[f(l+\sigma)-f(l-\sigma)]
\]

shows the relation to directional search. The organism is not supplied both outcomes of one moment. The identity explains an averaging principle, not a counterfactual oracle. In a changing recurrent organism with finite traces, saturation, two interacting banks and changing sensory coordinates, (21) is **not certified as an unbiased policy gradient** and has no convergence guarantee.

This is related to conventional stochastic reinforcement and perturbation-based learning. Williams gives a primary reinforcement-learning lineage; Miconi demonstrates related delayed reward-based recurrent learning under supplied tasks. Neither proves this continuous, two-currency, support-and-retention construction. [P2, P3]

### Boundaries and failure conditions of the scaffold's explanation

A later bodily consequence arriving after Z has faded cannot be correctly attributed merely because Theta is long-lived. The next-encounter mechanism reduces the requirement for a cortical trace to span repeated visits; it does not abolish the original action/consequence bridge.

The short-term signal can favour energy-saving immobility, discourage useful costly travel, credit coincidental intake, or interrupt energy-costly repair. Without immediate integrity loss, it may learn little about eventual danger. These are real limitations, not implementation bugs to conceal. Separate banks can conflict through their shared actuators.

The scaffold supplies preferred change directions. It does not demonstrate emergence of valence, love or a desire to exist. It might remain necessary after learning. Removing it later is another hypothesis.

## 9. One handoff and one subsequent interval

This ordering removes an otherwise ambiguous instantaneous loop; it is a candidate engineering convention, not a semantic event boundary.

1. Finalise actual packets from the interval just lived. Include applied regulatory controls, generated command, sensed movement and actual reserves. Compute beta, z and psi. Do not reset the sensory, associative or eligibility states.
2. Apply (19)–(21) using the previous interval's perturbations and their traces. The new variation has not yet been sampled and cannot receive credit for an already observed bodily change.
3. Compute contextual coefficients and perform the declared S associative updates using the previous H and the already-applied sensory gain. No new coactivity write occurs between those internal iterations.
4. Form phi from q and actual bodily condition. Sample the new trial variations. Produce h, j and kappa for the coming interval.
5. Write H once from actual psi and update its use state and packet means. This write is not reread to create an extra within-handoff “confirmation.”
6. Continue native sensory dynamics, sensory-local learning, pooling, spontaneous activity and body-feedback motor operation. New h affects query participation at the next delivery and retention during this interval. The actual world supplies the next bodily and sensory consequences.

A one-wave query-gain latency is explicit in this version; motor feedback remains faster. A new sensory-support perturbation therefore has an additional handoff before its query-mediated motor consequences can be observed. Its credit trace must cover that physical delay; a one-wave outcome estimate is not asserted sufficient. That latency can still act within an extended encounter. Removing it requires specifying the resulting coupled algebraic/dynamic loop, not silently reading h before it exists. Reading and writing are computational suboperations every wave, not separate train/run phases or alternate life episodes.

## 10. What happens across recurring encounters

An early sensory pattern can participate in chance motor and regulatory variations. Contact and the subsequent body state enter the same continuing history. H learns those relationships regardless of their desirability. If the bodily scaffold finds statistically useful correlations with the applied perturbations, Theta changes slightly.

On recurrence, learned H supplies a context-dependent q. Changed Theta transforms that q into a different pattern of h, j and kappa. The sensory cortex is currently processing a related encounter, so any changed retention support has a present anatomical target. No address of the original cortical packet is needed.

A repeatedly damaging relationship can become easier to evoke while the associated motor expression becomes more selectively restrained. If greater current participation of a sensory group helps produce that restraint, learned h can also support its fine parameters against coarsening. These are possible outcomes, not encoded identities or guaranteed results.

When the source is depleted or the mover's position differs, changed sensory, trace and body context can change the recalled/regulatory pattern. If the representation does not distinguish those conditions, the candidate cannot be credited with context-sensitive regulation simply because an outcome was once useful.

## 11. Analytical checks and admitted limitations

These are reasoning checks, not executed tests, numerical gates or a preregistration.

| Check | What the equations support | What they do not establish |
|---|---|---|
| H = 0 | q is zero; the regulator has bodily/bias features but no rich sensory context bypass | That learnt H becomes useful |
| No matching receptor input | Other cues can generate q for that channel | Accurate or episode-specific recall |
| Association iterations | No extra coactivity writes; no target is the next packet | No indirect self-confirmation |
| Regulation and evidence | Query gain cannot reach zero; raw sensory-local learning and actual bodily input remain | Guaranteed correction of every mistake |
| Bodily accounting | Recalled reserves cannot alter physical reserve or the actual-input learning channel | Acquired viability-seeking behaviour |
| Slow remodelling | W/H/Theta changes have explicit physical-time rates | That small parameter changes preserve perceptual geometry |
| Two bodily dimensions | Separate m, Z and Theta, without a shared outcome score | No competition, implicit trade-offs or optimisation interpretation |
| Harmful knowledge | Association writes are not negated by bodily harm | That useful restraint will actually be learned |
| Use-dependent preservation | Retrieval can lower H decay without adding occurrence count | Correctly calibrated certainty or immunity to false retention |
| Endogenous activity | Bounded structured command tendencies exist before learning | Discoverable first footholds, rich exploration or escape from every pause |

Main scientific liabilities:

- Conditioned covariance can be too weak for coherent higher-order associations; recurrence can mix incompatible content.
- Fixed mixed-context projections may alias important situations; sensory changes move the addresses used by learned H and Theta.
- The sensory-local learning pressure may encode high-variance nuisance rather than the useful low-amplitude distinctions.
- The shared expression/retention control can favour what is immediately useful and suppress details with delayed developmental value.
- Associative self-confirmation is restricted, not impossible: H affects h, h affects W, and W affects future actual packets.
- Retaining actual regulatory activity can produce habit or a self-maintaining bias. It does not automatically relocate regulation out of its original cortex.
- Bodily trend learning may be too short-sighted or too noisy to exploit the accepted repair/travel ecology.
- Competent behaviour could reside mainly in regulatory response weights. Improved navigation alone would not establish the intended sensory co-development.

## 12. Supplied, learned, and not yet chosen

**Supplied in this candidate:** random recurrent and mixing bases, pooling anatomy, nonlinearities, body-specific signal units, activity and eligibility timescales, norm bounds, independent exploration, opening and reference laws, a rudimentary anatomical motor-feedback map, positive sensor-query floors, and the signed bodily-learning scaffold.

**Intended to develop:** sensory sensitivities and fine residuals, contextual cross-channel relations, context-dependent evocation, and regulatory responses affecting selection, motor participation and retention.

**Not supplied:** object names, a resource-finding policy, a correct response to the mover, future-state targets, learned world dynamics, an episodic archive, or an external evaluator choosing actions.

**Not yet chosen even provisionally numerically:** channel sizes, context width, pooling depth, time constants, update rates, noise amplitudes, norm limits, sensor/motor scale and body/world numerical laws. Those require a quantitative configuration and Jason's separate review. This document does not claim a complete simulator-ready specification merely because the learning equations are explicit.

The two largest mechanism decisions for review are (a) whether shared sensory participation and retention is the right causal link, and (b) whether the declared bodily-learning exception is an admissible first scaffold. Rejecting either changes this candidate; it is not a parameter tweak. Other local laws also remain proposals, not accepted by presenting this account.

## 13. Source and synthesis record

### Project sources

- **S1:** `00_LOOM_CURRENT_STATE(2).md`, supplied merged-snapshot orientation; current mechanisms remain open.
- **S2:** `PRIMITIVE_ORGANISM_WORLD_COUPLING_SPEC_v0_1(2).md`, read with the Base World note; especially §§5–9, 13–18. Its supplied preparation-status header is known to differ from the merged header; no new repository-status claim depends on it.
- **S3:** `BASE_WORLD_COMPLETION_v0_1(1).md`, particularly §§6–8 and 13; actual transfer, recovery, learning/run boundaries.
- **S4:** `Loom_Continuation_2026-09-18/LOOM_DEVELOPMENTAL_DIRECTION_v0_1_REVIEW_DRAFT.md`, especially §§4–11 and 14–15; read locally for this design task.
- **S5:** `Pasted text.txt`: Jason's next-encounter proposal and recipient-specific sensory support/motor restraint. This is the source of the target relationship, not of the equations.
- **S6:** `LOOM_INDEPENDENT_MECHANISM_INVESTIGATION(1).md`, §3.1 and Candidate A: antecedent contextual covariance/return and separate perturbation/consequence ideas. Those are report proposals, not established mechanisms.
- **S7:** `HISTORICAL__substrate_description(1).md`: prior soft-tie rationale and open use law; its old supervised-gradient fusion is not reinstated.

### Targeted external checks (2026-09-20)

- **P1:** Oja, E. (1982), *Simplified neuron model as a principal component analyzer*, Journal of Mathematical Biology 15, 267–273. DOI `10.1007/BF00275687`. Publisher record checked. Restricted normalization precedent; no nonlinear whole-loop convergence inferred.
- **P2:** Williams, R. J. (1992), *Simple statistical gradient-following algorithms for connectionist reinforcement learning*, Machine Learning 8, 229–256. DOI `10.1007/BF00992696`. Publisher abstract/record checked. Establishes the reinforcement-learning ancestry; equations (19)–(21) are not represented as a verbatim REINFORCE algorithm or an unbiased-gradient result.
- **P3:** Miconi, T. (2017), *Biologically plausible learning in recurrent neural networks reproduces neural dynamics observed during cognitive tasks*, eLife 6:e20899. DOI `10.7554/eLife.20899`. Publisher abstract and displayed introduction/discussion checked. Its delayed, trial-end task rewards are not Loom's continuing two-currency environment.

**New synthesis:** current/recent native packet association; regulation that consumes evoked rather than full raw-scene context; actual regulatory participation as another associative input; one learned sensory-participation variable controlling both query gain and continuous soft ties; and a fully exposed conditional bodily-learning rule. No source validates this combination. No numerical experiment, organism simulation, repository modification or canon amendment was performed.
