import argparse
import csv
import math
from pathlib import Path


def to_float(x, default=None):
    try:
        return float(x)
    except Exception:
        return default


def read_trace(path: Path):
    rows = []
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    if not rows:
        raise SystemExit(f"Empty CSV: {path}")
    return rows


def compute_metrics(rows):
    dx = [abs(to_float(r.get("dx"), 0.0)) for r in rows]
    u = [to_float(r.get("u"), 0.0) for r in rows]
    v = [to_float(r.get("v"), 0.0) for r in rows]
    R = [to_float(r.get("R"), 0.0) for r in rows]
    Psi = [to_float(r.get("Psi"), 0.0) for r in rows]
    ev_last = str(rows[-1].get("event", ""))
    closed_last = int(to_float(rows[-1].get("closed"), 0) or 0)

    L_classical = sum(dx)

    L_struct = 0.0
    for i in range(len(rows) - 1):
        du = (u[i + 1] - u[i]) if (u[i + 1] is not None and u[i] is not None) else 0.0
        dv = (v[i + 1] - v[i]) if (v[i + 1] is not None and v[i] is not None) else 0.0
        L_struct += math.sqrt((to_float(rows[i].get("dx"), 0.0) or 0.0) ** 2 + du * du + dv * dv)

    if len(rows) >= 1:
        L_struct += abs(to_float(rows[-1].get("dx"), 0.0) or 0.0)

    return {
        "rows": len(rows),
        "closed": closed_last,
        "last_event": ev_last,
        "L_classical": L_classical,
        "L_struct": L_struct,
        "max_R": max(R) if R else 0.0,
        "max_Psi": max(Psi) if Psi else 0.0,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inputs", nargs="+", required=True, help="One or more SSIG trace CSV files")
    ap.add_argument("--out", default="structural_distance_summary.csv", help="Output summary CSV file name")
    args = ap.parse_args()

    out_path = Path(args.out)

    records = []
    for p in args.inputs:
        csv_path = Path(p)
        rows = read_trace(csv_path)
        m = compute_metrics(rows)
        m["trace"] = csv_path.name
        records.append(m)

    fieldnames = ["trace", "rows", "closed", "last_event", "L_classical", "L_struct", "max_R", "max_Psi"]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in records:
            w.writerow(r)

    for r in records:
        print(
            f"{r['trace']}: rows={r['rows']}, closed={r['closed']}, "
            f"L_classical={r['L_classical']}, L_struct={r['L_struct']}, "
            f"max_R={r['max_R']}, max_Psi={r['max_Psi']}"
        )

    print(f"WROTE {out_path.as_posix()}")


if __name__ == "__main__":
    main()
