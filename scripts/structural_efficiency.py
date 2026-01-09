import argparse
import csv
import math
from pathlib import Path


def _to_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return default


def _read_trace(path: Path):
    rows = []
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    if not rows:
        raise SystemExit(f"Empty CSV: {path}")
    return rows


def _compute(rows):
    dx = [_to_float(r.get("dx")) for r in rows]
    u = [_to_float(r.get("u")) for r in rows]
    v = [_to_float(r.get("v")) for r in rows]
    R = [_to_float(r.get("R")) for r in rows]
    Psi = [_to_float(r.get("Psi")) for r in rows]

    L_classical = sum(abs(x) for x in dx)

    L_struct = 0.0
    for i in range(len(rows) - 1):
        du = u[i + 1] - u[i]
        dv = v[i + 1] - v[i]
        L_struct += math.sqrt(dx[i] * dx[i] + du * du + dv * dv)
    if len(rows) >= 1:
        L_struct += abs(dx[-1])

    eps = 1e-12
    eta = L_struct / (L_classical + eps)

    closed = int(_to_float(rows[-1].get("closed"), 0.0))
    return {
        "rows": len(rows),
        "closed": closed,
        "L_classical": L_classical,
        "L_struct": L_struct,
        "eta": eta,
        "max_R": max(R) if R else 0.0,
        "max_Psi": max(Psi) if Psi else 0.0,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inputs", nargs="+", required=True, help="SSIG trace CSV files")
    ap.add_argument("--out", default="structural_efficiency_summary.csv", help="Output CSV")
    args = ap.parse_args()

    out_path = Path(args.out)

    fieldnames = ["trace", "rows", "closed", "L_classical", "L_struct", "eta", "max_R", "max_Psi"]
    records = []

    for p in args.inputs:
        path = Path(p)
        rows = _read_trace(path)
        m = _compute(rows)
        m["trace"] = path.name
        records.append(m)

    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in records:
            w.writerow(r)

    for r in records:
        print(
            f"{r['trace']}: eta={r['eta']}, "
            f"L_classical={r['L_classical']}, L_struct={r['L_struct']}, "
            f"max_R={r['max_R']}, max_Psi={r['max_Psi']}"
        )

    print(f"WROTE {out_path.as_posix()}")


if __name__ == "__main__":
    main()
