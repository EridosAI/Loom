from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
WT=ROOT/'worktrees/loom-p-b1-minimal-20260929'
D=WT/'developmental_ecology'
PACKET=ROOT/'exports/2026-09-30-Founder-Search-initial-stage'
sys.path.insert(0,str(D))
