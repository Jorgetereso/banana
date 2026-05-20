"""Batch 2 of modeling references: suitcase OPEN (chaotic) + harness on character
+ rope alone + debris items sheet."""
import os, sys, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_gameplay import NB, NB_BODY
from generate_props import PROPS_OUT, run_to_props
from generate_props_modeling import MODEL_STYLE, HARD_NO_EXTRAS
from generate_gameplay_cast import CAST_NOTE

ORANGE_REF = "https://jorgetereso.github.io/banana/assets/CHARACTER/cast/orange-chubby.png"

JOBS = [
    # =========================================================
    # SUITCASE OPEN — much more chaotic, scarier
    # =========================================================
    {
        "filename": "m07-suitcase-open-chaotic.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "Modeling reference: the SAME hard-shell carry-on suitcase, but now OPEN "
            "in a 3/4 perspective view from the front-right, lid flipped back, sitting "
            "on the white floor. The INTERIOR is a NIGHTMARE BOMB — far more chaotic "
            "and threatening than a generic bomb. Inside: a dense tangled nest of red, "
            "yellow, blue, green and black wires snaking everywhere, multiple bundles of "
            "grey clay-like explosive bricks taped together with electrical tape, an "
            "oversized blood-red digital countdown display reading \"00:38\" with a "
            "menacing glow, a cluster of mercury switches and circuit boards, a brass "
            "trigger key in a keyhole, frayed sparking wire ends, a single cartoonish "
            "googly EYE peeking out from the centre of the wire nest (creepy), small "
            "warning skull stickers stuck on the inside lid, ominous shadows in the case. "
            "Dark muted suitcase exterior, no banana sticker, no BANANA AIRWAYS branding. "
            + MODEL_STYLE + HARD_NO_EXTRAS
        ),
    },
    {
        "filename": "m08-suitcase-open-topdown.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "Modeling reference: TOP-DOWN view straight into the open chaotic bomb "
            "suitcase from m07. The camera looks vertically down into the interior. "
            "Visible: same dense tangle of red / yellow / blue / green / black wires, "
            "multiple bundles of grey clay explosive bricks, the oversized blood-red "
            "digital countdown reading \"00:38\", mercury switches and circuit boards, "
            "brass key in keyhole, sparking frayed wire ends, the creepy googly eye in "
            "the centre, warning skull stickers on the lid edge. The case rim frames "
            "the composition. NO banana sticker, NO BANANA AIRWAYS branding. White "
            "background outside the case." + MODEL_STYLE + HARD_NO_EXTRAS
        ),
    },
    # =========================================================
    # HARNESS on Orange Chubby character — front + side
    # =========================================================
    {
        "filename": "m09-harness-on-char-front.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K", imageUrls=[ORANGE_REF]),
        "prompt": (
            "Modeling reference: the ORANGE CHUBBY character standing in a relaxed "
            "T-pose, photographed straight-on from the FRONT, full body. He is wearing "
            "a heavy-duty SAFETY HARNESS BELT in bright safety yellow with red "
            "BANANA AIRWAYS stitching: a thick chest strap across his torso, shoulder "
            "straps over each shoulder, a waist belt clipped at the front with a chunky "
            "steel buckle, a prominent steel D-RING CARABINER mounted at the chest. "
            "The harness fits over his fluffy orange fur, deforming it slightly. Show "
            "the full character + harness clearly. " + CAST_NOTE + MODEL_STYLE
            + HARD_NO_EXTRAS
        ),
    },
    {
        "filename": "m10-harness-on-char-side.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K", imageUrls=[ORANGE_REF]),
        "prompt": (
            "Modeling reference: the ORANGE CHUBBY character standing in a relaxed "
            "T-pose, photographed from the LEFT SIDE (orthographic-ish side view), full "
            "body silhouette readable. Wearing the same heavy-duty safety harness as "
            "m09: bright yellow webbing with red BANANA AIRWAYS stitching, shoulder "
            "strap visible going over the shoulder and around the back, waist belt "
            "going around the body, the steel D-RING CARABINER on the front of the "
            "chest. " + CAST_NOTE + MODEL_STYLE + HARD_NO_EXTRAS
        ),
    },
    # =========================================================
    # ROPE alone, isolated
    # =========================================================
    {
        "filename": "m11-rope-coiled.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "Modeling reference: a thick coil of bright safety-yellow climbing-grade "
            "rope, neatly coiled into a circular bundle resting on a white surface, "
            "photographed from a slight high-angle 3/4 perspective. One loose end of "
            "the rope extends out of the coil toward the camera, terminating in a "
            "chunky steel locking carabiner. The rope shows woven braid texture, "
            "slightly worn but clean. Show the full coil and the carabiner clearly."
            + MODEL_STYLE + HARD_NO_EXTRAS
        ),
    },
    # =========================================================
    # DEBRIS items sheet — flat lay on white
    # =========================================================
    {
        "filename": "m12-debris-sheet.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "Modeling reference flat-lay: seven separate cabin-debris items arranged "
            "in a clean grid layout on a pure white seamless background, evenly spaced, "
            "each item photographed top-down for clear silhouette. The seven items, "
            "left to right: (1) a beat-up rectangular plastic airline food TRAY with "
            "compartments holding a sad portion of beans and rice, (2) a crushed white "
            "paper COFFEE CUP, (3) a dented aluminium SODA CAN with a generic label, "
            "(4) a single yellow BANANA, (5) a torn foil SNACK BAG with chips spilling "
            "out, (6) a folded BANANA AIRWAYS SAFETY CARD with stick-figure diagrams, "
            "(7) a wrinkled paper BOARDING PASS. Each item isolated with its own small "
            "contact shadow. Treat this as a product line-up sheet for modelers."
            + MODEL_STYLE
        ),
    },
]


def main():
    print(f"Generating {len(JOBS)} modeling references into {PROPS_OUT} (batch 2/2)\n")
    results = {}
    threads = [threading.Thread(target=run_to_props, args=(j, results), daemon=True) for j in JOBS]
    for t in threads:
        t.start(); time.sleep(0.3)
    for t in threads:
        t.join()
    print("\nDONE batch 2:")
    for j in JOBS:
        print(f"  {j['filename']:40s} {results.get(j['filename'], ('missing',))[0]}")


if __name__ == "__main__":
    main()
