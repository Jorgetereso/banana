"""Re-roll props 03 + 04 — the originals leaked POV hands / characters.
This time: explicit still-life / unmanned camera framing, no first person."""
import os, sys, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_gameplay import NB, NB_BODY
from generate_props import PROP_STYLE, run_to_props

# Even stricter framing rules to keep the camera away from POV
HARD_NO_PEOPLE = (
    "\n\nCRITICAL FRAMING RULES — do not break these:\n"
    "- The camera is an UNATTENDED static cinematic camera. There is NO PLAYER, "
    "NO HANDS, NO ARMS, NO PEOPLE, NO CREATURES, NO CHARACTERS anywhere in the frame.\n"
    "- This is a still-life / environment hero shot, NOT a first-person POV gameplay shot.\n"
    "- If you would normally render player hands at the bottom of the frame, DO NOT. "
    "The bottom of the frame is empty cabin floor or empty seat, not hands.\n"
    "- The cabin is completely EMPTY of any living thing. Just the prop and the environment."
)

REROLLS = [
    {
        "filename": "03-airborne-debris.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "Cinematic environment shot from an unmanned camera mounted at head height in "
            "the middle of the aisle of a battered BANANA AIRWAYS cabin during violent "
            "turbulence. Food trays, plastic cups, foil snack bags, bananas, a tumbling "
            "coffee can, magazines, a thrown safety card and paper boarding passes are "
            "all suspended mid-air across the frame, captured frozen in chaotic tumbling "
            "arcs with frozen motion-blur trails. The cabin floor tilts hard to one side. "
            "Yellow BANANA AIRWAYS seats are EMPTY, seatbelts dangling unbuckled. "
            "Overhead bins hang open spilling more debris. A bright shaft of window light "
            "cuts across the airborne debris. The cabin is completely empty of any people "
            "or creatures. "
            + PROP_STYLE + HARD_NO_PEOPLE
        ),
    },
    {
        "filename": "04-harness-belt.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "Cinematic still-life hero shot of a heavy-duty BANANA AIRWAYS safety "
            "harness belt laid out flat on the seat of an empty yellow BANANA AIRWAYS "
            "cabin chair, photographed from a slight high-angle 3/4 perspective. The "
            "harness webbing is bright safety-yellow with red BANANA AIRWAYS stitching, "
            "a banana decal patch sewn on the front plate, and a chunky steel D-ring "
            "carabiner with a chunky locking gate. A thick coiled yellow safety rope "
            "rests next to the belt on the same seat, partially uncoiled, the loose end "
            "clipped into the carabiner. The belt is slightly worn, with scuffs and "
            "a couple of duct-tape repairs. Soft tungsten cabin light from above, a "
            "diffuse window glow behind. The cabin around the seat is completely empty "
            "— no other creatures, no people, no characters, no hands. Just the "
            "harness, the rope, the empty seat and the cabin environment. "
            + PROP_STYLE + HARD_NO_PEOPLE
        ),
    },
]


def main():
    print(f"Re-rolling {len(REROLLS)} props with hard NO-PEOPLE framing")
    results = {}
    threads = [threading.Thread(target=run_to_props, args=(j, results), daemon=True) for j in REROLLS]
    for t in threads:
        t.start(); time.sleep(0.3)
    for t in threads:
        t.join()
    print("\nDONE:")
    for j in REROLLS:
        print(f"  {j['filename']:25s} {results.get(j['filename'], ('missing',))[0]}")


if __name__ == "__main__":
    main()
