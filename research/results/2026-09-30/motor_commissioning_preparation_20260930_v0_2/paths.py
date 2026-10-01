from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
WT=ROOT/'worktrees/loom-contact-release-20260930'
D=WT/'developmental_ecology'
PACKET=ROOT/'exports/2026-09-30-Founder-Search-initial-stage'
sys.path.insert(0,str(D))
