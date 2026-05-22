"""Re-rolls v4: strict isolated-on-white prompts, no BANANA AIRWAYS world context.
- m04 cart B: cropped ref, just clean it up isolated on white
- m07 suitcase: clean ref, same exact but no eye
- m13 safety card: clean ref, same exact but more chaotic"""
import os, sys, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_gameplay import NB, NB_BODY
from generate_props import run_to_props

BASE = "https://jorgetereso.github.io/banana/assets/PROPS/ref"
CART_REF = f"{BASE}/cart-b-cropped.png"
SUITCASE_REF = f"{BASE}/suitcase-open-source.png"
SAFETY_CARD_REF = f"{BASE}/safety-card-source.png"

# Hard-banned framing rules
ISOLATE = (
    "\n\nABSOLUTE OUTPUT RULES — these override anything else:\n"
    "- Output a STILL-LIFE PRODUCT PHOTO of the subject only.\n"
    "- PURE WHITE SEAMLESS BACKGROUND. Subject centered. Soft contact shadow under it.\n"
    "- NO hands, NO arms, NO fingers, NO people, NO characters, NO creatures.\n"
    "- NO airplane, NO airplane interior, NO cabin, NO hangar, NO outdoor scene.\n"
    "- NO additional props in the frame.\n"
    "- NO border frame, NO inset card, NO 'BANANA AIRWAYS' text overlay on the image edges.\n"
    "- NO first-person POV framing. The camera is a tripod product camera.\n"
    "- 16:9 ratio. Subject fills ~60-70% of the frame, centered.\n"
    "- Painted-3D illustration style with semi-realistic textures, slightly cartoony "
    "proportions, soft global illumination."
)

JOBS = [
    {
        "filename": "m04-cart-b-three-quarter.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K", imageUrls=[CART_REF]),
        "prompt": (
            "Re-render the shopping-cart-converted-to-airline-service-cart shown in "
            "the attached reference image, EXACTLY the same design (chrome wire mesh "
            "shopping cart frame, red push handle and red corner caps, plywood top "
            "screwed on, side metal drink tray, green metal thermos held by rope at "
            "the back of the handle, hanging painted 'BANANA AIRWAYS' sign with two "
            "bananas on the front grille, four caster wheels). Clean, full cart shown "
            "from wheels to top, 3/4 perspective from the front-right." + ISOLATE
        ),
    },
    {
        "filename": "m07-suitcase-open-chaotic.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K", imageUrls=[SUITCASE_REF]),
        "prompt": (
            "Re-render the open bomb suitcase shown in the attached reference image, "
            "EXACTLY the same composition, EXACTLY the same dark muted hard-shell "
            "suitcase, EXACTLY the same chaotic interior contents (tangled red/yellow/"
            "blue/green wires, multiple grey clay explosive bricks taped together, "
            "blood-red digital countdown '00:38', circuit boards, mercury switches, "
            "brass trigger key in keyhole, sparking frayed wire ends, warning skull "
            "stickers on the inside lid).\n\n"
            "ONLY CHANGE: REMOVE the cartoon googly EYE from the centre of the wire "
            "nest. There must be NO eye anywhere in the suitcase. Replace the eye's "
            "space with more tangled wires or an additional small electronic component. "
            "Everything else stays IDENTICAL to the reference image." + ISOLATE
        ),
    },
    {
        "filename": "m13-safety-card.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K", imageUrls=[SAFETY_CARD_REF]),
        "prompt": (
            "Re-render the airline safety card shown in the attached reference image. "
            "Keep the EXACT same overall layout, EXACT same red-on-yellow color scheme, "
            "EXACT same flat pictogram art style, EXACT same red border frame and "
            "stripes, EXACT same 'BANANA AIRWAYS' header logo and 'AIRLINE SAFETY CARD' "
            "title, EXACT same four numbered horizontal panels (1, 2, 3, 4), EXACT "
            "same red X / green check structure on each panel.\n\n"
            "MAKE EACH PANEL'S WRONG-ACTION SIDE MUCH MORE CHAOTIC AND INTENSE:\n"
            "PANEL 1 (VOMIT): bigger projectile vomit arc, more splash droplets, "
            "the neighbor stick-figure visibly covered head-to-toe in vomit splatters, "
            "motion lines.\n"
            "PANEL 2 (DIARRHEA): violent radial cartoon explosion lines from the "
            "toilet, the door blown clear off and flying away, smoke puffs, the "
            "passenger doubled over with motion shake lines.\n"
            "PANEL 3 (CRYING BABY): exaggerated wailing baby with arc-trajectory "
            "tears flying, mouth wider than the head, sound-wave ripples emanating, "
            "the parent stick-figure literally tearing tufts of hair out of their "
            "head, body bent in agony, panic-spike radiation around the head.\n"
            "PANEL 4 (SNACK FIGHT): full brawl, snack bag torn in half mid-tug, "
            "chips flying in every direction, both figures with steam coming from "
            "their ears, fists clenched, speech-bubble curse glyphs (@#$%), motion "
            "lines.\n\n"
            "The 'good action' icons on the right of each panel stay calm and unchanged." + ISOLATE
        ),
    },
]


def main():
    print(f"Re-rolls v4: {len(JOBS)} props")
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
