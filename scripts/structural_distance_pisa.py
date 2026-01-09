import argparse
import csv
import math
from pathlib import Path


def clamp(x, lo, hi):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


def to_float(x, default=None):
    try:
        return float(x)
    except Exception:
        return default


def atanh_safe(x, eps=1e-12):
    x = float(x)
    x = clamp(x, -1.0 + eps, 1.0 - eps)
    return 0.5 * math.log((1.0 + x) / (1.0 - x))


def read_rows(path: Path):
    with path.open("r", newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        rows = list(rdr)
        if not rows:
            raise SystemExit(f"Empty CSV: {path}")
        return rows, (rdr.fieldnames or [])


def write_rows(path: Path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in fieldnames})


def mean(vals):
    if not vals:
        return 0.0
    return sum(vals) / float(len(vals))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True, help="case07_grid_agg.csv (aggregated)")
    ap.add_argument("--row_out", default="pisa_structural_distance_rows.csv", help="Per-theta rows output CSV")
    ap.add_argument("--summary_out", default="pisa_structural_distance_summary.csv", help="Group summary output CSV")
    ap.add_argument("--eps", type=float, default=1e-12, help="Clamp epsilon for atanh")
    ap.add_argument("--m_col", default="", help="Optional numeric column to treat as m for D_muv (e.g., 'm' or 'x')")
    args = ap.parse_args()

    in_path = Path(args.inp)
    if not in_path.exists():
        raise SystemExit(f"Input not found: {args.inp}")

    rows, cols = read_rows(in_path)

    needed = ["mode", "alpha", "k", "theta", "a_avg_mean", "s_avg_mean"]
    for c in needed:
        if c not in cols:
            raise SystemExit(f"Missing column '{c}' in {args.inp}")

    use_m = bool(args.m_col.strip())
    if use_m and args.m_col not in cols:
        raise SystemExit(f"--m_col '{args.m_col}' not found in {args.inp}")

    enriched = []
    for r in rows:
        a = to_float(r.get("a_avg_mean"), None)
        s = to_float(r.get("s_avg_mean"), None)
        th = to_float(r.get("theta"), None)
        if a is None or s is None or th is None:
            continue

        u = atanh_safe(a, eps=args.eps)
        v = atanh_safe(s, eps=args.eps)
        R = math.sqrt(u * u + v * v)
        Psi = 0.5 * (u * u + v * v)

        out = dict(r)
        out["u"] = f"{u:.15g}"
        out["v"] = f"{v:.15g}"
        out["R"] = f"{R:.15g}"
        out["Psi"] = f"{Psi:.15g}"

        if use_m:
            mval = to_float(r.get(args.m_col), 0.0) or 0.0
            out["m_used"] = f"{mval:.15g}"
        else:
            out["m_used"] = ""

        # placeholders (filled after sorting)
        out["du"] = ""
        out["dv"] = ""
        out["D_uv_step"] = ""
        out["L_struct_uv"] = ""
        out["D_muv_step"] = ""
        out["L_struct_muv"] = ""

        enriched.append(out)

    def key_fn(rr):
        mode = rr.get("mode", "")
        alpha = to_float(rr.get("alpha"), 0.0) or 0.0
        kval = to_float(rr.get("k"), 0.0) or 0.0
        theta = to_float(rr.get("theta"), 0.0) or 0.0
        return (mode, alpha, kval, theta)

    enriched.sort(key=key_fn)

    prev_by_group = {}
    sum_uv_by_group = {}
    sum_muv_by_group = {}

    max_R_by_group = {}
    max_Psi_by_group = {}
    Rs_by_group = {}
    Ps_by_group = {}
    theta_min_by_group = {}
    theta_max_by_group = {}
    count_by_group = {}

    for rr in enriched:
        mode = rr.get("mode", "")
        alpha = rr.get("alpha", "")
        kval = rr.get("k", "")
        gkey = (mode, alpha, kval)

        theta = to_float(rr.get("theta"), 0.0) or 0.0
        u = to_float(rr.get("u"), 0.0) or 0.0
        v = to_float(rr.get("v"), 0.0) or 0.0
        R = to_float(rr.get("R"), 0.0) or 0.0
        Psi = to_float(rr.get("Psi"), 0.0) or 0.0

        if gkey not in count_by_group:
            count_by_group[gkey] = 0
            sum_uv_by_group[gkey] = 0.0
            sum_muv_by_group[gkey] = 0.0
            max_R_by_group[gkey] = R
            max_Psi_by_group[gkey] = Psi
            Rs_by_group[gkey] = []
            Ps_by_group[gkey] = []
            theta_min_by_group[gkey] = theta
            theta_max_by_group[gkey] = theta

        count_by_group[gkey] += 1
        theta_min_by_group[gkey] = min(theta_min_by_group[gkey], theta)
        theta_max_by_group[gkey] = max(theta_max_by_group[gkey], theta)

        Rs_by_group[gkey].append(R)
        Ps_by_group[gkey].append(Psi)
        max_R_by_group[gkey] = max(max_R_by_group[gkey], R)
        max_Psi_by_group[gkey] = max(max_Psi_by_group[gkey], Psi)

        prev = prev_by_group.get(gkey)
        if prev is None:
            du = 0.0
            dv = 0.0
            d_uv = 0.0
            d_muv = 0.0
        else:
            du = u - prev["u"]
            dv = v - prev["v"]
            d_uv = math.sqrt(du * du + dv * dv)

            if use_m:
                m_now = to_float(rr.get("m_used"), 0.0) or 0.0
                dm = m_now - prev["m"]
                d_muv = math.sqrt(dm * dm + du * du + dv * dv)
            else:
                d_muv = 0.0

        sum_uv_by_group[gkey] += d_uv
        sum_muv_by_group[gkey] += d_muv

        rr["du"] = f"{du:.15g}"
        rr["dv"] = f"{dv:.15g}"
        rr["D_uv_step"] = f"{d_uv:.15g}"
        rr["L_struct_uv"] = f"{sum_uv_by_group[gkey]:.15g}"

        if use_m:
            rr["D_muv_step"] = f"{d_muv:.15g}"
            rr["L_struct_muv"] = f"{sum_muv_by_group[gkey]:.15g}"
        else:
            rr["D_muv_step"] = ""
            rr["L_struct_muv"] = ""

        prev_by_group[gkey] = {
            "u": u,
            "v": v,
            "m": (to_float(rr.get("m_used"), 0.0) or 0.0) if use_m else 0.0,
        }

    row_cols = ["mode", "alpha", "k", "theta", "a_avg_mean", "s_avg_mean", "u", "v", "R", "Psi", "du", "dv", "D_uv_step", "L_struct_uv"]
    if use_m:
        row_cols += ["m_used", "D_muv_step", "L_struct_muv"]

    write_rows(Path(args.row_out), row_cols, enriched)

    summary_rows = []
    keys_sorted = sorted(
        count_by_group.keys(),
        key=lambda kk: (kk[0], float(kk[1]), float(kk[2]))
    )
    for (mode, alpha, kval) in keys_sorted:
        n = count_by_group[(mode, alpha, kval)]
        L_uv = sum_uv_by_group[(mode, alpha, kval)]
        maxR = max_R_by_group[(mode, alpha, kval)]
        maxPsi = max_Psi_by_group[(mode, alpha, kval)]
        meanR = mean(Rs_by_group[(mode, alpha, kval)])
        meanPsi = mean(Ps_by_group[(mode, alpha, kval)])
        tmin = theta_min_by_group[(mode, alpha, kval)]
        tmax = theta_max_by_group[(mode, alpha, kval)]

        out = {
            "mode": mode,
            "alpha": alpha,
            "k": kval,
            "rows": str(int(n)),
            "theta_min": f"{tmin:.15g}",
            "theta_max": f"{tmax:.15g}",
            "L_struct_uv": f"{L_uv:.15g}",
            "max_R": f"{maxR:.15g}",
            "max_Psi": f"{maxPsi:.15g}",
            "mean_R": f"{meanR:.15g}",
            "mean_Psi": f"{meanPsi:.15g}",
        }
        if use_m:
            out["L_struct_muv"] = f"{sum_muv_by_group[(mode, alpha, kval)]:.15g}"
        summary_rows.append(out)

    summary_cols = ["mode", "alpha", "k", "rows", "theta_min", "theta_max", "L_struct_uv"]
    if use_m:
        summary_cols += ["L_struct_muv"]
    summary_cols += ["max_R", "max_Psi", "mean_R", "mean_Psi"]

    write_rows(Path(args.summary_out), summary_cols, summary_rows)

    for r in summary_rows:
        msg = f"mode={r['mode']}, alpha={r['alpha']}, k={r['k']}: rows={r['rows']}, L_struct_uv={r['L_struct_uv']}, max_R={r['max_R']}, max_Psi={r['max_Psi']}"
        if use_m and "L_struct_muv" in r:
            msg += f", L_struct_muv={r['L_struct_muv']}"
        print(msg)

    print(f"WROTE {args.row_out}")
    print(f"WROTE {args.summary_out}")


if __name__ == "__main__":
    main()
