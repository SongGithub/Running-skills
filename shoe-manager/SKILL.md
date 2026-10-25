# shoe-tracker-skill — Track + Recommend Running Shoes

A modular skill for AI agents that:
1. **Track** — Auto-record shoe mileage when user uploads a Strava run with a shoe photo
2. **Recommend** — Suggest which shoe to wear based on today's workout, mileage, and RunRepeat classification

---

## 🎯 Purpose

Running shoes lose cushioning and support gradually. After 500-800km the foam is compressed and injury risk goes up. This skill removes the guesswork:

- **Know when to retire** — track exact km per shoe
- **Catch the sweet spot** — run in shoes at their best (50-300km fresh, 300-600km prime)
- **Rotate intelligently** — see which shoes get used most
- **Injury prevention** — worn shoes alter your gait
- **Get recommendations** — the right shoe for every workout

---

## 📸 Part 1: Shoe Mileage Tracking

### Trigger
User uploads a Strava run with a shoe photo and says something like:
- "add the km to the shoe in the photo"
- "track this shoe's mileage"
- "记一下这双鞋的公里数"

### Step 1 — Fetch latest Strava activity with photos
Refresh Strava OAuth token, get recent activities, find one with `total_photo_count > 0`, extract photo URL from `photos.primary.urls.600`.

### Step 2 — Identify shoe via image analysis
Use the AI agent's vision capabilities on the photo URL. Match against `reference/SHOE_TRACKING.md` visual features (brand logos, colorways, stripe patterns, unique identifiers).

### Step 3 — Record mileage in local database
```sql
INSERT INTO run_shoes (shoe_id, date, distance_km, source, strava_activity_id)
VALUES (?, ?, ?, 'strava', ?);

UPDATE shoes SET current_km = current_km + ?, total_runs = total_runs + 1
WHERE id = ?;
```

### Step 4 — Bind gear to Garmin activity
Garmin activities from Strava sync don't auto-assign gear. Must call:
```python
g.add_gear_to_activity(gear_uuid, garmin_activity_id)
```
Find the `gear_uuid` via `g.get_gear(user_profile_id)` and match `customMakeModel` to the shoe name.

### Step 5 — Confirm
"Recorded ✅ +Xkm, total XXkm"

---

## 👟 Part 2: Shoe Recommendation

### Trigger
User asks what to wear today:
- "what shoes should I wear today?"
- "今天穿什么鞋？"
- "suggest a shoe for my tempo run"

### How to Recommend

1. **Check the workout type** from today's training plan (recovery, easy, long run, tempo, intervals, race, trail)

2. **Check the shoe's RunRepeat category** in `reference/SHOE_TRACKING.md`

3. **Check current mileage** from the `shoes` table — lower km = fresher

4. **Consider lifecycle**:
   - 0-150km: 🆕 Fresh — any run
   - 150-350km: ✅ Sweet spot — ideal for race/speed
   - 350-500km: ⚠️ Aging — daily only, not races
   - 500-650km: 🔄 Retire soon — recovery only
   - 650km+: ❌ Retired — replace

5. **Recommend by workout:**

| Workout | Best Category | Examples from database |
|---------|--------------|----------------------|
| Recovery run | Max Cushion | Triumph 21, 1080 V13, Vomero Plus, Novablast 5 |
| Easy run (Z2) | Daily Trainer | Ride 18, SL2, EVO SL |
| Long run (Z2) | Daily Trainer / Max Cushion | EVO SL, Novablast 5, SL2, Ride 18 |
| Tempo/Threshold | Speed Trainer | Endorphin Speed 4 v2, Rebel V4, Adios 9, 260X 2.0 |
| Intervals (VO2max) | Speed Trainer | Adios 9, Rebel V4, 260X 2.0 |
| Race day | Carbon Plated Super Shoe | Adios Pro 4 🏆, Endorphin Pro 4, Metaspeed |
| Trail | Trail | Xodus |

6. **Explain why** — mention the shoe's category and current mileage:
   > "Today's threshold session — wear **Adios 9**, it's a firm speed trainer at only 98km, perfect for Z4 work."

---

## ⚠️ Known Issues

- Garmin tokens expire periodically and need MFA re-auth (codes go to user's email)
- Strava tokens auto-refresh via `refresh_token`
- Always check if the Garmin activity already has gear assigned before attempting to bind
- Do NOT track non-running activities (cycling, hiking)
- Recommendations should prioritize lower-mileage shoes when multiple options exist in the same category
