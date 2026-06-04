"""Repair-kit props: gorilla tape roll + tileable Unity texture, wood plank, hammer.
Same isolated-on-white painted-3D aesthetic as the props v4 re-rolls."""
import os, sys, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_gameplay import NB, NB_BODY
from generate_props import run_to_props

# Same hard isolation clause that worked in v4
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

# Different rules for tileable Unity texture (no perspective, edge-to-edge fill)
TEXTURE_RULES = (
    "\n\nABSOLUTE OUTPUT RULES — these override anything else:\n"
    "- Output a FLAT TILEABLE TEXTURE for game-engine use (Unity material).\n"
    "- Strictly TOP-DOWN ORTHOGRAPHIC view, ZERO perspective, ZERO camera angle.\n"
    "- Image fills the ENTIRE FRAME EDGE-TO-EDGE with the texture surface only.\n"
    "- SEAMLESSLY TILEABLE: left edge matches right, top edge matches bottom.\n"
    "- NO background, NO shadow, NO white margin, NO label, NO logo, NO writing.\n"
    "- NO objects, NO scene, NO depth, NO 3D rendering.\n"
    "- Even flat studio lighting with no directional shadow.\n"
    "- 16:9 ratio. Will be cropped to square in engine."
)

JOBS = [
    {
        "filename": "r01-gorilla-tape-roll.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "A roll of heavy-duty black industrial gorilla tape (cloth duct tape). "
            "Thick matte-black cloth-backed tape wound into a cylindrical roll, "
            "about 5 cm wide. The roll is slightly used — one loose end of tape "
            "lifted and curled outward from the side, showing the slightly glossy "
            "sticky underside. Visible cross-hatch cloth weave pattern on the matte "
            "outer surface, edges a bit scratched and frayed. 3/4 perspective from "
            "the front-right, the roll sitting on one flat circular side." + ISOLATE
        ),
    },
    {
        "filename": "r02-gorilla-tape-texture.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "Seamless tileable surface texture of black industrial gorilla tape — "
            "the matte black cloth weave of duct tape, photographed completely "
            "flat top-down. Even diagonal cross-hatch cloth weave pattern across "
            "the entire frame, subtle wear and fiber detail, faint wrinkles and "
            "micro-creases, very slight reflectivity in the cloth fibers. The "
            "weave repeats consistently and the texture is designed to tile "
            "without visible seams when used as a Unity material." + TEXTURE_RULES
        ),
    },
    {
        "filename": "r03-wood-plank.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "A single rough wooden plank, roughly 80 cm long and 15 cm wide, the "
            "kind grabbed in a hurry to nail over a hole in a fuselage. Weathered "
            "pine, warm light-brown tone with visible grain, a couple of dark "
            "knots, splintered short edges, small crack near one end. Two bent "
            "rusty nails are half-driven into the surface near the corners. "
            "3/4 perspective from slightly above, plank lying flat with the long "
            "edge angled toward the camera so length and thickness are clear." + ISOLATE
        ),
    },
    {
        "filename": "r04-hammer.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "A simple classic claw hammer — wooden handle slightly scratched and "
            "worn from use (warm brown wood with grip wear marks near the head), "
            "forged dark steel double-end head with a flat striking face on one "
            "side and a two-pronged curved nail-puller claw on the other. "
            "Standard carpenter proportions, nothing fancy or fantasy. 3/4 side "
            "perspective, hammer laid flat with the head to the left and the "
            "handle extending to the right." + ISOLATE
        ),
    },
]


def main():
    print(f"Repair-kit props: {len(JOBS)} jobs")
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
