# strava-club-workout-skill

Convert Strava club group events into Garmin workouts automatically.

## What It Does

1. Fetches group events from a Strava club (e.g. MRC Wednesday Quality)
2. Parses the workout description (intervals, tempo, threshold, etc.)
3. Creates a properly formatted Garmin workout
4. Schedules it on the user's Garmin calendar

## Trigger

- "what's the MRC Wednesday quality?"
- "create a workout from the club event"
- "schedule the next MRC session to my Garmin"

## Flow

### Step 1 — Fetch club group events
```python
/clubs/{CLUB_ID}/group_events
```

Find events with upcoming_occurrences matching this week. Each event has:
- title, description, upcoming_occurrences list
- description contains the full workout plan

### Step 2 — Parse the workout description
Club event descriptions typically include:
- Warmup details
- Main set (intervals, tempo, threshold with reps/distances/times)
- Recovery between efforts
- Cooldown

### Step 3 — Build Garmin workout

Key Garmin workout API facts (learned the hard way):

| Fact | Detail |
|------|--------|
| **conditionTypeId for distance** | 3 (not 1 from library's ConditionType.DISTANCE) |
| **conditionTypeId for time** | 2 |
| **targetTypeId for pace.zone** | 6 (not in library) |
| **targetTypeId for heart.rate.zone** | 4 |
| **Pace values in pace.zone** | m/s, NOT seconds/km (4.22 = 3:57/km) |
| **Distance unit for <1km** | unitId: 1, unitKey: "meter", factor: 100.0 |
| **Distance unit for ≥1km** | unitId: 2, unitKey: "kilometer", factor: 100000.0 |
| **RepeatGroup** | Use for repeating sets (8x400m, 6x1km) |
| **zoneNumber** | 4 = threshold, 5 = VO2max |

Pace conversion reference:
```
3:00/km = 5.56 m/s    4:00/km = 4.17 m/s
3:30/km = 4.76 m/s    4:30/km = 3.70 m/s
3:45/km = 4.44 m/s    5:00/km = 3.33 m/s
3:57/km = 4.22 m/s    5:30/km = 3.03 m/s
```

### Step 4 — Schedule
```python
g.schedule_workout(workout_id, 'YYYY-MM-DD')
```
The date comes from the event's `upcoming_occurrences` field (in UTC).

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | This file |
| `scripts/fetch_event.py` | Fetch and display club events |
| `scripts/predict_time.php` | (optional) Predict event times |

## Known Clubs

| Club | Strava ID |
|------|-----------|
| Mad Rabbit Crew | 882047 |
| DCT Running Crew | 1259829 |
