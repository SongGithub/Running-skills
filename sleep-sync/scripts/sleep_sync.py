#!/usr/bin/env python3
"""
Incremental Garmin sleep sync -> ~/.local/share/coach/memory.db : sleep_daily

Runs headless with the shared self-healing auth (garmin_auth.ensure_session).

Usage:
    python3 sleep_sync.py                 # incremental: last stored date-1 .. today
    python3 sleep_sync.py --from 2026-08-08
    python3 sleep_sync.py --days 30
    python3 sleep_sync.py --dry-run
"""
import sys, argparse, sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from garmin_auth import ensure_session

DB = Path.home() / ".local/share/coach/memory.db"

COLS = {
    "sleep_hours": "REAL", "sleep_score": "INTEGER", "sleep_score_qualifier": "TEXT",
    "avg_hr": "REAL", "deep_sec": "REAL", "light_sec": "REAL", "rem_sec": "REAL",
    "awake_sec": "REAL", "sleep_stress": "REAL", "hrv_overnight": "REAL",
    "body_battery_change": "REAL", "sleep_need_hours": "REAL",
    "sleep_start": "TEXT", "sleep_end": "TEXT", "awake_count": "INTEGER",
    "restless_moments": "INTEGER", "respiration": "REAL", "resting_hr": "REAL",
    "synced_at": "TEXT",
}


def _log(m):
    print(m, file=sys.stderr, flush=True)


def ensure_schema(db):
    db.execute("CREATE TABLE IF NOT EXISTS sleep_daily (date TEXT PRIMARY KEY)")
    have = {r[1] for r in db.execute("PRAGMA table_info(sleep_daily)")}
    added = []
    for c, t in COLS.items():
        if c not in have:
            db.execute("ALTER TABLE sleep_daily ADD COLUMN %s %s" % (c, t))
            added.append(c)
    db.commit()
    if added:
        _log("[schema] added columns: " + ", ".join(added))


def _local(ms):
    """Garmin *Local* timestamps are offset-shifted epoch ms; UTC view = wall clock."""
    if not ms:
        return None
    try:
        return datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return None


def fetch_day(g, d):
    try:
        s = g.get_sleep_data(d) or {}
    except Exception as e:
        _log("[warn] %s: %s" % (d, str(e)[:90]))
        return None
    dd = s.get("dailySleepDTO") or {}
    dur = dd.get("sleepTimeSeconds") or 0
    if not dur:
        return None
    sc = dd.get("sleepScores") or {}
    overall = sc.get("overall") or {}
    need = dd.get("sleepNeed") or {}
    nv = need.get("dailyNeeds") if isinstance(need, dict) else need
    return {
        "date": d,
        "sleep_hours": round(dur / 3600, 2),
        "sleep_score": overall.get("value"),
        "sleep_score_qualifier": overall.get("qualifierKey"),
        "avg_hr": dd.get("avgHeartRate"),
        "deep_sec": dd.get("deepSleepSeconds"),
        "light_sec": dd.get("lightSleepSeconds"),
        "rem_sec": dd.get("remSleepSeconds"),
        "awake_sec": dd.get("awakeSleepSeconds"),
        "sleep_stress": dd.get("avgSleepStress"),
        "hrv_overnight": s.get("avgOvernightHrv"),
        "body_battery_change": s.get("bodyBatteryChange"),
        "sleep_need_hours": round(nv / 3600, 2) if isinstance(nv, (int, float)) else None,
        "sleep_start": _local(dd.get("sleepStartTimestampLocal")),
        "sleep_end": _local(dd.get("sleepEndTimestampLocal")),
        "awake_count": dd.get("awakeCount"),
        "restless_moments": s.get("restlessMomentsCount"),
        "respiration": dd.get("averageRespirationValue"),
        "resting_hr": s.get("restingHeartRate"),
        "synced_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def upsert(db, rec):
    cols = list(rec.keys())
    ph = ",".join("?" for _ in cols)
    upd = ",".join("%s=excluded.%s" % (c, c) for c in cols if c != "date")
    db.execute(
        "INSERT INTO sleep_daily (%s) VALUES (%s) ON CONFLICT(date) DO UPDATE SET %s"
        % (",".join(cols), ph, upd),
        [rec[c] for c in cols],
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", default=None)
    ap.add_argument("--days", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    today = datetime.now().date()
    db = sqlite3.connect(str(DB))
    ensure_schema(db)

    row = db.execute("SELECT max(date) FROM sleep_daily WHERE sleep_hours IS NOT NULL").fetchone()
    last = row[0] if row and row[0] else None

    if a.start:
        start = datetime.strptime(a.start, "%Y-%m-%d").date()
    elif a.days:
        start = today - timedelta(days=a.days)
    elif last:
        start = datetime.strptime(last, "%Y-%m-%d").date() - timedelta(days=1)  # 1-day overlap
    else:
        start = today - timedelta(days=30)

    days = []
    d = start
    while d <= today:
        days.append(d.strftime("%Y-%m-%d"))
        d += timedelta(days=1)

    _log("[sync] last stored=%s  fetching %d day(s): %s .. %s" % (last, len(days), days[0], days[-1]))
    if a.dry_run:
        print("\n".join(days))
        return

    g = ensure_session()
    _log("[auth] session ready")
    n_new = n_upd = 0
    for ds in days:
        rec = fetch_day(g, ds)
        if not rec:
            continue
        existed = db.execute("SELECT 1 FROM sleep_daily WHERE date=?", (ds,)).fetchone() is not None
        upsert(db, rec)
        n_new += 0 if existed else 1
        n_upd += 1 if existed else 0
        if n_upd + n_new <= 3 or (n_new + n_upd) % 20 == 0:
            _log("  %s  %.2fh  score=%s" % (ds, rec["sleep_hours"], rec["sleep_score"]))
        db.commit()
    db.commit()

    got = db.execute("SELECT count(*), max(date) FROM sleep_daily WHERE sleep_hours IS NOT NULL").fetchone()
    print("synced: %d new, %d updated | table now %d rows, latest=%s" % (n_new, n_upd, got[0], got[1]))
    db.close()


if __name__ == "__main__":
    main()

