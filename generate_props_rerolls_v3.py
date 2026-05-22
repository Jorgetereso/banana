"""Three Krea re-rolls in parallel:
- m04-cart-b-three-quarter: isolated white, no people/hands/env (using user's reference)
- m07-suitcase-open-chaotic: same composition, REMOVE the eye in the middle
- m13-safety-card: same 4 panels but more chaotic / more intense
"""
import os, sys, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_gameplay import NB, NB_BODY
from generate_props import run_to_props

BASE = "https://jorgetereso.github.io/banana/assets/PROPS/ref"
CART_B_REF = f"{BASE}/cart-b-source.jpeg"
SUITCASE_REF = f"{BASE}/suitcase-open-source.png"
SAFETY_CARD_REF = f"{BASE}/safety-card-source.png"

JOBS = [
    {
        "filename": "m04-cart-b-three-quarter.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K", imageUrls=[CART_B_REF]),
        "prompt": (
            "Re-render the cart shown in the attached reference image, EXACTLY the "
            "same cart design — a chrome wire-mesh shopping trolley converted into a "
            "Banana Airways service cart, with a red push-bar handle, red corner caps, "
            "a plywood top, a side drink tray, a hanging painted BANANA AIRWAYS sign "
            "with bananas on the front grille, a green metal thermos held by rope at "
            "the back of the handle, and four caster wheels. 3/4 perspective from the "
            "front-right.\n\n"
            "ISOLATED on a PURE WHITE SEAMLESS BACKGROUND. Subtle soft contact shadow "
            "underneath. The cart is the only subject in the frame. NO people, NO "
            "characters, NO creatures, NO hands, NO arms, NO POV framing, NO airplane "
            "hangar, NO airplanes, NO background scenery, NO 'BANANA AIRWAYS' text or "
            "borders around the frame. Just the cart, clean, like a 3D modeling "
            "reference render or a product catalog photo. Painted-3D BANANA AIRWAYS "
            "art style (slightly cartoony, semi-realistic painted textures, punchy "
            "saturation). 16:9 framing. NO photorealism. NO film grain."
        ),
    },
    {
        "filename": "m07-suitcase-open-chaotic.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K", imageUrls=[SUITCASE_REF]),
        "prompt": (
            "Re-render the open bomb suitcase shown in the attached reference image, "
            "EXACTLY the same scene, exactly the same composition, exactly the same "
            "art style — open hard-shell carry-on in 3/4 perspective on a pure white "
            "background, lid flipped back, dark muted suitcase exterior with no banana "
            "sticker. Same chaotic interior: dense tangle of red, yellow, blue, green "
            "and black wires, multiple bundles of grey clay explosive bricks taped "
            "together, oversized blood-red digital countdown display reading \"00:38\", "
            "circuit boards, mercury switches, sparking frayed wire ends, brass trigger "
            "key in a keyhole, warning skull stickers stuck on the inside lid.\n\n"
            "ONE CRITICAL CHANGE: REMOVE the cartoon googly EYE from the centre of the "
            "wire nest. There must be NO eye anywhere in the suitcase. Everything else "
            "stays identical to the reference. Replace the eye with more tangled wires "
            "or a small additional component, do not leave a gap."
        ),
    },
    {
        "filename": "m13-safety-card.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K", imageUrls=[SAFETY_CARD_REF]),
        "prompt": (
            "Re-render the BANANA AIRWAYS airline safety card shown in the attached "
            "reference image. Keep the EXACT same layout, EXACT same format: yellow "
            "background, red border frame and stripes, red BANANA AIRWAYS logo with "
            "tiny plane silhouette at the top, \"AIRLINE SAFETY CARD\" red headline, "
            "four horizontal numbered panels stacked vertically (1, 2, 3, 4), each "
            "showing a stick-figure scenario in flat brown/dark-red on yellow, with "
            "a red X over the wrong action and a green check over the correct fix on "
            "the right side of each panel. Card laid flat on a white surface, photo-"
            "graphed top-down.\n\n"
            "MAKE IT MUCH MORE CHAOTIC AND INTENSE. Each panel should look MORE "
            "violent and unhinged than the reference:\n"
            "PANEL 1 — VOMITING: bigger projectile arc, more splash, the neighbor "
            "stick-figure covered in vomit splatters head-to-toe, motion lines, more "
            "drips, the vomiting passenger doubled over.\n"
            "PANEL 2 — EXPLOSIVE DIARRHEA: massive cartoon explosion lines and sharp "
            "spikes radiating from the toilet, toilet bowl visibly cracked, the door "
            "ripped off and flying across the panel, smoke clouds, the passenger's "
            "face contorted, motion lines everywhere.\n"
            "PANEL 3 — CRYING BABY MELTDOWN: gigantic baby with extreme tears flying "
            "in arcs, mouth open wider than the head, sound-wave lines emanating, "
            "the parent stick-figure literally tearing their own hair out in tufts, "
            "eyes squeezed shut, body bent in agony, panic spikes radiating from "
            "their head.\n"
            "PANEL 4 — SNACK FIGHT: full-on brawl over the snack bag, both passengers "
            "with steam coming out of their ears, fists clenched, snack bag torn in "
            "half mid-tug, chips flying out in every direction, motion lines, sparks, "
            "speech-bubble curses (just glyphs like @#$%).\n\n"
            "Style stays the same flat-colour vector pictogram, but the action in "
            "each panel must be visibly more chaotic, more intense, more cartoonishly "
            "violent. Same red/yellow BANANA AIRWAYS palette."
        ),
    },
]


def main():
    print(f"Running {len(JOBS)} re-rolls in parallel")
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
