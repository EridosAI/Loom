"""Independent read-only execution of 18 delivered mutant/control pairs."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys

ROOT = Path(r"C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405")
TARGET = ROOT / "developmental_ecology"
OUT = Path(__file__).resolve().parent
PYTHON = ROOT / ".venv/Scripts/python.exe"
OLD = "f7eb6f27c661e3db193a4225b56a825d7e41739d"
NEW = "6bc9683b54e4fa80136fe8534d7713e2a250a95f"
sys.path.insert(0, str(TARGET))
import verify_correction_mutants as prior
import verify_r1p_mutants as added

LOCATIONS = {
    "unmodified_f7": "tests/test_r1p_oblique.py:45",
    "class_search_disabled": "tests/test_r1p_oblique.py:45",
    "old_swept_search": "<unmodified f7eb6f27 physics>:158",
    "duplicate_field_update": "tests/test_r1p_oblique.py:87",
    "release_disabled": "tests/test_corrective_contracts.py:29",
    "live_branch_missing": "tests/test_records.py:85",
    "bank_reference_frozen": "tests/test_neural.py:204",
    "bank_reference_old_target": "tests/test_neural.py:215",
    "shared_reference_frozen": "tests/test_corrective_contracts.py:91",
    "fine_reference_frozen": "tests/test_corrective_contracts.py:91",
    "terminal_guard_removed": "tests/test_boundary_and_scheduler.py:48",
    "body_footprint_missing": "tests/test_physical.py:31",
    "hidden_pose_injected": "tests/test_corrective_contracts.py:135",
    "hidden_config_read": "tests/test_corrective_contracts.py:116",
    "evoked_refill": "tests/test_corrective_contracts.py:165",
    "double_source_debit": "tests/test_corrective_contracts.py:45",
    "damage_suppressed": "tests/test_corrective_contracts.py:48",
    "native_repeated": "tests/test_corrective_contracts.py:78",
}
CASES = dict(added.CASES, **prior.CASES)

def git(*args):
    return subprocess.check_output(["git", "-c", "safe.directory=" + ROOT.as_posix(), "-C", str(ROOT), *args])

def identity():
    old_source = git("show", OLD + ":developmental_ecology/loom_p/physics.py")
    old_hash = hashlib.sha256(old_source).hexdigest()
    assert old_hash == "2a2e53bdfb3964488a446f1549682bc00cb4bc0403ef4a95f1adc245a4e58f63"
    _, helper_hash = added.archived()
    assert helper_hash == old_hash
    preserved = []
    tracked = git("ls-tree", "-r", "--name-only", OLD, "developmental_ecology/loom_p", "developmental_ecology/tests").decode().splitlines()
    tracked += ["developmental_ecology/configuration.json", "developmental_ecology/verify_correction_mutants.py"]
    for path in tracked:
        if path.endswith("/physics.py"): continue
        before = git("show", OLD + ":" + path)
        after = git("show", NEW + ":" + path)
        assert before == after, path
        preserved.append(dict(path=path, sha256=hashlib.sha256(after).hexdigest(), commits_identical=True))
    from loom_p.schema import Config
    return dict(old_commit=OLD, new_commit=NEW, archived_physics_sha256=old_hash,
        helper_archived_hash_matches=True, semantic_configuration_sha256=Config().identity(), preserved=preserved)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--child")
    parser.add_argument("--attempt", default="001")
    args = parser.parse_args()
    # Process-only Git trust; no repository/global config mutation.
    os.environ["GIT_CONFIG_COUNT"] = "1"
    os.environ["GIT_CONFIG_KEY_0"] = "safe.directory"
    os.environ["GIT_CONFIG_VALUE_0"] = str(ROOT)
    if args.child:
        import pytest
        (added if args.child in added.CASES else prior).install(args.child)
        raise SystemExit(pytest.main([CASES[args.child][0], "-q", "-p", "no:cacheprovider", "--tb=long"]))
    evidence = OUT / ("pairs-attempt-" + args.attempt)
    evidence.mkdir(exist_ok=False)
    temp = OUT / ("isolated-temp-" + args.attempt)
    temp.mkdir(exist_ok=False)
    (evidence / "IDENTITY.json").write_text(json.dumps(identity(), indent=2), encoding="utf-8")
    envbase = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", TEMP=str(temp), TMP=str(temp), PYTHONPATH=str(TARGET))
    receipts = []
    for name, (test, message) in CASES.items():
        row = dict(name=name, test=test, expected_message=message, expected_location=LOCATIONS[name])
        for color in ("RED", "GREEN"):
            env = envbase.copy()
            env["PYTEST_ADDOPTS"] = '--basetemp="' + (temp / (name + "-" + color)).as_posix() + '"'
            command = ([str(PYTHON), "-B", "-X", "utf8", str(Path(__file__).resolve()), "--child", name]
                if color == "RED" else [str(PYTHON), "-B", "-X", "utf8", "-m", "pytest", test, "-q", "-p", "no:cacheprovider", "--tb=long"])
            result = subprocess.run(command, cwd=TARGET, env=env, capture_output=True, text=True, encoding="utf-8")
            output = result.stdout + result.stderr
            path = evidence / (name + "-" + color + ".txt")
            path.write_text(output, encoding="utf-8")
            good = (result.returncode == 1 and "1 failed" in output and message in output and LOCATIONS[name] in output.replace(chr(92), "/")
                if color == "RED" else result.returncode == 0 and "1 passed" in output)
            row[color] = dict(command=command, exit_code=result.returncode, confirmed=good, output=str(path.relative_to(OUT)), sha256=hashlib.sha256(path.read_bytes()).hexdigest())
            print(name, color, result.returncode, good, flush=True)
            if not good:
                receipts.append(row)
                (evidence / "SUMMARY.json").write_text(json.dumps(receipts, indent=2), encoding="utf-8")
                raise RuntimeError("Unexpected failure mode: " + name + " " + color)
        receipts.append(row)
    (evidence / "SUMMARY.json").write_text(json.dumps(receipts, indent=2), encoding="utf-8")

if __name__ == "__main__": main()
