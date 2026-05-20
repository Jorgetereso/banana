"""Re-roll selected shots using the locked style suffix + cast refs.
Saved as new files (21, 22, ...) — NEVER overwrites originals."""
import os, sys, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_gameplay import run, OUT_DIR, NB, NB_BODY  # STYLE is auto-applied inside run()
from generate_gameplay_cast import ORANGE, GREEN, PURPLE, RED, OCTOPUS, CAST_NOTE

REROLLS = [
    # 17 → 21: four-Pollo huddle (most ambitious cast composition)
    {
        "filename": "21-pollo-huddle-manual-v2.png",
        "endpoint": NB, "extra": dict(NB_BODY, imageUrls=[ORANGE, GREEN, PURPLE, RED]),
        "prompt": (
            "First-person POV at the center of a tight huddle of all FOUR main Pollos pressed "
            "around the camera in the dim Banana Airways cabin. Player hands at the bottom of "
            "the frame hold an open battered booklet labelled \"B.A.N.A.N.A. FLIGHT MANUAL\" "
            "with diagrams of a plane crashing. Surrounding the camera: ORANGE chubby Pollo on "
            "the left pointing at one page, GREEN braided Pollo on the right shaking her head, "
            "PURPLE muscular Pollo behind flexing one arm dramatically, RED mustache Pollo "
            "stroking his mustache contemplatively. All four faces visible, all leaning in. "
            "Warm tungsten cabin light. " + CAST_NOTE
        ),
    },
    # 14 → 22: Red Mustache copilot (single-character protagonism test)
    {
        "filename": "22-red-mustache-copilot-v2.png",
        "endpoint": NB, "extra": dict(NB_BODY, imageUrls=[RED]),
        "prompt": (
            "First-person pilot POV inside the cockpit of a battered Banana Airways propeller "
            "plane. Player hands grip the left yellow Banana Airways yoke at the bottom of the "
            "frame. To the right of the player, in the co-pilot seat, the RED Pollo with the "
            "magnificent handlebar mustache is twirling the tip of his mustache with one fuzzy "
            "hand while completely ignoring the alarm lights — sleepy droopy green eyes, smug "
            "calm expression. The other yoke vibrates wildly in front of him. Through the "
            "cracked windshield: a thunderstorm with lightning, fuel gauge needle red. " + CAST_NOTE
        ),
    },
]


def main():
    print(f"Re-rolling {len(REROLLS)} shots with the locked v2 style suffix\n")
    results = {}
    threads = [threading.Thread(target=run, args=(j, results), daemon=True) for j in REROLLS]
    for t in threads:
        t.start(); time.sleep(0.4)
    for t in threads:
        t.join()
    print("\nDONE:")
    for j in REROLLS:
        print(f"  {j['filename']:35s} {results.get(j['filename'], ('missing',))[0]}")


if __name__ == "__main__":
    main()
