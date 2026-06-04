"""Repair-kit v2 re-rolls:
- r01 + r02: gorilla tape lighter grey (real Gorilla brand colour, not pure black)
- r03: wood plank 1.5m x 30cm (wider/longer than v1)
- r04: simpler double-faced club hammer (two flat striking faces, no claw)

r01/r03/r04 use the normal run_to_props (STYLE injected — works with strong subject).
r02 bypasses submit() so the STYLE/Banana-Airways context is NOT appended."""
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
    "- 16:9 ratio. Subject fills ~60-70% of the frame, centered.\n"
    "- Painted-3D illustration style with semi-realistic textures, slightly cartoony "
    "proportions, soft global illumination."
)

# Jobs that go through normal pipeline (with STYLE injected)
WITH_STYLE_JOBS = [
    {
        "filename": "r01-gorilla-tape-roll.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "A roll of heavy-duty industrial duct tape in the classic GORILLA "
            "BRAND grey colour — dark slate-grey / charcoal with a visible "
            "silver-grey metallic sheen from the woven cloth fibres (NOT pure "
            "black, much lighter, like real Gorilla brand cloth tape — clearly "
            "grey, not black). Thick cloth-backed tape wound into a cylindrical "
            "roll about 5 cm wide. The roll is slightly used — one loose end of "
            "tape lifted and curled outward from the side, showing the darker "
            "slightly glossy sticky underside. Visible diagonal cross-hatch "
            "cloth weave pattern on the matte grey outer surface, edges a bit "
            "scratched and frayed. 3/4 perspective from the front-right, the "
            "roll sitting on one flat circular side." + ISOLATE
        ),
    },
    {
        "filename": "r03-wood-plank.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "A single rough wooden plank, large size — 1.5 METRES LONG and 30 "
            "CM WIDE (substantially wider and longer than a small board), the "
            "kind grabbed in a hurry to nail over a big hole in a fuselage. "
            "Wide proportions clearly readable — at least 5x longer than wide. "
            "Weathered pine, warm light-brown tone with visible grain running "
            "lengthwise, a couple of dark knots, splintered short edges, small "
            "crack near one end. Two bent rusty nails half-driven into the "
            "surface near the corners. 3/4 perspective from slightly above, "
            "plank lying flat with the long edge angled toward the camera so "
            "the wide format is clear. Same painted-3D weathered aesthetic as "
            "the previous narrower version, just bigger and wider." + ISOLATE
        ),
    },
    {
        "filename": "r04-hammer.png",
        "endpoint": NB, "extra": dict(NB_BODY, resolution="2K"),
        "prompt": (
            "A simple double-faced CLUB HAMMER (small drilling-hammer / sledge "
            "style) — wooden handle, warm brown wood, smooth round shape, "
            "slightly scratched and worn from use, no fancy decoration. The "
            "metal head is a chunky forged DARK STEEL BLOCK with TWO FLAT "
            "STRIKING FACES, one at each end of the head — symmetrical, you "
            "can hit with either side. Absolutely NO claw, NO nail-puller, "
            "NO peen, NO curved end — just two flat hitting faces. Simple, "
            "blocky, utilitarian shape, like a small sledgehammer or a stone "
            "mason's club hammer. 3/4 side perspective, hammer laid flat with "
            "one striking face to the left and the handle extending to the "
            "right." + ISOLATE
        ),
    },
]

# Job that needs STYLE-free prompt (texture, no subject to anchor against)
TEXTURE_PROMPT = (
    "A flat overhead photograph of grey industrial cloth duct material — the "
    "classic Gorilla Brand colour: dark slate-grey / charcoal with a slightly "
    "silvery metallic sheen from the woven cloth fibres (clearly grey, not "
    "pure black). Shot straight down. The image is filled entirely by the "
    "cloth weave surface, edge to edge. Fine diagonal cross-hatch weave "
    "pattern in slightly lighter silver-grey fibres, subtle fiber detail, "
    "faint creases and slight wear marks distributed evenly across the whole "
    "surface. The pattern repeats consistently so the image can tile "
    "seamlessly when used as a repeating material in a 3D engine.\n\n"
    "ABSOLUTE OUTPUT RULES:\n"
    "- Strictly top-down orthographic view, no perspective, no tilt.\n"
    "- Texture fills 100% of the frame, no white margin, no border.\n"
    "- Flat even ambient lighting, no shadow, no directional light.\n"
    "- NO people, NO characters, NO hands, NO objects, NO airplane, NO scene, "
    "NO environment, NO text, NO logo, NO label of any kind.\n"
    "- Just the fabric weave surface, like a scanned material swatch."
)


def run_no_style(job, results):
    """Direct submit that bypasses generate_gameplay.submit() (no STYLE append)."""
    name = job["filename"]
    try:
        body = {"prompt": job["prompt"], **job["extra"]}
        print(f"  [{name}] submitting (no STYLE)", flush=True)
        sub = http_json("POST", BASE + job["endpoint"], body)
        if sub.get("_error"):
            print(f"  [{name}] SUBMIT FAIL {sub['status']}: {sub['body'][:300]}")
            results[name] = ("error", sub); return
        job_id = sub.get("job_id")
        print(f"  [{name}] queued as {job_id}", flush=True)
        final = poll(job_id)
        status = final.get("status") if final else "unknown"
        if status != "completed":
            print(f"  [{name}] FAIL status={status}")
            results[name] = (status, final); return
        urls = final.get("result", {}).get("urls", [])
        if not urls:
            print(f"  [{name}] no urls"); results[name] = ("nourl", final); return
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
    texture_job = {
        "filename": "r02-gorilla-tape-texture.png",
        "endpoint": GPT, "extra": dict(GPT_BODY),
        "prompt": TEXTURE_PROMPT,
    }
    all_jobs = WITH_STYLE_JOBS + [texture_job]
    print(f"Repair v2: {len(all_jobs)} jobs ({len(WITH_STYLE_JOBS)} with STYLE, 1 without)\n")
    results = {}
    threads = []
    for j in WITH_STYLE_JOBS:
        threads.append(threading.Thread(target=run_to_props, args=(j, results), daemon=True))
    threads.append(threading.Thread(target=run_no_style, args=(texture_job, results), daemon=True))
    for t in threads:
        t.start(); time.sleep(0.3)
    for t in threads:
        t.join()
    print("\nDONE:")
    for j in all_jobs:
        print(f"  {j['filename']:40s} {results.get(j['filename'], ('missing',))[0]}")


if __name__ == "__main__":
    main()
