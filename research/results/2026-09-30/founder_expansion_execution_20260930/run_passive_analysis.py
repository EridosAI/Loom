"""Single bounded post-archive analysis sequence. No Life or world stepping."""
from pathlib import Path
import sys,time,json

HERE=Path(__file__).resolve().parent

def main():
    assert (HERE/'ARCHIVE_VERIFICATION.json').exists()
    assert not (HERE/'analysis').exists(), 'No repeated analysis pipeline'
    import passive_ab,select_passive_windows,passive_reconstruct_b,passive_c,write_combined_report,finalize_delivery
    stages=[('all_roster_AB',passive_ab.main,None),
        ('deterministic_C_selection',select_passive_windows.main,None),
        ('consequential_exact_B',passive_reconstruct_b.main,'consequential'),
        ('passive_C_windows',passive_c.main,None),
        ('remaining_exact_B_within_allowance',passive_reconstruct_b.main,'remaining'),
        ('combined_report',write_combined_report.main,None),
        ('final_custody_check',finalize_delivery.main,None)]
    for name,call,mode in stages:
        print(json.dumps(dict(stage=name,status='START',monotonic=time.perf_counter())),flush=True)
        if mode:sys.argv=[str(HERE/'passive_reconstruct_b.py'),mode]
        call()
        print(json.dumps(dict(stage=name,status='COMPLETE',monotonic=time.perf_counter())),flush=True)

if __name__=='__main__':main()
