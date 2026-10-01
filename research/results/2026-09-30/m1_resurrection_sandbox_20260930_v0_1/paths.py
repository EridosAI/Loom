"""NON-CANONICAL RESURRECTION SANDBOX; canonical inputs are read-only."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
WT=ROOT/'worktrees/loom-contact-release-20260930';D=WT/'developmental_ecology'
MOTOR=ROOT/'motor_commissioning_preparation_20260930_v0_2'
sys.path.insert(0,str(D));sys.path.insert(0,str(MOTOR))
