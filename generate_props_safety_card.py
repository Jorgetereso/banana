"""Generate a custom Banana Airways safety card pictogram with absurd jokes.
- vomit on neighbor
- explosive diarrhea on toilet
- crying baby driving parents insane
- one more bonus joke
"""
import os, sys, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_gameplay import NB, NB_BODY
from generate_props import run_to_props
from generate_props_modeling import MODEL_STYLE, HARD_NO_EXTRAS

JOBS = [
    {
        "filename": "m13-safety-card.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "Modeling reference: a folded paper AIRLINE SAFETY CARD lying flat on a "
            "pure white background, photographed top-down. The card is roughly the "
            "shape and proportions of a passport: yellow paper background with a thick "
            "RED border frame, top stripe and bottom stripe also red. Small red BANANA "
            "AIRWAYS logo at the top with a tiny silhouette of a propeller plane. The "
            "card is divided into FOUR horizontal panels stacked vertically, each panel "
            "showing a different absurd safety scenario in clean flat-colour stick-"
            "figure pictogram style (brown/dark-red figures on yellow background, big "
            "red arrows, big red X marks on the wrong actions, big red checkmarks or "
            "OK marks on the right actions). The four panels, top to bottom:\n\n"
            "PANEL 1 — VOMITING: a stick-figure passenger in an airline seat leaning "
            "out and projectile-vomiting an arc of liquid into the lap of the stick-"
            "figure neighbor in the next seat. RED X over the vomit. Right side of "
            "panel: a small icon of an airsickness paper bag with a big GREEN CHECK.\n\n"
            "PANEL 2 — EXPLOSIVE DIARRHEA: a stick-figure passenger sitting on a "
            "toilet bowl mid-relief, with cartoon explosion lines (jagged spike "
            "shapes) radiating out from underneath, motion lines, the toilet door "
            "blown off its hinges. Big RED X mark over the explosion. To the right, a "
            "small icon of someone calmly using the toilet with a GREEN CHECK.\n\n"
            "PANEL 3 — CRYING BABY MELTDOWN: a stick-figure baby in a parent's lap "
            "screaming with big tear-drop shapes flying out and the cartoon mouth wide "
            "open, while the parent stick-figure beside the baby has hands clutching "
            "their own head, hair sticking up in panic spikes, eyes scribbled wild. "
            "RED X over the chaos. To the right, a small icon of a LOLLIPOP being "
            "handed to the baby with a GREEN CHECK.\n\n"
            "PANEL 4 — FIGHTING OVER LAST SNACK: two stick-figure passengers tug-of-"
            "war over a tiny snack bag between them, both red-faced and yelling, "
            "speed-lines around. RED X over the fight. To the right, the small icon "
            "of one passenger calmly handing the snack to the other with a GREEN CHECK.\n\n"
            "Style: flat-colour vector pictogram, NOT photorealistic, no shading, no "
            "gradients. Looks like a real airline safety card you'd find in a seat "
            "pocket, but with absurd content. Same red/yellow BANANA AIRWAYS palette."
            + MODEL_STYLE + HARD_NO_EXTRAS
        ),
    },
]


def main():
    print("Generating safety card with absurd jokes")
    results = {}
    threads = [threading.Thread(target=run_to_props, args=(j, results), daemon=True) for j in JOBS]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(results)


if __name__ == "__main__":
    main()
