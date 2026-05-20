"""Generate hero prop shots for the reveal trailer.
4 props, no characters, in context inside the Banana Airways plane.
All Nano Banana Pro 2K. Wave-1-style aesthetic (proved to land the gameplay look)."""
import os, sys, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_gameplay import run, NB, NB_BODY, OUT_DIR  # OUT_DIR = assets/GAMEPLAY

PROPS_OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "PROPS")
os.makedirs(PROPS_OUT, exist_ok=True)

# Override OUT_DIR for prop generation by patching the run() expectation.
# Simpler: we'll just save to PROPS_OUT manually by overriding the filename to include path.

PROP_STYLE = (
    "In-engine prop hero shot for a reveal trailer, 16:9 cinematic framing, no HUD, "
    "no UI, no on-screen text overlays, no crosshair, NO CHARACTERS, NO HANDS, NO PEOPLE "
    "in the frame. Stylized 3D visuals in the language of GTA V / Far Cry — semi-realistic "
    "painted textures, slightly exaggerated proportions, punchy saturation, real-time "
    "lighting with mild bloom, subtle screen-space ambient occlusion, dramatic key light "
    "with soft fill. World is BANANA AIRWAYS, a rundown ultra-low-cost airline interior: "
    "battered cabin with worn red-and-yellow vinyl seats branded BANANA AIRWAYS, peeling "
    "banana-shaped decals, scuffed metal walls, dingy carpet, overhead bins, dim tungsten "
    "cabin lighting. The hero prop fills the central composition and is the clear subject. "
    "Slight wide-angle lens ~70-80° FOV. Clean cinematic frame. NO photorealism, NO "
    "ray-traced reflections, NO film grain, NO logos other than BANANA AIRWAYS / banana decals."
)

JOBS = [
    {
        "filename": "01-cart.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "Hero prop shot: a battered red-and-yellow stainless steel BANANA AIRWAYS "
            "service cart sitting in the narrow aisle of an airplane cabin, photographed "
            "from a low 3/4 front angle. The cart has a peeling BANANA AIRWAYS sticker "
            "on its front panel, a stylized banana decal underneath, chipped enamel "
            "paint, and a curled banana-yellow safety tag dangling from the push handle. "
            "Top of the cart is stacked with paper coffee cups, foil snack packets, a "
            "small basket of tiny bananas, and a half-empty coffee pot. Yellow vinyl "
            "BANANA AIRWAYS seats line the aisle in soft focus on both sides. Warm "
            "tungsten cabin lighting with a subtle window-light kicker from the right. "
            + PROP_STYLE
        ),
    },
    {
        "filename": "02-bomb-suitcase.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "Hero prop shot: an open hard-shell carry-on suitcase sitting on the dingy "
            "carpet of the airplane cabin, lid flipped back, viewed from a slight "
            "high-angle 3/4 perspective so the interior is clearly visible. Inside the "
            "suitcase: a tangled nest of red, yellow, blue and green wires, a small "
            "green-LED segmented timer counting down (\"00:38\"), bundles of grey "
            "clay-like explosive blocks taped together with electrical tape, and a "
            "folded paper labelled \"BANANA AIRWAYS DISARM MANUAL\" with a torn corner. "
            "A small banana decal stuck to the inside of the lid. Dim cabin light with "
            "a sharp red rim light from a warning lamp overhead casting tense shadows. "
            "Yellow BANANA AIRWAYS seat legs visible at frame edge. "
            + PROP_STYLE
        ),
    },
    {
        "filename": "03-airborne-debris.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "Hero shot: the interior of a battered BANANA AIRWAYS cabin captured "
            "mid-violent-turbulence, with food trays, plastic cups, foil snack bags, "
            "bananas, magazines, a thrown safety card, paper boarding passes and a "
            "single rolling coffee can all flying through the air mid-frame in chaotic "
            "tumbling arcs. Frozen motion-blur on the fastest items. The cabin floor "
            "tilts hard to one side. Yellow BANANA AIRWAYS seats are empty, seatbelts "
            "dangling. Overhead bins hang open. A bright shaft of light from a window "
            "cuts across the airborne debris. Strong sense of weightless impact, like "
            "a frozen frame from gameplay. "
            + PROP_STYLE
        ),
    },
    {
        "filename": "04-harness-belt.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "Hero prop shot: a heavy-duty BANANA AIRWAYS safety harness belt with a "
            "chunky steel D-ring carabiner, draped over the back of a yellow Banana "
            "Airways cabin seat. A thick coiled yellow safety rope rests on the seat "
            "next to the belt, partially uncoiled, with the rope's loose end hooked "
            "into the carabiner. The harness webbing is bright safety-yellow with red "
            "BANANA AIRWAYS stitching and a banana decal patch sewn on the front plate. "
            "Slightly worn, with scuffs and a couple of duct-tape repairs. Tungsten "
            "cabin light from above, soft window glow behind. 3/4 angle framing the "
            "harness as the clear hero. "
            + PROP_STYLE
        ),
    },
]


def run_to_props(job, results):
    """Wrapper: same as run() but saves into PROPS_OUT instead of GAMEPLAY."""
    import urllib.request
    from generate_gameplay import submit, poll
    name = job["filename"]
    try:
        print(f"  [{name}] submitting", flush=True)
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
                print(f"  [{name}] completed but no urls", flush=True)
                results[name] = ("nourl", final); return
            out = os.path.join(PROPS_OUT, name)
            req = urllib.request.Request(urls[0])
            with urllib.request.urlopen(req, timeout=120) as r, open(out, "wb") as f:
                f.write(r.read())
            print(f"  [{name}] OK saved -> {out}", flush=True)
            results[name] = ("ok", urls[0])
        else:
            print(f"  [{name}] FAIL status={status}", flush=True)
            results[name] = (status, final)
    except Exception as e:
        import traceback; traceback.print_exc()
        results[name] = ("exception", str(e))


def main():
    print(f"Generating {len(JOBS)} prop hero shots into {PROPS_OUT}\n")
    results = {}
    threads = [threading.Thread(target=run_to_props, args=(j, results), daemon=True) for j in JOBS]
    for t in threads:
        t.start(); time.sleep(0.3)
    for t in threads:
        t.join()
    print("\nSUMMARY:")
    for j in JOBS:
        print(f"  {j['filename']:25s} {results.get(j['filename'], ('missing',))[0]}")


if __name__ == "__main__":
    main()
