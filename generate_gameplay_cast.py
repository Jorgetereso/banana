"""Generate shots 11-20 — character-consistent POV scenes featuring the 5 main Pollos.

All via Nano Banana Pro. Each prompt attaches the relevant character reference images
via `imageUrls` so the model locks character design across shots.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_gameplay import run, OUT_DIR, NB, NB_BODY, STYLE
import threading, time

BASE_URL = "https://jorgetereso.github.io/banana/assets/CHARACTER/cast"

# 5 character refs
ORANGE   = f"{BASE_URL}/orange-chubby.png"
GREEN    = f"{BASE_URL}/green-pigtails.png"
PURPLE   = f"{BASE_URL}/purple-muscle.png"
RED      = f"{BASE_URL}/red-mustache.png"
OCTOPUS  = f"{BASE_URL}/octopus-on-orange.png"  # ref shows octopus attack pose

CAST_NOTE = (
    "CHARACTERS — the Pollos shown must EXACTLY match the attached reference images: "
    "(1) ORANGE chubby Pollo with red crest, big green frog-like eyes, thick coral-pink lips, "
    "fluffy spiky orange fur, rotund muscular body. "
    "(2) GREEN Pollo with two long braided pigtails tied with green ribbons, droopy green eyes, "
    "thick coral lips, red bandana around neck, white POLLO name tag, mossy green fur. "
    "(3) PURPLE muscular Pollo with bright orange crest and orange lips, droopy small eyes, "
    "huge muscle-bound torso with abs, orange feet, very flexed pose. "
    "(4) RED Pollo with luxurious dark-red handlebar mustache, sleepy green eyes, red bandana, "
    "white POLLO name tag, dark red fur. "
    "(5) PURPLE OCTOPUS ALIEN — translucent purple, green pacifier-like beak, suction-cup "
    "tentacles, used as a face-hugger that latches onto a Pollo's head. "
    "Do not invent other Pollos. Stick exactly to the design language of the references."
)

JOBS = [
    {
        "filename": "11-buckle-orange.png",
        "endpoint": NB, "extra": dict(NB_BODY, imageUrls=[ORANGE]),
        "prompt": (
            "First-person POV crouched in the aisle at seat 4A of a battered Banana Airways "
            "propeller plane. Player hands at the bottom of the frame are tugging on the long "
            "ends of a yellow seatbelt, trying to stretch it across the enormous belly of the "
            "ORANGE chubby Pollo passenger seated in front of the camera. The Orange Pollo's "
            "face is panicked — wide green eyes, thick coral lips pursed — both fuzzy little "
            "arms raised as the belt struggles to close around him. His red crest flops to one "
            "side. Yellow BANANA AIRWAYS seat back behind him. " + CAST_NOTE
        ),
    },
    {
        "filename": "12-green-demands-water.png",
        "endpoint": NB, "extra": dict(NB_BODY, imageUrls=[GREEN]),
        "prompt": (
            "First-person POV from behind a small black plastic serving tray held in the player's "
            "hands at the bottom of the frame — on the tray, a single half-filled paper cup of "
            "water and a tiny banana. Across the aisle, the GREEN Pollo with long braided "
            "pigtails leans aggressively out of her seat, mouth wide open mid-shout, droopy eyes "
            "narrowed, red bandana, POLLO name tag visible. She is jabbing one fuzzy finger at "
            "the player and pointing furiously at the water cup. Yellow Banana Airways cabin "
            "around them. " + CAST_NOTE
        ),
    },
    {
        "filename": "13-purple-flex-safety.png",
        "endpoint": NB, "extra": dict(NB_BODY, imageUrls=[PURPLE]),
        "prompt": (
            "First-person POV standing in the aisle of a Banana Airways cabin. The PURPLE "
            "muscular Pollo stands in front of the camera near the emergency exit row, flexing "
            "both massive biceps overhead while a deflated yellow life vest dangles around his "
            "neck. He is doing an enthusiastic safety briefing, lips parted in a confident "
            "grin, orange crest standing up. A folded BANANA AIRWAYS SAFETY CARD lies on the "
            "floor at his orange feet. Other Pollo passengers visible in the seats blurred out "
            "behind him, watching. Cabin lighting warm tungsten. " + CAST_NOTE
        ),
    },
    {
        "filename": "14-red-mustache-copilot.png",
        "endpoint": NB, "extra": dict(NB_BODY, imageUrls=[RED]),
        "prompt": (
            "First-person pilot POV inside the cockpit of a battered Banana Airways propeller "
            "plane. Player hands grip the left yellow Banana Airways yoke at the bottom of the "
            "frame. To the right of the player, in the co-pilot seat, the RED Pollo with the "
            "magnificent handlebar mustache is twirling the tip of his mustache with one fuzzy "
            "hand while completely ignoring the alarm lights — sleepy droopy green eyes, smug "
            "calm expression. The other yoke vibrates wildly in front of him. Through the "
            "cracked windshield: a thunderstorm with lightning, fuel gauge needle red. " + CAST_NOTE
        ),
    },
    {
        "filename": "15-octopus-on-green.png",
        "endpoint": NB, "extra": dict(NB_BODY, imageUrls=[GREEN, OCTOPUS]),
        "prompt": (
            "First-person POV in the central aisle of a Banana Airways cabin. Both player hands "
            "grip a scratched wooden baseball bat lifted into a windup at the bottom of the "
            "frame. Two steps away in the aisle, the GREEN Pollo with the long braided pigtails "
            "stumbles in panic, the PURPLE OCTOPUS ALIEN clamped fully across her face — its "
            "translucent purple body squashed onto her head, suction-cup tentacles wrapping "
            "around her braids and shoulders, its green pacifier-beak pressed against her "
            "forehead. The Green Pollo's POLLO name tag flaps as she flails. Warning red light "
            "strobing on the ceiling. Slight motion blur on the bat. " + CAST_NOTE
        ),
    },
    {
        "filename": "16-orange-stuck-lavatory.png",
        "endpoint": NB, "extra": dict(NB_BODY, imageUrls=[ORANGE]),
        "prompt": (
            "First-person POV standing in the rear of a Banana Airways cabin, looking at a "
            "narrow lavatory door labelled WC. The ORANGE chubby Pollo is wedged into the "
            "doorway — head sticking out one side, one fuzzy arm out the other, his enormous "
            "rotund orange belly completely jamming the frame. Big green eyes desperate, coral "
            "lips pursed. Player hands at the bottom of the frame wield a rusty red crowbar, "
            "wedged against the door frame, ready to pry. A banana peel lies on the floor. "
            "Warning red light from above. " + CAST_NOTE
        ),
    },
    {
        "filename": "17-pollo-huddle-manual.png",
        "endpoint": NB, "extra": dict(NB_BODY, imageUrls=[ORANGE, GREEN, PURPLE, RED]),
        "prompt": (
            "First-person POV at the center of a tight huddle of all FOUR main Pollos pressed "
            "around the camera in the dim Banana Airways cabin. Player hands at the bottom of "
            "the frame hold an open battered booklet labelled \"B.A.N.A.N.A. FLIGHT MANUAL\" "
            "with diagrams of a plane crashing. Surrounding the camera: ORANGE chubby Pollo on "
            "the left pointing at one page, GREEN braided Pollo on the right shaking her head, "
            "PURPLE muscular Pollo behind flexing one arm dramatically, RED mustache Pollo "
            "stroking his mustache contemplatively. All four faces visible, all leaning in. "
            "Warm tungsten cabin light. " + CAST_NOTE
        ),
    },
    {
        "filename": "18-purple-lifts-engine.png",
        "endpoint": NB, "extra": dict(NB_BODY, imageUrls=[PURPLE]),
        "prompt": (
            "First-person POV standing on the wing of a Banana Airways propeller plane, mid-"
            "flight, harness rope clipped at the edge of frame. Player hands at the bottom of "
            "the frame grip a battered red wrench. In front of the camera, the PURPLE muscular "
            "Pollo is lifting an entire yellow-and-red radial engine clean off the wing with "
            "both flexed arms above his head, biceps bulging, smug grin under orange lips, "
            "orange feet planted on the wing. Black oil drips from the engine. Sky behind: "
            "bright daylight, clouds. Wind streaks his purple fur. " + CAST_NOTE
        ),
    },
    {
        "filename": "19-red-cockpit-meltdown.png",
        "endpoint": NB, "extra": dict(NB_BODY, imageUrls=[RED]),
        "prompt": (
            "First-person POV in the cockpit of a Banana Airways plane, leaning across toward "
            "the RED Pollo co-pilot. The RED mustache Pollo is FACE-TO-CAMERA in full meltdown "
            "— huge bulging green eyes, mustache twirling out of control, mouth open in a "
            "scream, both fuzzy hands grabbing the player by the lapels of an invisible "
            "uniform. Behind him, every cockpit gauge is spinning into the red, papers floating "
            "in mid-air. Player hands raised at the bottom of the frame trying to push him "
            "back. Red alarm light bathes everything. " + CAST_NOTE
        ),
    },
    {
        "filename": "20-pollo-chase-aisle.png",
        "endpoint": NB, "extra": dict(NB_BODY, imageUrls=[ORANGE, GREEN, PURPLE, RED]),
        "prompt": (
            "First-person POV running backwards down the aisle of a Banana Airways cabin, "
            "looking back over the player's own shoulder. All four main Pollos are chasing the "
            "camera: ORANGE chubby Pollo leading at the front, fuzzy arms outstretched, lips "
            "wide open mid-shout, eyes blazing; behind him GREEN braided Pollo brandishing a "
            "rolled-up flight manual; PURPLE muscle Pollo behind her with both biceps flexed "
            "and orange crest puffed; RED mustache Pollo at the back screaming. The cabin is "
            "tilted from turbulence, banana peels on the floor, papers flying. Player's "
            "fingerless gloves visible at the bottom of the frame holding a half-eaten muffin "
            "as evidence. " + CAST_NOTE
        ),
    },
]


def main():
    print(f"Generating {len(JOBS)} character-consistent shots (all Nano Banana Pro)")
    print(f"Output → {OUT_DIR}\n")
    results = {}
    threads = [threading.Thread(target=run, args=(j, results), daemon=True) for j in JOBS]
    # Stagger to respect 8-job concurrency limit — we have 10, so the last 2 will queue
    # client-side via natural pacing. Start 8, wait for the first to finish before starting #9.
    for i, t in enumerate(threads):
        t.start()
        time.sleep(0.4)
        if i == 7:
            print("\n  -- 8 in-flight — waiting for one slot before next batch --\n")
            # Wait until at least one of the first 8 finishes
            while sum(1 for tt in threads[:8] if tt.is_alive()) >= 8:
                time.sleep(2)
    for t in threads:
        t.join()
    print("\n========== SUMMARY ==========")
    for j in JOBS:
        name = j["filename"]
        r = results.get(name, ("missing", None))
        print(f"  {name:30s} {r[0]}")


if __name__ == "__main__":
    main()
