# Morning Routine - Interactive Prototype

> **Instructions**: Scroll through this document as if you're using the app. Imagine each screen is your phone. Tell me what works, what doesn't, what feels annoying, what feels good.

---

## SCREEN 0: Entry Point

**Context**: You've just opened your phone. You finished your nightly checkout last night. Now it's morning.

```
┌─────────────────────────────────────┐
│  ☰                  SISO INTERNAL    │
├─────────────────────────────────────┤
│                                      │
│           [BOTTOM NAV]               │
│   ┌─────┬─────┬─────┬─────┐         │
│   │Plan │Task │Stats│More │         │
│   └─────┴─────┴─────┴─────┘         │
│                                      │
│    ┌─────────────────────────────┐   │
│    │                             │   │
│    │     🌅 Morning Routine       │   │
│    │     Start your day right    │   │
│    │                             │   │
│    │   [ START ROUTINE ]          │   │
│    │                             │   │
│    └─────────────────────────────┘   │
│                                      │
│    Yesterday: 420 XP ⭐⭐⭐           │
│    Streak: 7 days 🔥                 │
└─────────────────────────────────────┘
```

**Questions:**
- Does this feel like a natural entry point?
- Or would you prefer to tap "Plan" and then see this?
- Is seeing yesterday's XP motivating or annoying?

---

## SCREEN 1: Step Progress Overview

**Context**: You tapped "START ROUTINE". Now you see the flow.

```
┌─────────────────────────────────────┐
│  Morning Routine    XP: +120    ☰  │
├─────────────────────────────────────┤
│  ● ○ ○ ○ ○                           │
│  Wake → Freshen → Flow → Power →    │
└─────────────────────────────────────┘
│
│  ┌─────────────────────────────────┐ │
│  │   STEP 1 OF 5                  │ │
│  │   Wake Up & Manifestation       │ │
│  │                                 │ │
│  │   ⏰ Estimated: 2 min            │ │
│  │                                 │ │
│  │   Yesterday you woke up at      │ │
│  │   6:45 AM and earned 120 XP     │ │
│  │                                 │ │
│  │   [← Previous]  [Skip →]  [→]   │ │
│  └─────────────────────────────────┘ │
└──────────────────────────────────────┘
```

**Questions:**
- Can you see all steps? Is it clear what's coming?
- Is the step count (1 of 5) helpful or stressful?
- Does seeing yesterday's wake time motivate you?
- What if you want to skip this step?

---

## SCREEN 2: Wake Up - Main View

**Context**: You tapped "Next" or clicked on step 1.

```
┌─────────────────────────────────────┐
│  Morning Routine    XP: +120    ☰  │
├─────────────────────────────────────┤
│  ● ○ ○ ○ ○                           │
│  Wake → Freshen → Flow → Power →    │
└─────────────────────────────────────┘
│
│  ┌─────────────────────────────────┐ │
│  │   🌅 Wake Up & Manifestation   │ │
│  ├─────────────────────────────────┤ │
│  │                                 │ │
│  │   Today's Theme:                │ │
│  │   "Focus on deep work blocks"   │ │
│  │                                 │ │
│  │   ──────────────────────────    │ │
│  │                                 │ │
│  │   Yesterday's Stats:            │ │
│  │   • 420 XP earned               │ │
│  │   • Woke at 6:45 AM             │ │
│  │   • 5/5 habits completed        │ │
│  │                                 │ │
│  │   ──────────────────────────    │ │
│  │                                 │ │
│  │   Log Wake Time:                │ │
│  │   [ 6:30 AM 🕐 ]                │ │
│  │                                 │ │
│  │   [ Auto-detect ] [ Manual ]    │ │
│  │                                 │ │
│  │   [ COMPLETE STEP → ]           │ │
│  └─────────────────────────────────┘ │
│                                      │
│  [← Back]  [Skip →]  [Next Step →]   │
└──────────────────────────────────────┘
```

**Questions:**
- Is the theme visible enough?
- Are yesterday's stats helpful context or clutter?
- How would you actually log wake time? Scroll? Type?
- Do you want auto-detect (phone unlock time) or manual?
- Does "COMPLETE STEP" feel satisfying?

---

## INTERACTION: You Tap "COMPLETE STEP"

**What happens:**
- XP animation: +120 XP floats up
- Checkmark appears on step 1 in progress bar
- Progress bar updates: ●● ○ ○ ○
- Screen transitions to step 2

**Question:**
- Does the immediate XP reward feel good?
- Or do you prefer waiting until the end?

---

## SCREEN 3: Freshen Up - Activity Selection

**Context**: Step completed. Now moving to freshen up.

```
┌─────────────────────────────────────┐
│  Morning Routine    XP: +160    ☰  │
├─────────────────────────────────────┤
│  ●● ○ ○ ○                           │
│  Wake → Freshen → Flow → Power →    │
└─────────────────────────────────────┘
│
│  ┌─────────────────────────────────┐ │
│  │   STEP 2 OF 5                  │ │
│  │   Freshen Up                    │ │
│  │                                 │ │
│  │   ⏰ Estimated: 3-5 min          │ │
│  │                                 │ │
│  │   Select your activity:         │ │
│  │                                 │ │
│  │   ┌─────────────────────────┐   │ │
│  │   │ 🚿 Shower               │   │ │
│  │   │ Regular or cold         │   │ │
│  │   └─────────────────────────┘   │ │
│  │                                 │ │
│  │   ┌─────────────────────────┐   │ │
│  │   │ 🪥 Brush Teeth          │   │ │
│  │   │ + Bathroom break        │   │ │
│  │   └─────────────────────────┘   │ │
│  │                                 │ │
│  │   ┌─────────────────────────┐   │ │
│  │   │ 🧼 Face wash + quick    │   │ │
│  │   │ get ready               │   │ │
│  │   └─────────────────────────┘   │ │
│  │                                 │ │
│  │   [← Previous]  [Skip →]  [→]   │ │
│  └─────────────────────────────────┘ │
└──────────────────────────────────────┘
```

**Questions:**
- Are these the right options? What's missing?
- Do you ever do multiple of these? How should that work?
- Is 3-5 min accurate or annoying?
- What if you want to skip this? (Skip button)

---

## SCREEN 4: Freshen Up - Timer Active

**Context**: You selected "Shower - Cold". Timer starts.

```
┌─────────────────────────────────────┐
│  Morning Routine    XP: +160    ☰  │
├─────────────────────────────────────┤
│  ●● ○ ○ ○                           │
│  Wake → Freshen → Flow → Power →    │
└─────────────────────────────────────┘
│
│  ┌─────────────────────────────────┐ │
│  │   🚿 Cold Shower               │ │
│  │                                 │ │
│  │        ⏱️  2:34                 │ │
│  │                                 │ │
│  │   Timer running...              │ │
│  │                                 │ │
│  │   [ PAUSE ]  [ FINISH EARLY ]   │ │
│  │                                 │ │
│  │   💡 Pro tip: Cold showers     │ │
│  │   increase dopamine!           │ │
│  │                                 │ │
│  │   [← Cancel]                   │ │
│  └─────────────────────────────────┘ │
└──────────────────────────────────────┘
```

**Questions:**
- Do you want the timer running automatically?
- Or should you manually start/stop it?
- Is the pro tip helpful or distracting?
- What if you finish early? Does that affect XP?

---

## INTERACTION: You Finish the Shower

**What happens:**
- Timer stops at 3:12
- Screen shows: "Great! You earned +40 XP"
- Bonus: "Speed bonus! +25 XP (under 5 min from wake up)"
- Total: +65 XP floats up
- Step 2 checks off: ●●● ○ ○

**Question:**
- Does the speed bonus motivate you?
- Or does it stress you out?

---

## SCREEN 5: Skip Confirmation

**Context**: Let's say you want to skip "Get Blood Flowing" (exercise).

```
┌─────────────────────────────────────┐
│  Morning Routine    XP: +225    ☰  │
├─────────────────────────────────────┤
│  ●●● ○ ○                            │
│  Wake → Freshen → Flow → Power →    │
└─────────────────────────────────────┘
│
│  ┌─────────────────────────────────┐ │
│  │   ⚠️ Skip this step?            │ │
│  │                                 │ │
│  │   Get Blood Flowing             │ │
│  │   (Push-ups, exercise, etc.)    │ │
│  │                                 │ │
│  │   Why are you skipping?         │ │
│  │                                 │ │
│  │   ⚪ Not enough time             │ │
│  │   ⚪ Feeling unwell              │ │
│  │   ⚪ Already exercised today     │ │
│  │   ⚪ Other reason                │ │
│  │                                 │ │
│  │   [ Other: _____________ ]      │ │
│  │                                 │ │
│  │   [ Cancel ]  [ Confirm Skip ]  │ │
│  └─────────────────────────────────┘ │
└──────────────────────────────────────┘
```

**Questions:**
- Does requiring a reason feel accountable or annoying?
- Are the right skip reasons listed?
- What if you skip the same step 3 days in a row?
- Should it suggest removing that step from your routine?

---

## SCREEN 6: Rush Mode

**Context**: You're running late. You tapped "Rush Mode" toggle.

```
┌─────────────────────────────────────┐
│  ⚡ Rush Mode ON    XP: +225    ☰  │
├─────────────────────────────────────┤
│  ●●●● ○                              │
│  Wake → Freshen → Flow → Power →    │
└─────────────────────────────────────┘
│
│  ┌─────────────────────────────────┐ │
│  │   STEP 4 OF 5                  │ │
│  │   Power Up Brain               │ │
│  │                                 │ │
│  │   Quick complete mode           │ │
│  │                                 │ │
│  │   Water: [500ml] [1000ml]       │ │
│  │   Supplements: [✓] Done         │ │
│  │                                 │ │
│  │   [ SKIP ALL REMAINING → ]      │ │
│  │                                 │ │
│  │   [← Previous]  [→]             │ │
│  └─────────────────────────────────┘ │
└──────────────────────────────────────┘
```

**Questions:**
- Does rush mode feel helpful or like cheating?
- Should "SKIP ALL" require one reason for everything?
- Or individual reasons for each skipped step?
- Does rush mode reduce XP or stay the same?

---

## SCREEN 7: Summary Screen

**Context**: You completed all steps.

```
┌─────────────────────────────────────┐
│  ✓ Morning Routine Complete!  ☰   │
├─────────────────────────────────────┤
│                                      │
│     🎉 Great job today!             │
│                                      │
│  ┌─────────────────────────────────┐ │
│  │   TODAY'S PERFORMANCE           │ │
│  ├─────────────────────────────────┤ │
│  │                                 │ │
│  │   Total XP: +285                │ │
│  │   ⭐⭐⭐⭐⭐                       │ │
│  │                                 │ │
│  │   Steps completed: 4/5          │ │
│  │   Time: 18 minutes              │ │
│  │                                 │ │
│  │   ──────────────────────────    │ │
│  │                                 │ │
│  │   Wake Up:      +120 XP         │ │
│  │   Freshen Up:   +65 XP          │ │
│  │   Power Up:     +100 XP         │ │
│  │   (Skipped: Exercise)           │ │
│  │                                 │ │
│  │   ──────────────────────────    │ │
│  │                                 │ │
│  │   Streak: 7 days 🔥             │ │
│  │   Weekly avg: 310 XP            │ │
│  │                                 │ │
│  │   [ VIEW DETAILS ]              │ │
│  │   [ CONTINUE TO DAY → ]         │ │
│  └─────────────────────────────────┘ │
└──────────────────────────────────────┘
```

**Questions:**
- Is this summary satisfying?
- Do you want to see XP breakdown or just total?
- Is the streak display motivating?
- What does "CONTINUE TO DAY" mean? Go to Timebox?

---

## ALTERNATIVE: Progress Bar Instead of Steps

**Context**: Maybe you prefer a simpler progress indicator.

```
┌─────────────────────────────────────┐
│  Morning Routine    XP: +160    ☰  │
├─────────────────────────────────────┤
│  ████████████░░░░░░░░  40%          │
│  Step 2 of 5                       │
└─────────────────────────────────────┘
```

**Question:**
- Dots (●● ○ ○) vs Progress bar (██████░░░)?
- Which gives you a better sense of progress?

---

## ALTERNATIVE: Vertical Sidebar (Desktop)

**Context**: What if you're on desktop/tablet?

```
┌─────────────────────────────────────────────┐
│  Morning Routine              XP: +160   ☰  │
├─────────────────────────────────────────────┤
│                                              │
│  ┌────────┐  ┌──────────────────────────┐  │
│  │ ● Wake │  │   🚿 Cold Shower         │  │
│  │ ●Fresh │  │                          │  │
│  │ ○ Flow │  │   Timer: 2:34            │  │
│  │ ○Power │  │                          │  │
│  │ ○Plan  │  │   [ PAUSE ] [ FINISH ]   │  │
│  │        │  │                          │  │
│  │        │  │   💡 Cold showers        │  │
│  │  Rush  │  │      increase dopamine!  │  │
│  │  Mode  │  └──────────────────────────┘  │
│  └────────┘                                 │
└──────────────────────────────────────────────┘
```

**Question:**
- Do you ever use the app on desktop?
- Would a sidebar be better than top progress?

---

## EDGE CASE: Interruption

**Context**: You're on step 3, get a phone call, close the app.

**What happens when you reopen:**

```
┌─────────────────────────────────────┐
│  ⏸️ Routine Paused                  │
├─────────────────────────────────────┤
│                                      │
│  You were on step 3 of 5            │
│                                      │
│  "Get Blood Flowing"                │
│                                      │
│  [ RESUME WHERE I LEFT OFF ]        │
│  [ START OVER ]                      │
│  [ VIEW PROGRESS ]                   │
│                                      │
└──────────────────────────────────────┘
```

**Question:**
- Is this the right behavior?
- Or should it auto-resume without asking?

---

## CRITICAL QUESTION: Step Order

**Current proposed order:**
1. Wake Up
2. Freshen Up
3. Get Blood Flowing
4. Power Up Brain
5. Plan Day

**Your reality:**
- Do you actually do them in this order?
- What if you exercise BEFORE freshening up?
- What if you drink water WHILE planning your day?

**Proposal:**
- Default order as shown
- Steps are clickable - jump to any step
- Mark steps complete in any order
- Only requirement: all marked complete to finish

**Question:**
- Does this flexibility solve the rigidity problem?
- Or does it break the "guided flow" concept?

---

## CRITICAL QUESTION: Nighttime vs Morning

**Current proposal:**
- Morning: Stepped flow (what you're reviewing)
- Nightly: Keep scrolling (current design)

**Rationale:**
- Morning = sequential, active, momentum-based
- Nightly = reflective, flexible, review-based

**Question:**
- Do you agree with this distinction?
- Or should nightly also be stepped?

---

## FINAL FEEDBACK QUESTIONS

**Overall:**
1. Does this feel like an improvement over the current scrolling page?
2. What's the ONE thing that would make you hate this?
3. What's the ONE thing that would make you love this?
4. What's missing?
5. What should I remove?

**Specific:**
1. How do you feel about the step indicator? Dots vs progress bar?
2. Is rush mode necessary or does it complicate things?
3. Should skips require reasons?
4. Immediate XP per step or delayed until end?
5. Can you imagine actually using this every morning?

---

## YOUR TURN

**Tell me:**
- What works?
- What doesn't?
- What feels wrong?
- What feels right?
- What would you change?
- Would you use this?

**Be honest.** This is just a prototype - nothing is built. Better to critique now than after we code it.

---

## Sources
- Based on research from: [32 Stepper UI Examples](https://www.eleken.co/blog-posts/stepper-ui-examples)
- [Form Wizard Best Practices](https://www.andrewcoyle.com/blog/how-to-design-a-form-wizard)
- Current implementation: `src/domains/lifelock/1-daily/1-morning-routine/ui/pages/MorningRoutineSection.tsx`
