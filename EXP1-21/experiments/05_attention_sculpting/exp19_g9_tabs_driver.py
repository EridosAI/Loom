"""exp19_g9_tabs_driver.py — the one-shot generator of exp19_g9_tab_B512_vs_BT_{full,stratified}.json
(committed per the panel's provenance FLAG: the load-bearing cross-arm instrument must be regenerable
without guessing the cell recipe). Cells: B512 g9 series at its per-B ops (full 450 / strat 300); B=T
committed captures at its ops (full 300 / strat 550). Deterministic; byte-reproducible."""
import json, torch
torch.set_num_threads(1)
import exp19_cal as CAL, exp19_tabs as TB

def g9(arm, s):
    d = json.loads((CAL.XA.OUTDIR / f"exp19_g9_{arm}_s{s}_series.json").read_text())
    return d["acq"], d["full_onsets"], d["strat_onsets"]

def main():
    b512f, b512s = {}, {}
    for s in range(8):
        a, f, st = g9("exp19_wperm_B512", s)
        b512f[s], b512s[s] = (a, f), (a, st)
    btf = {s: CAL._onsets("exp12_shuffle", s, "full") for s in range(8)}
    bts = {s: CAL._onsets("exp12_shuffle", s, "stratified") for s in range(8)}
    for read, wa, wb, da, db in (("full", 450, 300, b512f, btf), ("stratified", 300, 550, b512s, bts)):
        tab = TB.matched_bar_tab19(TB.cell("B512", read, wa, da), TB.cell("BT", read, wb, db))
        (CAL.XA.OUTDIR / f"exp19_g9_tab_B512_vs_BT_{read}.json").write_text(json.dumps(tab, indent=2))
        print(read, "tab written")

if __name__ == "__main__":
    main()
