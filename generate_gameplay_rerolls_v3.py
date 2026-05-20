"""Re-roll the four-character huddle with the v3 (strict anti-bird) CAST_NOTE.
Saved as 23-cast-huddle-manual-v3.png. Does NOT touch existing 17 or 21."""
import os, sys, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_gameplay import run, OUT_DIR, NB, NB_BODY
from generate_gameplay_cast import ORANGE, GREEN, PURPLE, RED, CAST_NOTE

REROLLS = [
    {
        "filename": "23-cast-huddle-manual-v3.png",
        "endpoint": NB, "extra": dict(NB_BODY, imageUrls=[ORANGE, GREEN, PURPLE, RED]),
        "prompt": (
            "First-person POV at the center of a tight huddle of all FOUR main characters "
            "pressed around the camera in the dim Banana Airways cabin. Player hands at the "
            "bottom of the frame hold an open battered booklet labelled \"B.A.N.A.N.A. "
            "FLIGHT MANUAL\" with diagrams of a plane crashing. Surrounding the camera: "
            "ORANGE CHUBBY character on the left pointing at one page, GREEN PIGTAILS "
            "character on the right shaking her head, PURPLE MUSCLE character behind "
            "flexing one arm dramatically, RED MUSTACHE character stroking his mustache "
            "contemplatively. All four faces visible, all leaning in. Warm tungsten cabin "
            "light. Each character must look identical to the attached reference image — "
            "with thick rubber lips, NOT beaks. " + CAST_NOTE
        ),
    },
]


def main():
    print(f"Re-rolling {len(REROLLS)} shot with v3 CAST_NOTE (anti-bird hammered)\n")
    results = {}
    threads = [threading.Thread(target=run, args=(j, results), daemon=True) for j in REROLLS]
    for t in threads:
        t.start(); time.sleep(0.3)
    for t in threads:
        t.join()
    print("\nDONE:")
    for j in REROLLS:
        print(f"  {j['filename']:35s} {results.get(j['filename'], ('missing',))[0]}")


if __name__ == "__main__":
    main()
