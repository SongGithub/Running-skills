# strava-club-workout-skill

Convert Strava club group events into Garmin workouts.

## Why

Club coaches post detailed workouts in Strava group events, but you have to manually recreate them in Garmin. This skill does it automatically — reads the event, builds the workout, schedules it to your watch.

## Quick Start

```bash
# See what's coming up
python3 scripts/fetch_event.py mrc

# Get full details  
python3 scripts/fetch_event.py mrc detail
```

## How It Works

1. Strava API → club group events with descriptions
2. Parse the session details (threshold, 400s, recoveries)
3. Build Garmin workout with correct units and targets
4. Schedule to your watch

## Critical API Facts

See `SKILL.md` for the complete Garmin workout API reference. Key points:

- Distance steps use conditionTypeId=3 (not 1)
- Pace zone target uses values in m/s, NOT seconds/km
- Sub-1km distances use unit meter (unitId=1), not kilometer
