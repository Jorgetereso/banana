"""Generate shots 11-20 — character-consistent POV scenes featuring the 5 main characters.

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
    "ABSOLUTE CHARACTER RULES — read carefully and obey:\n\n"
    "These creatures are NOT chickens, NOT birds, NOT any animal. They are ORIGINAL "
    "FUZZY PUPPET CREATURES, like Muppets crossed with cartoon frogs. The word "
    "\"POLLO\" printed on some name tags is in-world brand text — it does NOT describe "
    "the species. Ignore that text completely when designing the creature.\n\n"
    "MANDATORY ANATOMY (all four humanoid characters share these):\n"
    "- Mouth is THICK SOFT RUBBER LIPS, like clay or jelly, in coral / pink / orange "
    "tones. The lips are the most defining feature, prominent and expressive, like a "
    "Muppet's mouth or a cartoon frog's mouth.\n"
    "- Eyes are LARGE WHITE GOOGLY EYES with small round pupils, very expressive, "
    "set wide on the face.\n"
    "- Body covered in FUZZY SHAGGY FUR in a solid bright color.\n"
    "- Two arms with chunky four-fingered hands.\n"
    "- Two legs ending in chunky bare feet, no shoes.\n"
    "- Some have a small SOFT TUFT of red or orange spikes on top of the head — this "
    "is a floppy decorative crest, NOT a chicken's comb.\n\n"
    "ABSOLUTELY FORBIDDEN — under no circumstances:\n"
    "- NO BEAKS of any kind. No pointed beaks, no duck bills, no bird bills. The "
    "mouth is ALWAYS thick rubber lips. If you draw a beak, you have failed.\n"
    "- NO FEATHERS. Body is fuzzy mammalian-style fur, not feathers.\n"
    "- NO WINGS. Always arms with hands.\n"
    "- NO BIRD ANATOMY of any kind.\n"
    "- NO chicken-shaped silhouettes, no chicken legs, no wattles, no chicken combs.\n\n"
    "CHARACTER ROSTER (match the attached reference images exactly):\n"
    "(1) ORANGE CHUBBY — rotund orange fuzzy body, soft floppy red crest tuft, big "
    "round green frog-like eyes, thick coral-pink rubber lips, two arms.\n"
    "(2) GREEN PIGTAILS — mossy green fuzzy body, two long braided pigtails tied with "
    "green ribbons, droopy small green eyes, thick coral-orange rubber lips, red "
    "bandana, white name tag.\n"
    "(3) PURPLE MUSCLE — bright purple fuzzy body, soft orange crest tuft, orange "
    "thick rubber lips, droopy small white eyes, huge muscle-bound torso with abs, "
    "chunky orange bare feet.\n"
    "(4) RED MUSTACHE — dark-red fuzzy body, sleepy droopy green eyes, magnificent "
    "dark-red handlebar mustache curling at the tips, red bandana, white name tag.\n"
    "(5) PURPLE OCTOPUS ALIEN — translucent purple cephalopod, green pacifier-like "
    "beak (ONLY this one has a beak), suction-cup tentacles, used as a face-hugger.\n\n"
    "Do not invent extra characters. Stick to this roster and the reference images."
)

JOBS = [
    {
        "filename": "11-buckle-orange.png",
        "endpoint": NB, "extra": dict(NB_BODY, imageUrls=[ORANGE]),
        "prompt": (
            "First-person POV crouched in the aisle at seat 4A of a battered Banana Airways "
            "propeller plane. Player hands at the bottom of the frame are tugging on the long "
            "ends of a yellow seatbelt, trying to stretch it across the enormous belly of the "
            "ORANGE CHUBBY character passenger seated in front of the camera. The Orange Chubby character's "
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
            "water and a tiny banana. Across the aisle, the GREEN PIGTAILS character with long braided "
            "pigtails leans aggressively out of her seat, mouth wide open mid-shout, droopy eyes "
            "narrowed, red bandana, name tag visible. She is jabbing one fuzzy finger at "
            "the player and pointing furiously at the water cup. Yellow Banana Airways cabin "
            "around them. " + CAST_NOTE
        ),
    },
    {
        "filename": "13-purple-flex-safety.png",
        "endpoint": NB, "extra": dict(NB_BODY, imageUrls=[PURPLE]),
        "prompt": (
            "First-person POV standing in the aisle of a Banana Airways cabin. The PURPLE "
            "MUSCLE character stands in front of the camera near the emergency exit row, flexing "
            "both massive biceps overhead while a deflated yellow life vest dangles around his "
            "neck. He is doing an enthusiastic safety briefing, lips parted in a confident "
            "grin, orange crest standing up. A folded BANANA AIRWAYS SAFETY CARD lies on the "
            "floor at his orange feet. Other passengers visible in the seats blurred out "
            "behind him, watching. Cabin lighting warm tungsten. " + CAST_NOTE
        ),
    },
    {
        "filename": "14-red-mustache-copilot.png",
        "endpoint": NB, "extra": dict(NB_BODY, imageUrls=[RED]),
        "prompt": (
            "First-person pilot POV inside the cockpit of a battered Banana Airways propeller "
            "plane. Player hands grip the left yellow Banana Airways yoke at the bottom of the "
            "frame. To the right of the player, in the co-pilot seat, the RED MUSTACHE character with the "
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
            "frame. Two steps away in the aisle, the GREEN PIGTAILS character with the long braided pigtails "
            "stumbles in panic, the PURPLE OCTOPUS ALIEN clamped fully across her face — its "
            "translucent purple body squashed onto her head, suction-cup tentacles wrapping "
            "around her braids and shoulders, its green pacifier-beak pressed against her "
            "forehead. The Green character's name tag flaps as she flails. Warning red light "
            "strobing on the ceiling. Slight motion blur on the bat. " + CAST_NOTE
        ),
    },
    {
        "filename": "16-orange-stuck-lavatory.png",
        "endpoint": NB, "extra": dict(NB_BODY, imageUrls=[ORANGE]),
        "prompt": (
            "First-person POV standing in the rear of a Banana Airways cabin, looking at a "
            "narrow lavatory door labelled WC. The ORANGE CHUBBY character is wedged into the "
            "doorway — head sticking out one side, one fuzzy arm out the other, his enormous "
            "rotund orange belly completely jamming the frame. Big green eyes desperate, coral "
            "lips pursed. Player hands at the bottom of the frame wield a rusty red crowbar, "
            "wedged against the door frame, ready to pry. A banana peel lies on the floor. "
            "Warning red light from above. " + CAST_NOTE
        ),
    },
    {
        "filename": "17-cast-huddle-manual.png",
        "endpoint": NB, "extra": dict(NB_BODY, imageUrls=[ORANGE, GREEN, PURPLE, RED]),
        "prompt": (
            "First-person POV at the center of a tight huddle of all FOUR main characters pressed "
            "around the camera in the dim Banana Airways cabin. Player hands at the bottom of "
            "the frame hold an open battered booklet labelled \"B.A.N.A.N.A. FLIGHT MANUAL\" "
            "with diagrams of a plane crashing. Surrounding the camera: ORANGE CHUBBY character on "
            "the left pointing at one page, GREEN PIGTAILS character on the right shaking her head, "
            "PURPLE MUSCLE character behind flexing one arm dramatically, RED MUSTACHE character stroking his mustache contemplatively. All four faces visible, all leaning in. "
            "Warm tungsten cabin light. " + CAST_NOTE
        ),
    },
    {
        "filename": "18-purple-lifts-engine.png",
        "endpoint": NB, "extra": dict(NB_BODY, imageUrls=[PURPLE]),
        "prompt": (
            "First-person POV standing on the wing of a Banana Airways propeller plane, mid-"
            "flight, harness rope clipped at the edge of frame. Player hands at the bottom of "
            "the frame grip a battered red wrench. In front of the camera, the PURPLE MUSCLE "
            "character is lifting an entire yellow-and-red radial engine clean off the wing with "
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
            "the RED MUSTACHE character co-pilot. The RED MUSTACHE character is FACE-TO-CAMERA in full meltdown "
            "— huge bulging green eyes, mustache twirling out of control, mouth open in a "
            "scream, both fuzzy hands grabbing the player by the lapels of an invisible "
            "uniform. Behind him, every cockpit gauge is spinning into the red, papers floating "
            "in mid-air. Player hands raised at the bottom of the frame trying to push him "
            "back. Red alarm light bathes everything. " + CAST_NOTE
        ),
    },
    {
        "filename": "20-cast-chase-aisle.png",
        "endpoint": NB, "extra": dict(NB_BODY, imageUrls=[ORANGE, GREEN, PURPLE, RED]),
        "prompt": (
            "First-person POV running backwards down the aisle of a Banana Airways cabin, "
            "looking back over the player's own shoulder. All four main characters are chasing the "
            "camera: ORANGE CHUBBY character leading at the front, fuzzy arms outstretched, lips "
            "wide open mid-shout, eyes blazing; behind him GREEN PIGTAILS character brandishing a "
            "rolled-up flight manual; PURPLE MUSCLE character behind her with both biceps flexed "
            "and orange crest puffed; RED MUSTACHE character at the back screaming. The cabin is "
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
