"""Generate modeling-reference views of the 4 props.
White background, multiple angles, isolated. For the 3D modeler.

- Cart Option A (BANANA AIRWAYS cart): front + 3/4
- Cart Option B (supermarket trolley hack): front + 3/4
- Suitcase closed (NO banana sticker): front + 3/4
- Suitcase open MORE CHAOTIC: 3/4 + top-down
- Harness on Orange Chubby character: front + side
- Rope alone: 3/4 coiled with carabiner
- Debris items sheet: all flying items side-by-side on white
"""
import os, sys, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_gameplay import NB, NB_BODY
from generate_props import PROPS_OUT, run_to_props

ORANGE_REF = "https://jorgetereso.github.io/banana/assets/CHARACTER/cast/orange-chubby.png"

MODEL_STYLE = (
    "\n\nMODELING REFERENCE STYLE: Clean industrial-design product render against a "
    "PURE WHITE SEAMLESS BACKGROUND. The object is the only subject in the frame, "
    "centered, evenly lit with soft studio key + fill lighting from above, subtle "
    "contact shadow under the object. No environment, no cabin, no aircraft, no other "
    "props, no characters except where explicitly specified. The object reads clearly "
    "as a modelable form with all surface details, seams, hardware and proportions "
    "visible. Same painted-3D art language as BANANA AIRWAYS (slightly exaggerated "
    "cartoon proportions, semi-realistic painted textures, punchy saturation), but "
    "rendered as an isolated asset, like a Marketplace product page or a turntable "
    "render. NO photorealism. NO film grain. NO ray-traced reflections. NO HUD, NO UI."
)

HARD_NO_EXTRAS = (
    "\n\nNO other props in the frame. NO bananas anywhere unless explicitly described. "
    "NO BANANA AIRWAYS stickers / decals unless explicitly described. NO background "
    "objects, NO cabin parts, NO airplane parts. White background, isolated subject only."
)

JOBS = [
    # =========================================================
    # CART OPTION A — standard Banana Airways cart
    # =========================================================
    {
        "filename": "m01-cart-a-front.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "Modeling reference: a battered red-and-yellow stainless-steel airline "
            "service trolley, photographed straight-on FRONT view (orthographic-ish). "
            "Rectangular box on four small swivel casters, a push-bar handle along the "
            "top, a hinged front door with two latches, a peeling BANANA AIRWAYS sticker "
            "panel on the door, chipped enamel paint, scuffs. Top tray empty for clarity. "
            "Show the full cart from floor wheels to top handle, full silhouette readable."
            + MODEL_STYLE + HARD_NO_EXTRAS
        ),
    },
    {
        "filename": "m02-cart-a-three-quarter.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "Modeling reference: same battered red-and-yellow stainless-steel airline "
            "service trolley as the front view, now photographed from a 3/4 PERSPECTIVE "
            "angle from the front-left, showing the front face, the left side panel and "
            "the top in one shot. Reveals the depth of the cart, the casters underneath, "
            "the push-bar geometry. Same peeling BANANA AIRWAYS sticker on the front "
            "door panel. Empty top tray." + MODEL_STYLE + HARD_NO_EXTRAS
        ),
    },
    # =========================================================
    # CART OPTION B — supermarket trolley hack
    # =========================================================
    {
        "filename": "m03-cart-b-front.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "Modeling reference: a JURY-RIGGED airline service cart that is obviously "
            "a CONVERTED SUPERMARKET SHOPPING TROLLEY — they didn't have budget for "
            "real airline carts so they grabbed a chrome wire shopping cart and modified "
            "it. Front view. The base is a clearly recognizable wire-grid shopping "
            "trolley (chrome wire mesh sides, kid-seat flap at the back, four caster "
            "wheels with one wobbly front wheel). They've added: a flat plywood top "
            "screwed onto the rim to make a serving surface, a couple of stainless-steel "
            "lunch trays bolted to the sides as drink-holder shelves, a hand-painted "
            "BANANA AIRWAYS sign zip-tied to the front grille, a coffee thermos held in "
            "place with bungee cords, duct-tape repairs, mismatched wheels. Low-budget, "
            "hand-made, charming. Full cart shown front-on." + MODEL_STYLE + HARD_NO_EXTRAS
        ),
    },
    {
        "filename": "m04-cart-b-three-quarter.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "Modeling reference: same jury-rigged supermarket-trolley-converted airline "
            "cart from m03, now in 3/4 PERSPECTIVE view from the front-right. Shows the "
            "wire-mesh cage shape of the original shopping cart, the plywood top, the "
            "bolted-on side trays, the kid-seat flap at the back, the duct-tape repairs, "
            "the bungee-corded thermos and the hand-painted BANANA AIRWAYS sign zip-tied "
            "to the front." + MODEL_STYLE + HARD_NO_EXTRAS
        ),
    },
    # =========================================================
    # SUITCASE CLOSED — NO banana sticker
    # =========================================================
    {
        "filename": "m05-suitcase-closed-front.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "Modeling reference: a battered hard-shell carry-on suitcase, CLOSED, "
            "photographed straight-on from the FRONT (the wide face) at floor level. "
            "Rectangular hard-shell case in a muted dark colour (dark grey or navy), "
            "with two metal latches at the top, a sturdy carry handle, two small wheels "
            "at the bottom, scuffed corners, a few dings, an old airline luggage tag "
            "tied to the handle. NO banana sticker, NO BANANA AIRWAYS branding on the "
            "case. Generic-looking civilian carry-on. Full suitcase visible top to bottom."
            + MODEL_STYLE + HARD_NO_EXTRAS
        ),
    },
    {
        "filename": "m06-suitcase-closed-three-quarter.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "Modeling reference: same battered hard-shell carry-on suitcase from m05, "
            "still CLOSED, now in 3/4 PERSPECTIVE view from the front-right. Reveals "
            "the depth of the case, the side panel, the wheel housings, the handle "
            "extension slot on top. Same dark muted colour, same metal latches, same "
            "tag dangling from the handle. NO banana sticker, NO BANANA AIRWAYS "
            "branding." + MODEL_STYLE + HARD_NO_EXTRAS
        ),
    },
]


def main():
    print(f"Generating {len(JOBS)} modeling-reference shots into {PROPS_OUT} (batch 1/2)\n")
    results = {}
    threads = [threading.Thread(target=run_to_props, args=(j, results), daemon=True) for j in JOBS]
    for t in threads:
        t.start(); time.sleep(0.3)
    for t in threads:
        t.join()
    print("\nDONE batch 1:")
    for j in JOBS:
        print(f"  {j['filename']:40s} {results.get(j['filename'], ('missing',))[0]}")


if __name__ == "__main__":
    main()
