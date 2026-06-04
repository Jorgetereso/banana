"""Retry r02 — bypass submit() so the global STYLE (Banana Airways gameplay
context) is NOT appended to the prompt. The texture needs a clean prompt."""
import os, sys, urllib.request, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_gameplay import BASE, GPT, GPT_BODY, http_json, poll

PROPS_OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "PROPS")

PROMPT = (
    "A flat overhead photograph of black industrial cloth duct material, "
    "shot straight down. The image is filled entirely by the cloth weave "
    "surface, edge to edge. Matte black fabric with a fine diagonal "
    "cross-hatch weave pattern, subtle fiber detail, faint creases and slight "
    "wear marks distributed evenly across the whole surface. The pattern "
    "repeats consistently so that the image can tile seamlessly when used "
    "as a repeating material in a 3D engine.\n\n"
    "ABSOLUTE OUTPUT RULES:\n"
    "- Strictly top-down orthographic view, no perspective, no tilt.\n"
    "- Texture fills 100% of the frame, no white margin, no border.\n"
    "- Flat even ambient lighting, no shadow, no directional light.\n"
    "- NO people, NO characters, NO hands, NO objects, NO airplane, NO scene, "
    "NO environment, NO text, NO logo, NO label of any kind.\n"
    "- Just the fabric weave surface, like a scanned material swatch."
)

FILENAME = "r02-gorilla-tape-texture.png"


def main():
    body = {"prompt": PROMPT, **GPT_BODY}
    print(f"  [{FILENAME}] submitting (no STYLE)", flush=True)
    sub = http_json("POST", BASE + GPT, body)
    if sub.get("_error"):
        print(f"  SUBMIT FAIL {sub['status']}: {sub['body'][:300]}")
        return
    job_id = sub.get("job_id")
    print(f"  [{FILENAME}] queued as {job_id}", flush=True)
    final = poll(job_id)
    status = final.get("status") if final else "unknown"
    if status != "completed":
        print(f"  [{FILENAME}] FAIL status={status}")
        return
    urls = final.get("result", {}).get("urls", [])
    if not urls:
        print(f"  [{FILENAME}] no urls returned")
        return
    out = os.path.join(PROPS_OUT, FILENAME)
    req = urllib.request.Request(urls[0])
    with urllib.request.urlopen(req, timeout=120) as r, open(out, "wb") as f:
        f.write(r.read())
    print(f"  [{FILENAME}] OK saved -> {out}", flush=True)


if __name__ == "__main__":
    main()
