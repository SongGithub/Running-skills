# shoe-tracker-skill

Auto-track running shoe mileage from Strava photos.

## Why

Running shoes lose cushioning and support gradually — you don't feel it day to day, but after 500-800km the foam is compressed, the rubber is worn, and injury risk goes up.

Most runners guess their shoe mileage. This skill **removes the guesswork**:

- **Know when to retire** — track exact km per shoe, no more "I think these have 400km"
- **Catch the sweet spot** — running in shoes at their best (50-300km fresh, 300-600km prime) vs past their prime (600km+)
- **Rotate intelligently** — see which shoes get used most, balance your rotation
- **Injury prevention** — worn shoes alter your gait; knowing mileage helps spot patterns before pain starts

**How it works:** 📸 Strava photo → 🔍 AI identifies shoe → 💾 logs km → 🔗 syncs to Garmin Gear

1. You upload a Strava run with a photo of your shoes
2. Your AI agent identifies the shoe from the photo
3. The distance is recorded to that shoe's log
4. The shoe is bound to the Garmin activity (so Garmin Gear stays in sync)

## Quick Start

1. Set up Garmin + Strava (see `onboarding.md`)
2. Fill in your shoes in `reference/SHOE_TRACKING.md`
3. Run with a shoe photo → ask your agent to track it

## Requirements

- Garmin Connect account
- Strava account with API app
- Python 3.9+ with `garminconnect` library
- AI agent with vision capabilities

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | AI agent instructions |
| `scripts/track_shoe.py` | Fetch Strava photos + distances |
| `scripts/garmin_setup.py` | One-time Garmin login helper |
| `schema/schema.sql` | SQLite database structure |
| `reference/SHOE_TEMPLATE.md` | Template for shoe IDs |
# credential test
