# Exploration audit methods — fixed before reading native movement results

Passive extraction only. Use all 60 existing trajectories, with FS-060 prefix separate and a fixed 59-complete-life denominator for pooled biological histories. Read native physical records at original 0.01 s fidelity and initial checkpoint as data; no P import, object reinstantiation, RNG, motor generator or dynamics execution. Verify each input file/payload checksum. Heading/direction correlations and time-lag MSD use deterministic 0.1 s sampling to reduce observer work, not recording fidelity.

Report displacement/max excursion, native polyline distance, actual saved endpoint translational/angular velocity, forward/lateral velocity in the saved heading frame, commands and contacts. Age panels: 0–60, 60–120, 120–180, 180–240, 240–300, 300–360, 360–420 and final partial block. Compare early and late panels; do not label a whole-life statistic purely newborn.

MSD: (a) birth-relative squared displacement at 1/2/5/10/20/30/60/120/180/240/300/360/420 s; (b) each life's time-averaged squared displacement at fixed lags. No extrapolation of diffusion coefficient or infinite behavior. Averages across lives are not independent within-life samples.

Persistence: heading cos-difference and normalized velocity-direction dot product at fixed lags 0…20 s by 0.1 s then 21…120 s by 1 s. Velocity directions require both speeds >0.01. First correlation crossing below 1/e is an oscillatory first-crossing descriptor, not an exponential-fit persistence constant. No crossing means right-censored at 120 s. All-life and first-60-s curves retained.

Forward/reverse bouts: contiguous saved body-forward velocity >0.01 / <−0.01. Report all lengths plus count lasting ≥0.1 s. Reversals: alternate forward/reverse bouts each lasting ≥0.1 s, ignoring intervening deadband. Fixed sensitivity thresholds 0.005/0.02. No direction inferred from the sign of angular speed alone. Command correlation is ordinary Pearson left/right, separately common/differential RMS and same/opposite signs.

Activity: active if speed or body-edge rotational speed r|omega| exceeds 0.005. Predominantly rotation if r|omega|>2*speed; predominantly translation if speed>2*r|omega|; otherwise mixed. Fractions are time weighted. This is a kinematic ratio, not an intention or an energy-cost decomposition. Report thresholds, do not treat the fractions as universal categories.

Path curvature: change in saved velocity direction / native path length, excluding endpoints with speed≤0.01; retain median and 90th percentile and total absolute direction change per accepted distance. Also report body-heading change separately; reversals are not assumed to be turning in place. Near-zero denominators excluded and counted.

Coverage/recurrence: world-aligned square bins at side 0.25 and 1; count visited bins versus age, distinct-bin re-entry after leaving, and fraction of cell transitions entering an already visited bin. A within-bin step is not a new entry. Report 0.25-grid half-bin-offset sensitivity. Spatial occupancy is not swept body coverage. No visited-space information feeds P.

Trapping: saved positive contact impulse/rate, wall gap, mover gap and nearest static fixture gap; report time within 0.25/0.5 of a surface. Compare all complete lives with no-positive-contact complete lives. Local motion without contact weakens hard-collision trapping as a necessary explanation; it does not eliminate visual/chemical feedback or other environmental influence. No causal motor omission/alternative trajectory is authorized or performed.

The old source-density layout is preserved as provisional. Only findings material to mechanism-versus-opportunity interpretation may alter the design recommendation; no numerical motor option is tested or fitted here.
