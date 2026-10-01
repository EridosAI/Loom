"""Independent, read-only R3 mutant execution; exports only to this directory."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys

TARGET = Path(r"C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\developmental_ecology")
OUT = Path(__file__).resolve().parent
PYTHON = TARGET.parent / ".venv/Scripts/python.exe"
sys.path.insert(0, str(TARGET))

CORRECTIVE = "tests/test_corrective_contracts.py::"
BANK = "tests/test_neural.py::test_bank_projection_and_reference_follow_new_value"
SENSORY = CORRECTIVE + "test_separate_sensory_reference_following"
HIDDEN = CORRECTIVE + "test_hidden_state_cannot_bypass_declared_transductions"
OWNERSHIP = CORRECTIVE + "test_evoked_reserves_have_no_direct_physical_ownership"
CASES = {
    "bank_reference_frozen": (BANK, "assert np.allclose(r.reference", "tests/test_neural.py:204"),
    "bank_reference_old_target": (BANK, "Bank reference must follow newly projected theta", "tests/test_neural.py:215"),
    "shared_reference_frozen": (SENSORY + "[shared_ref-shared-tau_shared_reference]", "shared_ref movement missing", "tests/test_corrective_contracts.py:91"),
    "fine_reference_frozen": (SENSORY + "[fine_ref-fine-tau_fine_reference]", "fine_ref movement missing", "tests/test_corrective_contracts.py:91"),
    "terminal_guard_removed": ("tests/test_boundary_and_scheduler.py::test_terminal_scheduler_restores_trial_state_and_draws_once[19]", "Invented terminal handoff", "tests/test_boundary_and_scheduler.py:48"),
    "body_footprint_missing": ("tests/test_physical.py::test_field_flux_mass_and_moving_geometry_continuity", "Body footprint must change diffusion", "tests/test_physical.py:31"),
    "hidden_pose_injected": (HIDDEN, "Hidden world state entered native learner arithmetic", "tests/test_corrective_contracts.py:135"),
    "hidden_config_read": (HIDDEN, "Forbidden learner configuration read", "tests/test_corrective_contracts.py:116"),
    "evoked_refill": (OWNERSHIP, "Evoked reserve bypassed motor/physical ownership", "tests/test_corrective_contracts.py:165"),
    "shared_reference_new_target": (SENSORY + "[shared_ref-shared-tau_shared_reference]", "shared_ref movement missing", "tests/test_corrective_contracts.py:91"),
    "fine_reference_new_target": (SENSORY + "[fine_ref-fine-tau_fine_reference]", "fine_ref movement missing", "tests/test_corrective_contracts.py:91"),
    "terminal_guard_removed_59": ("tests/test_boundary_and_scheduler.py::test_terminal_scheduler_restores_trial_state_and_draws_once[59]", "Invented terminal handoff", "tests/test_boundary_and_scheduler.py:48"),
    "hidden_stock_injected": (HIDDEN, "Hidden world state entered native learner arithmetic", "tests/test_corrective_contracts.py:135"),
    "hidden_clock_injected": (HIDDEN, "Hidden world state entered native learner arithmetic", "tests/test_corrective_contracts.py:135"),
    "hidden_world_counter_injected": (HIDDEN, "Hidden world state entered native learner arithmetic", "tests/test_corrective_contracts.py:135"),
    "evoked_integrity_refill": (OWNERSHIP, "Evoked reserve bypassed motor/physical ownership", "tests/test_corrective_contracts.py:165"),
}

def install(name):
    import loom_p.engine as engine
    import loom_p.neural as neural
    import verify_correction_mutants as delivered
    if name in delivered.CASES:
        delivered.install(name)
    elif name == "terminal_guard_removed_59":
        delivered.install("terminal_guard_removed")
    elif name.endswith("_reference_new_target"):
        original = neural.Cortex.step
        attr, target, tau = (("shared_ref", "shared", "tau_shared_reference")
            if name.startswith("shared") else ("fine_ref", "fine", "tau_fine_reference"))
        def broken(self, c, raw, support, dt):
            before = getattr(self, attr).copy()
            original(self, c, raw, support, dt)
            setattr(self, attr, neural.follow(before, getattr(self, target), dt, getattr(c, tau)))
        neural.Cortex.step = broken
    elif name.startswith("hidden_"):
        original = engine.Engine._coupled
        def broken(self, dt, refresh, allow_terminal=False):
            if name == "hidden_stock_injected": hidden = float(self.stocks.sum())
            elif name == "hidden_clock_injected": hidden = self.time
            elif name == "hidden_world_counter_injected": hidden = self.organism.rng.counters.get("life/world-position", 0)
            else: raise AssertionError("Unrecognized independent mutant")
            self.raw[0][0] += hidden * 0.001
            return original(self, dt, refresh, allow_terminal)
        engine.Engine._coupled = broken
    elif name == "evoked_integrity_refill":
        original = engine.Engine._coupled
        def broken(self, dt, refresh, allow_terminal=False):
            result = original(self, dt, refresh, allow_terminal)
            self.body.integrity += 0.0001 * self.organism.association.q[self.c.slices[5]][0]
            return result
        engine.Engine._coupled = broken
    else:
        raise ValueError(name)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--child")
    parser.add_argument("--attempt", default="002")
    args = parser.parse_args()
    if args.child:
        import pytest
        install(args.child)
        raise SystemExit(pytest.main([CASES[args.child][0], "-q", "-p", "no:cacheprovider", "--tb=long"]))
    evidence = OUT / ("mutants-attempt-" + args.attempt)
    evidence.mkdir(exist_ok=False)
    temp = OUT / ("isolated-temp-" + args.attempt)
    temp.mkdir(exist_ok=False)
    base_env = os.environ.copy()
    base_env.update(PYTHONDONTWRITEBYTECODE="1", PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", TEMP=str(temp), TMP=str(temp))
    receipts = []
    for name, (test, message, line) in CASES.items():
        receipt = dict(name=name, test=test, expected_message=message, expected_test_line=line)
        for color in ("RED", "GREEN"):
            env = base_env.copy()
            env["PYTEST_ADDOPTS"] = "--basetemp=" + str(temp / (name + "-" + color))
            command = ([str(PYTHON), "-B", "-X", "utf8", str(Path(__file__).resolve()), "--child", name]
                if color == "RED" else [str(PYTHON), "-B", "-X", "utf8", "-m", "pytest", test, "-q", "-p", "no:cacheprovider", "--tb=long"])
            result = subprocess.run(command, cwd=TARGET, env=env, capture_output=True, text=True, encoding="utf-8")
            output = result.stdout + result.stderr
            path = evidence / (name + "-" + color + ".txt")
            path.write_text(output, encoding="utf-8")
            good = (result.returncode == 1 and "1 failed" in output and message in output and line in output.replace(chr(92), "/")
                if color == "RED" else result.returncode == 0 and "1 passed" in output)
            receipt[color] = dict(command=command, exit_code=result.returncode, confirmed=good,
                output=str(path.relative_to(OUT)), sha256=hashlib.sha256(path.read_bytes()).hexdigest())
            print(name, color, result.returncode, good, flush=True)
            if not good:
                receipts.append(receipt)
                (evidence / "SUMMARY.json").write_text(json.dumps(receipts, indent=2), encoding="utf-8")
                raise RuntimeError("Unexpected result: " + name + " " + color)
        receipts.append(receipt)
    (evidence / "SUMMARY.json").write_text(json.dumps(receipts, indent=2), encoding="utf-8")

if __name__ == "__main__": main()
