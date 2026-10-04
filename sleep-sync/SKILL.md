---
name: sleep-sync
description: Incremental Garmin sleep sync into a local SQLite table (sleep_daily), plus the sleep metric dictionary and the freshness check that guards the morning report. Use when syncing, backfilling, or analysing Garmin sleep data.
---

# Sleep Sync

One row per night of Garmin sleep data, written incrementally into
\`~/.local/share/coach/memory.db\` → table \`sleep_daily\`.

## Why this exists

The sleep table used to be written **only** by manual backfill scripts
(\`pull_sleep.py\`, \`pull_sleep_detail.py\`). Nothing scheduled them, so the table
silently went two months stale without anyone noticing. The fix separates concerns:

- **data layer** — a launchd job owns the write, deterministically, every morning
- **reasoning layer** — the morning report only *reads* and asserts freshness

Never put the sync inside an LLM turn: a model that skips a step, or a tool call
that fails while the reply still goes out, produces exactly the silent staleness
this module exists to prevent.

## Files

- \`scripts/sleep_sync.py\` — the incremental sync (self-healing auth, no browser/MFA)
- depends on \`garmin_auth.ensure_session()\` from the shared garmin auth module

## Install

1. Copy \`scripts/sleep_sync.py\` into the workspace root next to \`garmin_auth.py\`.
2. Install the launchd job (macOS):

\`\`\`xml
<key>Label</key><string>com.song.sleep-sync</string>
<key>ProgramArguments</key>
<array>
  <string>/opt/homebrew/bin/python3</string>
  <string>/path/to/sleep_sync.py</string>
</array>
<key>StartCalendarInterval</key>
<dict><key>Hour</key><integer>8</integer><key>Minute</key><integer>45</integer></dict>
\`\`\`

Schedule it **before** the morning report, and after any job that refreshes the
Garmin token/cache.

## Usage

\`\`\`bash
python3 sleep_sync.py                 # incremental: last stored date - 1 .. today
python3 sleep_sync.py --from 2026-08-08   # explicit backfill window
python3 sleep_sync.py --days 30
python3 sleep_sync.py --dry-run
\`\`\`

The 1-day overlap on incremental runs is deliberate: Garmin finalises late
data (sleep stress, HRV) after the first sync, so re-writing yesterday repairs it.

## Schema

\`\`\`sql
date TEXT PRIMARY KEY, sleep_hours REAL, sleep_score INTEGER,
sleep_score_qualifier TEXT, avg_hr REAL, deep_sec REAL, light_sec REAL,
rem_sec REAL, awake_sec REAL, sleep_stress REAL, hrv_overnight REAL,
body_battery_change REAL, sleep_need_hours REAL, sleep_start TEXT,
sleep_end TEXT, awake_count INTEGER, restless_moments INTEGER,
respiration REAL, resting_hr REAL, synced_at TEXT
\`\`\`

Missing columns are added with \`ALTER TABLE\` on every run, so the table upgrades itself.

## Freshness contract

The morning report (or any consumer) must assert:

\`\`\`bash
sqlite3 ~/.local/share/coach/memory.db \
  "select max(date) from sleep_daily where sleep_hours is not null"
\`\`\`

If that is not today or yesterday, the consumer must say so explicitly
("sleep DB not synced, last N days missing") and, if possible, re-run
\`sleep_sync.py\`. Silent staleness is the failure mode to avoid.

## Metric notes

- \`sleepScores.*.qualifierKey\` is Garmin's own banding; \`overall.value\` is the 0-100 score.
- Deep/REM/light/awake are **estimates from wrist movement + HR**, not
  polysomnography. Compare against your own history, never absolute norms.
- \`sleepStartTimestampLocal\` / \`sleepEndTimestampLocal\` are offset-shifted
  epoch **milliseconds**; viewing them in UTC yields the local wall clock.
- Devices without the skin-temp sensor return \`null\` for \`avgSkinTempDeviationC\`;
  \`sleepNeed\` is likewise absent on some firmware — treat both as optional.
- Garmin cannot capture caffeine, alcohol, meal timing, room temperature or
  screens. Those need manual logging to be correlated.

