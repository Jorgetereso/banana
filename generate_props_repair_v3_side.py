"""Retry r03b plank side view — bypass STYLE so the Banana Airways context
isn't injected. Side profile of a long thin plank lacks strong subject
anchor so STYLE override-ed the prompt last time."""
import os, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_gameplay import BASE, GPT, GPT_BODY, http_json, poll
from generate_props import PROPS_OUT

PROMPT = (
    "Side-profile product photograph of a single rough wooden plank, 1.5 "
    "metres long and 30 cm wide and 3 cm thick. The plank is photographed "
    "from a pure horizontal side view (camera at the same height as the "
    "plank, looking straight at its long edge). The plank runs horizontally "
    "across the entire frame from left to right — like a long thin "
    "horizontal bar — clearly showing the full 1.5 m length and the 3 cm "
    "thickness as a slender horizontal band.\n\n"
    "The plank is weathered pine, warm light-brown tone, dark knots visible "
    "along its top edge, splintered short ends, with two bent rusty nails "
    "sticking out from the top surface (the nails are visible above the "
    "plank's top profile line). Painted-3D illustration style, semi-"
    "realistic textures.\n\n"
    "ABSOLUTE OUTPUT RULES:\n"
    "- PURE WHITE SEAMLESS BACKGROUND. Subject centered. Soft contact "
    "shadow under the plank.\n"
    "- Strict horizontal side elevation, NO perspective, NO foreshortening.\n"
    "- The plank fills almost the full width of the 16:9 frame.\n"
    "- NO hands, NO arms, NO people, NO characters, NO creatures.\n"
    "- NO airplane, NO cabin, NO hangar, NO outdoor scene, NO environment.\n"
    "- NO other props in the frame.\n"
    "- NO text, NO logo, NO label, NO writing."
)

FILENAME = "r03b-plank-side.png"


def main():
    body = {"prompt": PROMPT, **GPT_BODY}
    print(f"  [{FILENAME}] submitting (no STYLE, GPT-Image-2)", flush=True)
    sub = http_json("POST", BASE + GPT, body)
    if sub.get("_error"):
        print(f"  SUBMIT FAIL {sub['status']}: {sub['body'][:300]}"); return
    job_id = sub.get("job_id")
    print(f"  [{FILENAME}] queued as {job_id}", flush=True)
    final = poll(job_id)
    status = final.get("status") if final else "unknown"
    if status != "completed":
        print(f"  [{FILENAME}] FAIL status={status}"); return
    urls = final.get("result", {}).get("urls", [])
    if not urls:
        print(f"  no urls"); return
    out = os.path.join(PROPS_OUT, FILENAME)
    req = urllib.request.Request(urls[0])
    with urllib.request.urlopen(req, timeout=120) as r, open(out, "wb") as f:
        f.write(r.read())
    print(f"  [{FILENAME}] OK saved -> {out}", flush=True)


if __name__ == "__main__":
    main()
