# Aerobic Decoupling Test (Pa:HR)

A repeatable field test for aerobic durability: how much heart rate drifts upward
at a steady, easy effort over 90 minutes.

## What it measures

Cardiac drift — the rise in heart rate relative to speed as a run goes on. Low
drift means the aerobic system is holding efficiency; high drift means the cost
of a given pace is climbing (fitness, heat, dehydration, glycogen depletion or
fatigue).

It is a **trend tool**, not a single-day verdict. One test proves little; three
tests under the same conditions show direction.

## Procedure

1. **Route** — flat loop, minimal climbing, ideally something you can repeat exactly.
2. **Conditions** — start in cool conditions and keep the **maximum temperature at or below 24 C**
   for the whole run. Average temperature alone is not enough: a run that averages
   22 C but peaks at 26 C is already heat-affected in the final third.
   Avoid wind, direct sun and unusually humid days.
3. **Effort** — steady easy pace, conversational. Roughly 65-75% of LTHR.
   Hold pace, not heart rate; the whole point is to watch what heart rate does.
4. **No fuelling** — no food or drink during the 90 minutes. Keep caffeine intake
   the same as a normal run.
5. **Duration** — 90 minutes of continuous running. Warm up inside the run, not before.
6. **Sampling**
   - `a` = mean heart rate between minute 9:30 and 10:30
   - `b` = mean heart rate over the final 5 minutes, ending at minute 90
7. **Do not sprint the finish.** Any late acceleration invalidates the comparison.

## Calculation

```
decoupling % = (b - a) / a * 100
```

Also record the pace of both windows. If pace moved by more than ~10 s/km between
them, treat the raw number as unreliable and compare heart rate per unit speed instead:

```
pace_adjusted % = ((b / speed_b) / (a / speed_a) - 1) * 100
```

## Interpretation

| Result | Reading |
|---|---|
| 5% or less | Elite / well-developed aerobic durability |
| 5-10% | Good; normal for most trained runners |
| 10-15% | Aerobic endurance is the limiter; more easy volume and longer steady runs |
| Above 15% | Re-check conditions first (heat, pace drift, under-fuelling), then treat as a base-building priority |

Negative values mean heart rate fell at the same pace. That is fine and usually
reflects a well-executed warm-up rather than a measurement error.

## Common ways to break the test

- **Pace drift.** Slowing down lowers heart rate and flatters the result; speeding
  up raises it and makes the result look worse. Steady pace is the whole test.
- **Hills.** Even gentle rollers change the workload enough to distort the numbers.
- **Heat.** The single largest external confounder. Cap the maximum temperature.
- **Dehydration and low glycogen.** Both push heart rate up independently of fitness.
- **Caffeine or a late meal.** Keep pre-run routine identical between tests.
- **Comparing across seasons.** A cool-weather test and a summer test are not comparable.

## Frequency

Every 4-6 weeks, same route, same time of day. Keep the test as that week's long
run — it replaces training rather than adding to it.

## Computing it from Garmin data

Activity detail metrics provide 1 Hz samples. Relevant fields:

| Metric | Unit handling |
|---|---|
| `directHeartRate` | bpm, as-is |
| `sumMovingDuration` | seconds, as-is |
| `sumDistance` | centimetres, divide by 100 |
| `directSpeed` | metres per second, as-is |

Take the mean of `directHeartRate` in the two windows above; everything else is
bookkeeping. Record temperature from the activity summary alongside the result.
