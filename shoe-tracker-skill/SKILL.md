# shoe-tracker-skill — Auto-track Running Shoe Mileage from Strava Photos

A modular skill for AI agents to automatically record shoe mileage when a runner uploads a Strava activity with a shoe photo.

## What It Does

**camera 📸 → identify shoe 🔍 → record km 💾 → bind Garmin Gear 🔗**

When the user says something like "帮我记一下这双鞋的公里数" or "add the km to the shoe in the photo":

1. Fetch latest Strava activity with a photo
2. Use image analysis to identify the shoe model
3. Look up the shoe in the local database
4. Record the distance to that shoe
5. Bind the shoe as gear on the Garmin activity (so Garmin Gear stays in sync)

## Prerequisites for User

- **Garmin Connect** account (email/password)
- **Strava** account with API app (client_id + client_secret)
- Ability to take shoe photos and upload them with Strava runs

## Required Files (created during onboarding)

| File | Purpose |
|------|---------|
| `config/garmin_tokens.json` | Garmin API session tokens |
| `config/strava_config.json` | Strava API client_id/secret/refresh_token |
| `runs.db` | SQLite database with shoes + run_shoes tables |
| `reference/SHOE_TRACKING.md` | Shoe visual identification guide |

## Directory Structure

```
shoe-tracker-skill/
├── SKILL.md                ← This file
├── onboarding.md           ← Setup guide for the user
├── scripts/
│   ├── track_shoe.py       ← Main: fetch photo → identify → record → bind
│   └── garmin_setup.py     ← Garmin login/token helper
├── schema/
│   └── schema.sql          ← Database table creation
└── reference/
    └── SHOE_TEMPLATE.md    ← Template for user to fill with their shoes
```

## Full End-to-End Flow

### Trigger
User uploads a Strava run with a shoe photo and asks to track the mileage.

### Step 1 — Fetch latest Strava activity with photos
Refresh Strava OAuth token, get recent activities, find one with `total_photo_count > 0`, extract photo URL from `photos.primary.urls.600`.

### Step 2 — Identify shoe via image analysis
Use the AI agent's vision capabilities on the photo URL. Match against `reference/SHOE_TRACKING.md` visual features (brand logos, colorways, stripe patterns, unique identifiers).

### Step 3 — Record mileage in local database
```sql
INSERT INTO run_shoes (shoe_id, date, distance_km, source, activity_id)
VALUES (?, ?, ?, 'strava', ?);

UPDATE shoes SET current_km = current_km + ?, total_runs = total_runs + 1
WHERE id = ?;
```

### Step 4 — Bind gear to Garmin activity
Garmin activities don't auto-assign gear from Strava sync. Must call:
```python
g.add_gear_to_activity(gear_uuid, garmin_activity_id)
```
Find the `gear_uuid` via `g.get_gear(user_profile_id)` and match `customMakeModel` to the shoe name.

### Step 5 — Confirm with user
"已记录 ✅ 新增Xkm，共XXkm"

## Key Garmin Gear UUIDs (known)

If the skill has been used before, gear UUIDs are stored in the database. Otherwise, look them up at runtime from Garmin's gear API.

## Known Issues

- Garmin tokens expire periodically and need MFA re-auth (codes go to user's email)
- Strava tokens auto-refresh via `refresh_token`
- The agent MUST check if the Garmin activity already has gear assigned before attempting to bind
- Do NOT track non-running activities (cycling, hiking, etc.)
