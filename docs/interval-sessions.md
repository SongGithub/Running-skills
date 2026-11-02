# Interval Session Templates

Three quality sessions, each aimed at a **different physiological ceiling**. They
are not interchangeable and should not be stacked in the same week.

**Paces are variables, not constants.** Never train to a number copied from an old
plan. Derive every target from the athlete's *current* anchors and re-derive whenever
a marker moves - or when conditions change (see temperature, below).

> **Keep personal calibration out of this repository.** The snapshot of an individual
> athlete's current 5K time, threshold pace and heart-rate values belongs in their
> private workspace, not here. This file describes the *method*; the numbers are local.

## Pace model

Two anchors; everything else is derived.

| Anchor | How to obtain | Gives |
|---|---|---|
| **Current 5K time** | time trial or race | 5K pace = time / 5 |
| **Current threshold pace (TH)** | field test, watch LT detection, or the heat-corrected method below | TH pace |

| Session target | Derivation |
|---|---|
| VO2max reps (5 x 1000 m) | **= current 5K pace** |
| Threshold reps (4 x 1600 m) | **= current TH pace** |
| Marathon-pace blocks (3 x 5 km) | **= TH pace + 20-25 s/km** |
| Half marathon pace (reference only) | = TH pace + 3-8 s/km |

Fill these in privately for the individual athlete:

    Current 5K : __:__        -> 5K pace  _:__/km
    Threshold  :  _:__/km
    Zones      : Z1 <___ | Z2 ___ | Z3 ___ | Z4 ___ | Z5 ___

### Deriving threshold pace from a race result

If a measured LT is stale or absent, convert a recent race:

1. Take the most recent **maximal** effort at a known distance.
2. Use Riegel (exponent ~1.06) to project the distance that would be covered in
   60 minutes:

       d60 = race_distance x (3600 / race_seconds) ^ (1 / 1.06)

3. Threshold pace is then 3600 / (d60 in km).
4. Cross-check against "half marathon pace - 3 to 5 s/km". If the two disagree by more
   than a few seconds, one input is probably not a maximal effort.

**Sanity checks before trusting a result:**

- A 5K time and a half marathon time must belong to the same fitness level. If the half
  implies a 5K far faster than the recorded one, the 5K was probably not raced.
- A measured threshold pace within ~5 s/km of 5K pace is implausible. Threshold should
  sit roughly 12-20 s/km slower than 5K pace.
- Race conditions matter - see the temperature section.

## Temperature adjustment

Heat raises heart rate at a fixed pace and slows pace at a fixed heart rate. Apply an
adjustment to every pace target:

| Temperature | Adjustment |
|---|---|
| 15 C or below | baseline |
| 15-20 C | +2 to +5 s/km |
| 20-25 C | +5 to +10 s/km |
| 25 C and above | +10 to +15 s/km |

**Operating rule in heat: never chase both pace and heart rate.** Hold the heart-rate
cap and let the pace go. Slowing to protect the effort is the correct call, not a
failed session.

Corollary for calibration: a race run in heat will *understate* true fitness. Either
apply the correction above, or prefer a cool-morning result as the anchor.

## 1. Marathon-pace blocks - 3 x 5 km

**Targets:** marathon-specific endurance - holding goal pace while fatigued, plus race
fuelling rehearsal.

- **Work:** 3 x 5 km at **M pace** (derive as TH + 20-25 s/km)
- **Total quality volume:** 15 km - the largest of the three sessions
- **Heart rate:** Z3
- **Recovery between blocks:** **1 km jog** (2 recoveries), roughly 6-6.5 min each
- **Session size:** 15 km work + 2 km recovery = 17 km, so ~20-22 km with warm-up and
  cool-down
- **When to use:** marathon build only. In a half or 10-12 km block this is too much
  sustained volume - use the threshold session instead.
- **Guardrails:** pace discipline matters more than heart rate. Drifting more than
  5 s/km faster than target means the session is being raced.

## 2. VO2max intervals - 5 x 1000 m

**Targets:** raising the VO2max ceiling - the top end, not sustainable race pace.

- **Work:** 5 x 1000 m at **current 5K race pace**
- **Total quality volume:** 5 km
- **Recovery:** **2-3 min jog** between reps
- **Heart rate:** Z5 by the end of each rep. Early reps lag - judge the session on
  reps 4 and 5, not rep 1.
- **When to use:** specific phase, or to arrest a plateau in top-end speed. Maximum
  once per week, never in the same week as a race.
- **Guardrails:** if rep 4 or 5 cannot hold within 5 s/km of rep 1, stop. Fading
  VO2max reps deliver the fatigue without the adaptation.

## 3. Threshold cruise intervals - 4 x 1600 m

**Targets:** lactate threshold - moving the pace that can be held for an hour.

- **Work:** 4 x 1600 m at **current TH pace**
- **Total quality volume:** 6.4 km
- **Recovery:** **1 min jog** - deliberately short, so lactate does not fully clear
- **Heart rate:** Z4. Reps should finish at or just under LTHR.
- **When to use:** the workhorse session for 10 km to half marathon blocks.
- **Guardrails:** do not extend the 1 min recovery to make it comfortable. But if
  heart rate cannot drop below the top of Z4 in that minute, the pace was above
  threshold.

## Why they are not interchangeable

| Session | Work volume | Primary adaptation | Cost |
|---|---|---|---|
| 3 x 5 km @ M pace | 15 km | Fatigue resistance at goal pace | High (volume-driven) |
| 5 x 1000 m @ 5K pace | 5 km | VO2max ceiling | High (intensity-driven) |
| 4 x 1600 m @ TH pace | 6.4 km | Lactate threshold | Moderate |

The 5 x 1000 m and 4 x 1600 m sessions look similar on paper but sit on opposite sides
of threshold. Running the 1000s at threshold defeats the purpose; running the 1600s at
5K pace turns a controllable session into a race.

## Placement rules

- **Maximum 2 quality sessions per week**, separated by at least 48 hours.
- **One ceiling per week.** Do not pair the VO2max session with the threshold session
  in the same week except in a dedicated overreaching block.
- **Long runs stay easy** (Z2, hard cap at the top of Z2) in any week containing quality.
- **Recovery week:** keep one quality session, cut its volume by roughly 40 percent.
- **Race week:** the race is the quality session. No intervals.

## Recalibration triggers

Recompute every pace when any of these change:

- a new 5K time trial or race result
- a new threshold field test, or watch LT pace moving more than 5 s/km
- a race result at any distance that shifts the fitness baseline
- return from a break of 2+ weeks
- a run done in materially different heat (apply the temperature table instead)
