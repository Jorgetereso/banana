"""Plank v4: longer — 2.5m x 25cm (~10:1 ratio).
3 views: top-down (Nano), 3/4 high (Nano), side-profile (GPT, no STYLE)."""
import os, sys, threading, time, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_gameplay import NB, NB_BODY, GPT, GPT_BODY, BASE, http_json, poll
from generate_props import run_to_props, PROPS_OUT

ISOLATE = (
    "\n\nABSOLUTE OUTPUT RULES — these override anything else:\n"
    "- Output a STILL-LIFE PRODUCT PHOTO of the subject only.\n"
    "- PURE WHITE SEAMLESS BACKGROUND. Subject centered. Soft contact shadow under it.\n"
    "- NO hands, NO arms, NO fingers, NO people, NO characters, NO creatures.\n"
    "- NO airplane, NO airplane interior, NO cabin, NO hangar, NO outdoor scene.\n"
    "- NO additional props in the frame.\n"
    "- NO border frame, NO inset card, NO 'BANANA AIRWAYS' text overlay on the image edges.\n"
    "- NO first-person POV framing. The camera is a tripod product camera.\n"
    "- 16:9 ratio. Subject fills ~80-90% of the frame width.\n"
    "- Painted-3D illustration style with semi-realistic textures, slightly cartoony "
    "proportions, soft global illumination."
)

PLANK_DESCRIPTION = (
    "A single very LONG rough wooden plank — 2.5 METRES long and 25 CM wide "
    "and about 3 cm thick. Extremely elongated proportions: the plank is "
    "approximately 10 TIMES LONGER than it is wide — long, narrow, like a "
    "scaffolding board or floor joist. Weathered pine, warm light-brown tone "
    "with visible grain running lengthwise, a couple of dark knots, splintered "
    "short edges, a small crack near one end. Two bent rusty nails are "
    "half-driven into the top surface near the two short ends. Same painted-3D "
    "weathered aesthetic as the previous version."
)

# Strong subject prompts — go through STYLE-injected pipeline
WITH_STYLE_JOBS = [
    {
        "filename": "r03a-plank-top.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            PLANK_DESCRIPTION + "\n\n"
            "VIEW: strict TOP-DOWN orthographic view, camera straight overhead "
            "looking directly down at the plank. The plank lies flat and "
            "spans the FULL WIDTH of the 16:9 frame edge to edge — its length "
            "almost touches the left and right edges of the frame. The width "
            "is only ~1/10 of the length, so it appears as a long narrow "
            "horizontal bar across the centre of the frame. No perspective, "
            "no foreshortening." + ISOLATE
        ),
    },
    {
        "filename": "r03c-plank-three-quarter.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            PLANK_DESCRIPTION + "\n\n"
            "VIEW: 3/4 perspective from HIGH FRONT ANGLE (camera elevated "
            "looking down at ~45 degrees), so the elongated proportions stay "
            "readable. The plank lies flat, oriented diagonally across the "
            "frame from lower-left corner to upper-right corner — long axis "
            "spanning the full diagonal so the extreme length is unmistakable. "
            "Both nails visible on the top surface." + ISOLATE
        ),
    },
]

# Side-profile prompt — no strong subject, must bypass STYLE
SIDE_PROMPT = (
    "Side-profile product photograph of a very long thin wooden plank, 2.5 "
    "metres long and 25 cm wide and 3 cm thick. The plank is photographed "
    "from a pure horizontal side view (camera at the same height as the "
    "plank, looking straight at its long edge). The plank runs horizontally "
    "across the ENTIRE WIDTH of the frame from edge to edge — it appears as "
    "an extremely long thin horizontal band, almost 10 times longer than it "
    "is tall in the frame, clearly showing the full 2.5 m length and the "
    "3 cm thickness as a slender horizontal strip.\n\n"
    "The plank is weathered pine, warm light-brown tone, dark knots visible "
    "along its top edge, splintered short ends, with two bent rusty nails "
    "sticking out from the top surface (the nails are visible above the "
    "plank's top profile line). Painted-3D illustration style, semi-"
    "realistic textures.\n\n"
    "ABSOLUTE OUTPUT RULES:\n"
    "- PURE WHITE SEAMLESS BACKGROUND. Subject centered. Soft contact "
    "shadow under the plank.\n"
    "- Strict horizontal side elevation, NO perspective, NO foreshortening.\n"
    "- The plank fills the FULL WIDTH of the 16:9 frame, edge to edge.\n"
    "- NO hands, NO arms, NO people, NO characters, NO creatures.\n"
    "- NO airplane, NO cabin, NO hangar, NO outdoor scene, NO environment.\n"
    "- NO other props in the frame.\n"
    "- NO text, NO logo, NO label, NO writing."
)


def run_no_style(job, results):
    name = job["filename"]
    try:
        body = {"prompt": job["prompt"], **job["extra"]}
        print(f"  [{name}] submitting (no STYLE)", flush=True)
        sub = http_json("POST", BASE + job["endpoint"], body)
        job_id = sub.get("job_id")
        print(f"  [{name}] queued as {job_id}", flush=True)
        final = poll(job_id)
        urls = final.get("result", {}).get("urls", []) if final else []
        if not urls:
            print(f"  [{name}] FAIL"); results[name] = ("fail", final); return
        out = os.path.join(PROPS_OUT, name)
        req = urllib.request.Request(urls[0])
        with urllib.request.urlopen(req, timeout=120) as r, open(out, "wb") as f:
            f.write(r.read())
        print(f"  [{name}] OK saved -> {out}", flush=True)
        results[name] = ("ok", urls[0])
    except Exception as e:
        import traceback; traceback.print_exc()
        results[name] = ("exception", str(e))


def main():
    side_job = {
        "filename": "r03b-plank-side.png",
        "endpoint": GPT, "extra": dict(GPT_BODY),
        "prompt": SIDE_PROMPT,
    }
    all_jobs = WITH_STYLE_JOBS + [side_job]
    print(f"Plank v4 (longer): {len(all_jobs)} jobs\n")
    results = {}
    threads = []
    for j in WITH_STYLE_JOBS:
        threads.append(threading.Thread(target=run_to_props, args=(j, results), daemon=True))
    threads.append(threading.Thread(target=run_no_style, args=(side_job, results), daemon=True))
    for t in threads:
        t.start(); time.sleep(0.3)
    for t in threads:
        t.join()
    print("\nDONE:")
    for j in all_jobs:
        print(f"  {j['filename']:40s} {results.get(j['filename'], ('missing',))[0]}")


if __name__ == "__main__":
    main()
