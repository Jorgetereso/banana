"""Repair v3:
- Plank: 3 views (top, side, 3/4) so the 1.5m x 30cm proportions read clearly
- Hammer: same double-faced concept but cleaner, more classic shape"""
import os, sys, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_gameplay import NB, NB_BODY
from generate_props import run_to_props

ISOLATE = (
    "\n\nABSOLUTE OUTPUT RULES — these override anything else:\n"
    "- Output a STILL-LIFE PRODUCT PHOTO of the subject only.\n"
    "- PURE WHITE SEAMLESS BACKGROUND. Subject centered. Soft contact shadow under it.\n"
    "- NO hands, NO arms, NO fingers, NO people, NO characters, NO creatures.\n"
    "- NO airplane, NO airplane interior, NO cabin, NO hangar, NO outdoor scene.\n"
    "- NO additional props in the frame.\n"
    "- NO border frame, NO inset card, NO 'BANANA AIRWAYS' text overlay on the image edges.\n"
    "- NO first-person POV framing. The camera is a tripod product camera.\n"
    "- 16:9 ratio. Subject fills ~60-80% of the frame, centered.\n"
    "- Painted-3D illustration style with semi-realistic textures, slightly cartoony "
    "proportions, soft global illumination."
)

PLANK_DESCRIPTION = (
    "A single rough wooden plank, 1.5 METRES long and 30 CM wide and about "
    "3 cm thick — clearly wide-format proportions: the plank is approximately "
    "5 times longer than it is wide. Weathered pine, warm light-brown tone "
    "with visible grain running lengthwise, a couple of dark knots, splintered "
    "short edges, a small crack near one end. Two bent rusty nails are "
    "half-driven into the top surface near the two short ends. Same painted-3D "
    "weathered aesthetic as the previous version."
)

JOBS = [
    {
        "filename": "r03a-plank-top.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            PLANK_DESCRIPTION + "\n\n"
            "VIEW: strict TOP-DOWN orthographic view, camera straight overhead "
            "looking directly down at the plank. The plank lies flat and fills "
            "the full width of the frame horizontally — the full 1.5m length "
            "spans almost the entire 16:9 frame from left to right, showing the "
            "true 5:1 wide-format proportions unambiguously. No perspective, no "
            "foreshortening." + ISOLATE
        ),
    },
    {
        "filename": "r03b-plank-side.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            PLANK_DESCRIPTION + "\n\n"
            "VIEW: PURE SIDE-PROFILE elevation view, camera at the same height "
            "as the plank, looking straight at its long edge. The plank runs "
            "horizontally across the entire frame from left to right as a long "
            "thin horizontal band, showing its full 1.5m length and 3 cm "
            "thickness clearly. The two bent rusty nails are visible sticking "
            "out from the top surface in profile. No perspective, no "
            "foreshortening." + ISOLATE
        ),
    },
    {
        "filename": "r03c-plank-three-quarter.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            PLANK_DESCRIPTION + "\n\n"
            "VIEW: 3/4 perspective from HIGH FRONT ANGLE (camera elevated "
            "looking down at ~45 degrees), so the wide-format proportions stay "
            "readable and don't get crushed by low-angle foreshortening. The "
            "plank lies flat, oriented diagonally across the frame with the "
            "long axis from lower-left to upper-right. Both nails visible on "
            "the top surface." + ISOLATE
        ),
    },
    {
        "filename": "r04-hammer.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "A classic clean ENGINEER'S CLUB HAMMER — traditional simple shape, "
            "no irregular bumps or forging marks. The wooden handle is straight "
            "and gently tapered, warm brown wood with a smooth surface, "
            "slightly worn from use. The metal head is a clean SYMMETRICAL "
            "forged dark steel block, RECTANGULAR / slightly hexagonal cross-"
            "section, with TWO FLAT POLISHED STRIKING FACES — one at each end. "
            "The head is perfectly symmetrical along its long axis so the "
            "hammer can hit either way. Absolutely NO claw, NO nail-puller, "
            "NO peen, NO curved end — just two flat hitting faces. Looks like "
            "a textbook club hammer / small sledge / stone-mason's hammer. "
            "Clean classic industrial shape, nothing fantasy, nothing weird. "
            "3/4 side perspective, hammer laid flat with the head to the left, "
            "handle extending to the right." + ISOLATE
        ),
    },
]


def main():
    print(f"Repair v3: {len(JOBS)} jobs (3 plank views + classic hammer)\n")
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
