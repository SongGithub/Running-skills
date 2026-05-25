# shoe-manager

Track running shoe mileage from Strava photos + get smart recommendations on what to wear.

## Why

Running shoes lose cushioning and support gradually — you don't feel it day to day, but after 500-800km the foam is compressed, the rubber is worn, and injury risk goes up. Most runners guess.

This skill removes the guesswork with **two superpowers**:

### 📸 Track
- **Know exactly how many km each shoe has** — no more "I think these have 400km"
- **Catch the sweet spot** — shoes perform best from 50-350km, start degrading after 400-500km
- **Injury prevention** — worn shoes alter your gait; tracking mileage catches patterns before pain starts
- **Auto-sync to Garmin Gear** — Strava photo → record → Garmin, all automatic

### 👟 Recommend
- **Right shoe for the right workout** — max cushion for recovery, speed trainers for intervals, carbon plate for race day
- **RunRepeat-verified categories** — each shoe classified by lab data, not guesswork
- **Lifecycle-aware** — won't suggest a 550km shoe for your marathon

## How It Works

**Track:** 📸 Strava photo → 🔍 AI identifies shoe → 💾 logs km → 🔗 syncs to Garmin Gear
**Recommend:** 📋 check workout → 📊 check mileage → 🏆 match shoe → 💬 explain why

## Quick Start

1. Set up Garmin + Strava (see `onboarding.md`)
2. Fill in your shoes in `reference/SHOE_TRACKING.md` (include visual IDs + RunRepeat category)
3. Run with a shoe photo → ask your agent to track
4. Ask "what should I wear today?" → get a recommendation

## Requirements

- Garmin Connect account
- Strava account with API app
- Python 3.9+ with `garminconnect` library
- AI agent with vision capabilities

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | AI agent instructions (track + recommend) |
| `reference/SHOE_TRACKING.md` | Shoe visual IDs + RunRepeat categories + recommendation matrix |
| `scripts/track_shoe.py` | Fetch Strava photos + distances |
| `scripts/garmin_setup.py` | One-time Garmin login helper |
| `schema/schema.sql` | SQLite database structure |
| `onboarding.md` | Step-by-step setup guide |
