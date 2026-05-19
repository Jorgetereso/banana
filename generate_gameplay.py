"""Generate the 10 gameplay POV shots via Krea API.

5 via Nano Banana Pro, 5 via GPT Image 2. Submits all in parallel,
polls each job, downloads to assets/GAMEPLAY/.
"""
import os, sys, time, json, threading, traceback
import urllib.request, urllib.error

PATAKEY = os.environ.get("Patakey")
if not PATAKEY:
    print("ERROR: Patakey env var not set"); sys.exit(1)

BASE = "https://api.krea.ai"
HEADERS = {
    "Authorization": f"Bearer {PATAKEY}",
    "Content-Type": "application/json",
}

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "GAMEPLAY")
os.makedirs(OUT_DIR, exist_ok=True)

STYLE = (
    "In-engine first-person gameplay screenshot, 16:9, no HUD, no UI, no on-screen text, no crosshair. "
    "Stylized 3D in the visual language of GTA V / Far Cry — semi-realistic painted textures, slightly "
    "exaggerated cartoon proportions, punchy saturation, real-time lighting with mild bloom, screen-space "
    "ambient occlusion. World is BANANA AIRWAYS, a rundown ultra-low-cost airline: red-and-yellow branding "
    "on seats and equipment, banana logo stickers, battered yellow-and-red propeller plane. Passengers and "
    "crew are fuzzy googly-eyed POLLO creatures with thick rubber lips and big white eyes, in orange / "
    "purple / green / blue fur. Player's first-person hands and forearms visible at the bottom of the "
    "frame — fingerless work gloves, slightly oversized cartoon proportions. Lens slight wide-angle ~90° "
    "FOV. NO photorealism, NO ray-traced reflections, NO cinematic film grain."
)

NB = "/generate/image/google/nano-banana-pro"
GPT = "/generate/image/openai/gpt-image-2"

NB_BODY = {"aspectRatio": "16:9", "resolution": "2K"}
GPT_BODY = {"width": 1536, "height": 864, "quality": "high"}

JOBS = [
    # ---------- NANO BANANA PRO (1-5) ----------
    {
        "filename": "01-coffee-cart.png", "endpoint": NB, "extra": NB_BODY,
        "prompt": (
            "First-person POV walking down the narrow aisle of a battered Banana Airways propeller "
            "plane, both player hands gripping the red push-handle of a steel Banana Airways food cart "
            "in the lower half of the frame. The cart is stacked with paper coffee cups, foil snacks "
            "and a single bruised banana. Yellow vinyl seats with red BANANA AIRWAYS logos line the "
            "aisle. In the mid-ground a furious purple fuzzy Pollo passenger leans out of seat 12C, "
            "lips wide open mid-shout, googly eyes locked on the camera, one fuzzy arm raised. Other "
            "Pollos peek over their headrests. Warm tungsten cabin lights, slight motion blur on the "
            "cart wheels, no UI."
        ),
    },
    {
        "filename": "02-making-coffee.png", "endpoint": NB, "extra": NB_BODY,
        "prompt": (
            "First-person POV inside the cramped rear galley of a beat-up Banana Airways plane. Player "
            "hands with fingerless work gloves visible at lower edge of frame — left hand steadies a "
            "chipped white BANANA AIRWAYS coffee mug on a stainless counter, right hand tilts a "
            "battered industrial coffee pot, hot dark coffee streaming mid-pour with steam curling up. "
            "Counter is cluttered with creamer pods, bent spoons, a half-eaten banana, a yellow rubber "
            "glove. A red warning light on the bulkhead casts a pulsing glow across the metal. "
            "Cabinets vibrate from turbulence, droplets of coffee mid-air. Banana logo sticker peeling "
            "on the coffee machine."
        ),
    },
    {
        "filename": "03-lollipop.png", "endpoint": NB, "extra": NB_BODY,
        "prompt": (
            "First-person POV crouched in the aisle of a Banana Airways cabin, leaning toward seat 7A. "
            "Player's right hand extended into the frame, fingers pinching the white paper stick of a "
            "rainbow-swirl lollipop, offering it forward. A sobbing fluffy green Pollo passenger "
            "buckled in the seat looks up — googly eyes wide and wet, thick rubber lips trembling, "
            "two big tears mid-fall. Yellow Banana Airways seat back behind them. Soft warm cabin "
            "light, slight depth-of-field on the lollipop, no UI, no text."
        ),
    },
    {
        "filename": "04-bat-bug.png", "endpoint": NB, "extra": NB_BODY,
        "prompt": (
            "First-person POV in the central aisle of a Banana Airways cabin, both player hands "
            "gripping a scratched wooden baseball bat lifted into a windup at the bottom of the frame. "
            "Standing in the aisle two steps away: a tall orange fuzzy Pollo teammate, arms flailing, "
            "with a chittering insectoid alien creature splayed across their face — many spindly legs "
            "wrapped around their head, oversized googly eyes of the Pollo barely peeking out. "
            "Teammate's body language is pure panic. Cabin seats blurred on either side, warning red "
            "light strobing on the ceiling. Slight motion blur on the bat."
        ),
    },
    {
        "filename": "05-missile-dodge.png", "endpoint": NB, "extra": NB_BODY,
        "prompt": (
            "First-person pilot POV inside the cockpit of a battered Banana Airways propeller plane. "
            "Both player hands in fingerless gloves grip a yellow Banana Airways yoke at the lower "
            "frame, knuckles tense, yoke banked hard left. Dashboard fills the lower third — analog "
            "gauges, scratched paint, banana stickers, a single dangling polaroid of a fluffy orange "
            "Pollo. Through the cracked, oil-streaked windshield: a green-blue mountain valley at "
            "sunset, and a missile streaking diagonally past the right window, white smoke trail "
            "curling, blast glow on the glass. Distant flak puffs in the sky."
        ),
    },
    # ---------- GPT IMAGE 2 (6-10) ----------
    {
        "filename": "06-engine-rope.png", "endpoint": GPT, "extra": GPT_BODY,
        "prompt": (
            "First-person POV dangling outside a Banana Airways propeller plane in mid-flight. Both "
            "player hands at the lower frame — one gripping a thick yellow safety rope clipped to a "
            "harness D-ring (visible at chest level), the other clamping a chunky red wrench against "
            "a bolt on the side of a sputtering yellow-and-red radial engine. The engine is leaking "
            "black smoke and dripping oil. The propeller spins blurred just beyond. Sky behind: "
            "bright daylight, scattered clouds, mountain ridges far below. Wind streaks the player's "
            "gloves and rope. The fuselage curves to the right — \"BANANA AIRWAYS\" painted in "
            "chipped yellow letters."
        ),
    },
    {
        "filename": "07-tape-wing.png", "endpoint": GPT, "extra": GPT_BODY,
        "prompt": (
            "First-person POV leaning out of a torn-open emergency door of a Banana Airways propeller "
            "plane mid-flight. Player's harness rope visible at the right edge of frame. Both hands "
            "at the bottom of the frame — left hand pressing a strip of grey silver duct tape onto "
            "the yellow-painted aluminum wing, right hand pulling the duct-tape roll outward "
            "stretching the tape. The wing has a jagged crack with fuel mist vapor streaming "
            "sideways from it in the slipstream. The propeller spins blurred just past the wing. Sky "
            "is overcast blue-grey, ocean far below. Wind flattens the player's gloves."
        ),
    },
    {
        "filename": "08-wood-fuselage.png", "endpoint": GPT, "extra": GPT_BODY,
        "prompt": (
            "First-person POV inside the rear of a Banana Airways cabin, standing in front of a "
            "jagged passenger-sized hole ripped out of the fuselage wall. Player's left hand at the "
            "bottom of the frame braces a rough pine plank diagonally across the hole, right hand "
            "swings a wooden-handled hammer mid-strike at a rusty nail. Several nails clamped "
            "between the player's teeth. Wind streaks visible papers and a stray banana peel flying "
            "past into the hole. Outside the hole: ocean far below at sunset, golden hour glow "
            "blasting into the cabin. Yellow Banana Airways seats in the periphery, one torn loose."
        ),
    },
    {
        "filename": "09-pull-up.png", "endpoint": GPT, "extra": GPT_BODY,
        "prompt": (
            "First-person pilot POV inside the cockpit of a battered Banana Airways propeller plane "
            "in a steep dive. Both player hands clenched white-knuckle on a yellow Banana Airways "
            "yoke at the bottom of the frame, yoke pulled hard back toward the camera. Dashboard "
            "analog gauges all spinning toward red. A massive red flashing PROXIMITY warning light "
            "bathes the entire cockpit in pulsing red. Through the windshield: a jagged forest-"
            "covered mountain ridge rushing up to fill the frame, treetops alarmingly close, sky a "
            "thin pale sliver at the top. Inside the cockpit, papers and a banana fly up off the "
            "dashboard."
        ),
    },
    {
        "filename": "10-bomb-suitcase.png", "endpoint": GPT, "extra": GPT_BODY,
        "prompt": (
            "First-person POV crouched on the cabin floor of a Banana Airways plane, looking "
            "straight down into an open hard-shell carry-on suitcase. Inside the suitcase: a tangled "
            "nest of red, yellow, blue and green wires, a small green-LED segmented timer counting "
            "down (\"00:38\"), bundles of grey clay-like blocks taped together, and a folded paper "
            "\"BANANA AIRWAYS DISARM MANUAL\" with a torn corner. Both player hands enter from the "
            "bottom of the frame — left hand pinching the red wire, right hand holding a pair of "
            "red-handled pliers hovering above it, just about to cut. Yellow Banana Airways carpet "
            "visible around the suitcase. Tense red rim light from a warning lamp overhead."
        ),
    },
]


def http_json(method, url, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"_error": True, "status": e.code, "body": e.read().decode(errors="replace")}


def submit(job):
    body = {"prompt": job["prompt"] + "\n\n" + STYLE, **job["extra"]}
    r = http_json("POST", BASE + job["endpoint"], body)
    return r


def poll(job_id, timeout=300):
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        r = http_json("GET", BASE + f"/jobs/{job_id}")
        last = r
        status = r.get("status")
        if status in ("completed", "failed", "cancelled"):
            return r
        time.sleep(3)
    return last


def download(url, path):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=120) as r, open(path, "wb") as f:
        f.write(r.read())


def run(job, results):
    name = job["filename"]
    try:
        print(f"  [{name}] submitting → {job['endpoint'].split('/')[-1]}", flush=True)
        sub = submit(job)
        if sub.get("_error"):
            print(f"  [{name}] SUBMIT FAIL {sub['status']}: {sub['body'][:300]}", flush=True)
            results[name] = ("error", sub)
            return
        job_id = sub.get("job_id")
        print(f"  [{name}] queued as {job_id}", flush=True)
        final = poll(job_id)
        status = final.get("status") if final else "unknown"
        if status == "completed":
            urls = final.get("result", {}).get("urls", [])
            if not urls:
                print(f"  [{name}] completed but no urls: {final}", flush=True)
                results[name] = ("nourl", final)
                return
            out = os.path.join(OUT_DIR, name)
            download(urls[0], out)
            print(f"  [{name}] ✓ saved → {out}", flush=True)
            results[name] = ("ok", urls[0])
        else:
            print(f"  [{name}] FAIL status={status}: {json.dumps(final)[:400]}", flush=True)
            results[name] = (status, final)
    except Exception:
        traceback.print_exc()
        results[name] = ("exception", None)


def main():
    print(f"Generating {len(JOBS)} gameplay shots → {OUT_DIR}")
    print(f"  5 via Nano Banana Pro · 5 via GPT Image 2\n")
    results = {}
    threads = [threading.Thread(target=run, args=(j, results), daemon=True) for j in JOBS]
    for t in threads:
        t.start()
        time.sleep(0.4)  # small stagger to avoid hammering the submit endpoint
    for t in threads:
        t.join()
    print("\n========== SUMMARY ==========")
    for j in JOBS:
        name = j["filename"]
        r = results.get(name, ("missing", None))
        print(f"  {name:25s} {r[0]}")


if __name__ == "__main__":
    main()
