"""Re-generate harness-on-character shots using the NEW main-character ref."""
import os, sys, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_gameplay import NB, NB_BODY
from generate_props import run_to_props
from generate_props_modeling import MODEL_STYLE, HARD_NO_EXTRAS

MAIN_CHAR = "https://jorgetereso.github.io/banana/assets/CHARACTER/cast/main-character.png"

MAIN_CHAR_NOTE = (
    "\n\nMAIN CHARACTER — match the attached reference image EXACTLY. The character is:\n"
    "- A standing-upright fuzzy orange creature (NOT a chicken, NOT a bird, NOT any "
    "animal). Body shape: chubby-but-muscular torso with visible abs, two arms, two "
    "legs ending in chunky bare feet.\n"
    "- Fluffy spiky orange fur covering the whole body, with individual fur-spike tufts.\n"
    "- A large soft floppy RED CREST on top of the head, made of soft rubber/plush.\n"
    "- Large droopy GREEN frog-like eyes with small black pupils. The eyes are heavy-"
    "lidded and tired-looking. Big and prominent.\n"
    "- Thick coral-pink RUBBER LIPS (not a beak). The lips are puffy and prominent, "
    "like a muppet's mouth or a cartoon frog's lips. NEVER a beak.\n"
    "- A RED BANDANA / kerchief tied around the neck (the bandana is dark red with a "
    "subtle pattern, knotted at the front).\n"
    "- NO name tag. NO POLLO label. NO chicken anatomy. NO feathers. NO wings."
)

JOBS = [
    {
        "filename": "m09-harness-on-char-front.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K", imageUrls=[MAIN_CHAR]),
        "prompt": (
            "Modeling reference: THE MAIN CHARACTER (orange fluffy creature with red "
            "crest, droopy green eyes, coral lips and red bandana — see reference "
            "image) standing in a relaxed T-pose, photographed straight-on from the "
            "FRONT, full body. He is wearing a heavy-duty SAFETY HARNESS BELT in "
            "bright safety yellow with red BANANA AIRWAYS stitching: thick shoulder "
            "straps over each shoulder, a chest strap across the torso, a waist belt "
            "clipped at the front with a chunky steel buckle, leg loops, and a "
            "prominent steel D-RING CARABINER mounted at the chest. The harness fits "
            "over his fluffy orange fur, deforming it slightly. The bandana stays "
            "tied around the neck. Show the full character + harness clearly."
            + MAIN_CHAR_NOTE + MODEL_STYLE + HARD_NO_EXTRAS
        ),
    },
    {
        "filename": "m10-harness-on-char-side.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K", imageUrls=[MAIN_CHAR]),
        "prompt": (
            "Modeling reference: THE MAIN CHARACTER (orange fluffy creature with red "
            "crest, droopy green eyes, coral lips and red bandana — see reference "
            "image) standing in a relaxed T-pose, photographed from the LEFT SIDE "
            "(orthographic-ish side profile), full body. He is wearing the same "
            "heavy-duty safety harness as the front view: bright yellow webbing with "
            "red BANANA AIRWAYS stitching, shoulder strap visible going over the "
            "shoulder and around the back, waist belt going around the body, leg loops "
            "visible, the steel D-RING CARABINER on the front of the chest. The "
            "bandana stays tied around the neck."
            + MAIN_CHAR_NOTE + MODEL_STYLE + HARD_NO_EXTRAS
        ),
    },
]


def main():
    print(f"Re-generating {len(JOBS)} harness-on-character shots with new main-character ref")
    results = {}
    threads = [threading.Thread(target=run_to_props, args=(j, results), daemon=True) for j in JOBS]
    for t in threads:
        t.start(); time.sleep(0.3)
    for t in threads:
        t.join()
    print("\nDONE:")
    for j in JOBS:
        print(f"  {j['filename']:40s} {results.get(j['filename'], ('missing',))[0]}")


if __name__ == "__main__":
    main()
