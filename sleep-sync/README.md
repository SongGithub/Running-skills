# sleep-sync

Incremental Garmin sleep → SQLite sync. See [SKILL.md](SKILL.md).

- \`scripts/sleep_sync.py\` — headless, self-healing auth, 1-day overlap on incremental runs
- writes \`~/.local/share/coach/memory.db\` → \`sleep_daily\`
- runs from launchd \`com.song.sleep-sync\` at 08:45, **before** the morning report
- the morning report only reads the table and asserts freshness — the sync is never
  run from inside an LLM turn

No personal data is stored in this repo; the script reads credentials from the
local keychain/token file at runtime.

