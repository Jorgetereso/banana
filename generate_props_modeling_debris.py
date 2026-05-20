"""Re-roll m12-debris-sheet with stricter no-scene framing."""
import os, sys, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_gameplay import NB, NB_BODY
from generate_props import run_to_props

JOBS = [
    {
        "filename": "m12-debris-sheet.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "PRODUCT CATALOG FLAT-LAY photograph. Pure white seamless background. NO "
            "scene. NO environment. NO cabin. NO airplane. NO people. NO characters. "
            "NO hands. NO POV. NO depth, NO perspective lines, NO horizon.\n\n"
            "Seven individual props arranged in a single horizontal row across the "
            "frame, each one separated and centred in its column, each one shot "
            "straight-down top-down so you see its outline clearly against the white "
            "background. Each item has a tiny soft contact shadow under it. The seven "
            "items, left to right:\n"
            "1. A rectangular brown plastic airline meal TRAY with three compartments "
            "containing a sad portion of beans, rice, and a roll.\n"
            "2. A crushed white paper COFFEE CUP, side lying on its side.\n"
            "3. A dented red aluminium SODA CAN with a generic label.\n"
            "4. A single yellow BANANA.\n"
            "5. A torn red foil SNACK BAG with chips spilling out.\n"
            "6. A folded paper SAFETY CARD (red and yellow) with stick-figure diagrams.\n"
            "7. A wrinkled paper BOARDING PASS.\n\n"
            "16:9 framing, all seven items fit comfortably across the frame at equal "
            "spacing. Soft even studio lighting. Same painted-3D BANANA AIRWAYS art "
            "style (slightly cartoony semi-realistic painted textures, punchy "
            "saturation) but rendered as ISOLATED PRODUCT ICONS on white, NOT as a "
            "scene. This is a sprite-sheet / modeling reference sheet, not gameplay."
        ),
    },
]


def main():
    print("Re-roll m12-debris-sheet")
    results = {}
    threads = [threading.Thread(target=run_to_props, args=(j, results), daemon=True) for j in JOBS]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(results)


if __name__ == "__main__":
    main()
