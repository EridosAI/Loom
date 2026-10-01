# Positive-control review addendum — 27 September 2026

This addendum corrects the PC-CONTACT assessment against the unchanged accepted task and records the separately authorized PC-HOLD repeat. It supersedes the affected status conclusions in the earlier execution report; it does not overwrite the original observations, assessments, runs or review package.

| Control | Current disposition | Qualification |
|---|---|---|
| PC-LR | DEMONSTRATED | Guided channel pairing; separately authorized zero-step second attempt after connection loss |
| PC-MOTION | DEMONSTRATED WITH EXPLICIT GUIDANCE | Turning sign corrected; final conceptual explanation after wall cutoff |
| PC-CONTACT | DEMONSTRATED for the declared onset-recognition task | Approximate onset recognized before physical replay; timing uncertainty and later scene-interpretation errors retained |
| PC-HOLD | DEMONSTRATED on separately authorized attempt 002 | 1.2 s continuous gentle support; prior practice, physical feedback and duration guidance documented. Attempt 001 remains below its one-second target |

## Why PC-CONTACT was initially marked partial, and why that label is corrected

The accepted `POSITIVE_CONTROL_CARDS.md` defines the task as: “Use small paired entries to approach, and identify contact onset from raw contact/proprioceptive history.” It separately instructs the evaluator to check actual onset, impact and support and preserve missed onset or damage.

Before the physical replay, Jason said contact appeared around **0.8 s**, while explicitly expressing timing uncertainty. The actual first impact was **0.898417740 s**, and the first native contact sample was **0.900 s**. He identified the initial contact transition from the permitted sensor display. This is approximate recognition, not an exact timestamp report. The accepted card sets no numerical timing-accuracy gate; none is invented here.

The assistant originally withheld full demonstration because Jason could not confidently map trace colours to coordinates and interpreted later persistent contact as another impact or rough ground. Those limitations were real, but naming colours/channels and fully explaining the subsequent scene were not additional predeclared PC-CONTACT pass requirements. Making them gates was an assessment error. Onset recognition is therefore recorded as demonstrated on the existing pre-replay evidence.

The following remain unchanged: the original uncertainty; the mistaken later scene interpretation; the initially large `[1, 1]` commands rather than a careful small approach; the physical trajectory and damage; and the additional learning from the post-case replay. No damage-free criterion was specified. This correction does not claim precise timing, perfect contact understanding, careful initial actuation or an unassisted sequence. It does not use the later replay as evidence that the earlier scene explanation was correct. No PC-CONTACT rerun occurred.

The correction is recorded in `PC-CONTACT.ASSESSMENT_CORRECTION.json`, with the original observation quoted and hashes binding the original result, runtime receipt and accepted task card. The original `PC-CONTACT.RESULT.json` and earlier report are preserved as historical assessments.

## PC-HOLD repeat

Jason separately authorized one fresh attempt: “Wait is it unmet because I only went to 0.8s? Rerun it if you like.” This did not authorize further cases or retries. Attempt 002 used the same canonical execution object, complete physical initial state, apparatus, interface, laws, ten-second ceiling, twenty-minute wall allowance and one-second support criterion. Only its attempt-specific grant record and output destination changed. Jason chose all 15 submitted command pairs and ended the case himself at **1.500 s**. Wall duration was **120.368 s**.

Continuous positive-duration support qualified from **0.300 to 1.500 s**, lasting **1.200 s**. Force ranged from **0.037641686 to 0.150862270**, strictly below the original **0.25** threshold. There was **zero sustained stress damage during that interval**. The repeat therefore obtained the declared physical hold target.

Damage before the qualifying interval remains recorded: impact damage **0.003166194**, sustained stress damage **0.000669606**, total **0.003835801**. Expenditure was **0.002625**. E/I changed from **0.700000 / 1.000000** to **0.697375 / 0.996164**. The first attempt, including its 0.8 s qualifying interval and later exploration, is not replaced or relabelled.

The same closed-record test was used for both attempts: positive contact impulse over positive duration, actual force equal to impulse/duration, all active contact forces strictly below the threshold, and zero sustained stress damage. Contiguous intervals use only the existing `event_time_tol = 1e-10`. All artifact hashes and sizes and the force/damage arithmetic were verified. No world was advanced during analysis.

## Current boundary and evidence

All four disclosed demonstrations are now documented, with their guidance and retry qualifications. This satisfies the demonstration component on that stated basis; it does not by itself authorize B1 or assert that every separate B1 admission condition has been re-reviewed. No B1 execution or sealed B1 state/evaluator inspection occurred. No further case is started. No P learning, perceptual ceiling, internal world model, survival or efficacy claim follows from this human practice.

The cumulative executed record contains **790 native steps and 79 human commands** across six preparations: PC-LR twice, PC-MOTION once, PC-CONTACT once and PC-HOLD twice. Every control service is closed. The apparatus worktree remains clean at `352f73fffa6d9781eae8aa38e708a9a05669588f`; P remains `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. No production code, configuration, interface, physical law or accepted criterion changed, and no Git write occurred.

The updated portable package retains the earlier package contents under `historical-original-review/`, adds all attempt-002 records and grant provenance, and includes this addendum and the assessment correction. The earlier report's partial/failure and gate conclusions describe its then-current assessment; use this addendum for current status. `PACKAGE_FILE_MANIFEST.json` binds every file in the updated package except itself. The original package remains byte-for-byte preserved.
